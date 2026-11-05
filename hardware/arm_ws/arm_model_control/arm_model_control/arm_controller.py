"""阶段四：双臂控制器。

DualArmController 封装睿尔曼 SDK 连接、rm_movej_canfd 下发、UDP 反馈、
安全钩子（软停 rm_set_arm_slow_stop / watchdog system_error / rm_clear_system_err）。
仅第一台(左臂)初始化三线程模式开启 UDP 接收线程。

参考 Pico arm_controller.py：rm_movej_canfd(joint7补0, follow=False,
trajectory_mode=2, radio=200)。
"""

import threading
import time

SIDES = ("left", "right")


class DualArmController:
    """双臂 CANFD 跟随控制器。"""

    def __init__(self, left_ip, right_ip, port=8080, level=3, sdk_src=None,
                 udp_push_cycle_ms=2, enable_udp_push=True,
                 udp_port_left=8091, udp_port_right=8092, logger=None):
        self.ips = {"left": left_ip, "right": right_ip}
        self.port = int(port)
        self.level = int(level)
        self.sdk_src = sdk_src
        self.udp_push_cycle_ms = int(udp_push_cycle_ms)
        self.enable_udp_push = bool(enable_udp_push)
        self.udp_ports = {"left": int(udp_port_left), "right": int(udp_port_right)}
        self._logger = logger
        self._sdk = None
        self._robots = {}
        self._connected = False
        self._lock = threading.Lock()
        # 规划线程与 CANFD 控制线程共用 SDK：按臂串行化调用
        self._io_locks = {side: threading.Lock() for side in SIDES}
        self._last_joints = {"left": None, "right": None}

    def _log(self, side, msg):
        if self._logger is not None:
            self._logger.info(f"[{side}] {msg}")

    def connect(self):
        from arm_model_control.coordinate_align import _load_sdk
        self._sdk = _load_sdk(self.sdk_src)
        RoboticArm = self._sdk["RoboticArm"]
        rm_thread_mode_e = self._sdk["rm_thread_mode_e"]

        # 左臂：三线程模式（开启 UDP 接收线程，供 arm_observer 发布 /observation 话题）
        self._robots["left"] = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
        h = self._robots["left"].rm_create_robot_arm(
            self.ips["left"], self.port, self.level)
        if getattr(h, "id", -1) == -1:
            raise RuntimeError(f"左臂连接失败：{self.ips['left']}")

        # 右臂：普通模式
        self._robots["right"] = RoboticArm()
        h = self._robots["right"].rm_create_robot_arm(
            self.ips["right"], self.port, self.level)
        if getattr(h, "id", -1) == -1:
            raise RuntimeError(f"右臂连接失败：{self.ips['right']}")

        if self.enable_udp_push:
            self._configure_udp_push()
        self._configure_safety()
        self._connected = True
        return self

    def _configure_udp_push(self):
        rm_realtime_push_config_t = self._sdk.get("rm_realtime_push_config_t")
        if rm_realtime_push_config_t is None:
            return
        for side in SIDES:
            robot = self._robots[side]
            ret, cfg = robot.rm_get_realtime_push()
            ip, fc = "", -1
            if ret == 0 and cfg:
                ip = cfg.get("ip", "")
                if isinstance(ip, bytes):
                    ip = ip.decode("utf-8", errors="ignore")
                fc = int(cfg.get("force_coordinate", -1))
            # 双臂固定使用不同端口（左 8091 / 右 8092），不沿用机械臂历史配置
            config = rm_realtime_push_config_t(
                cycle=self.udp_push_cycle_ms, enable=True,
                port=self.udp_ports[side], force_coordinate=fc, ip=ip)
            robot.rm_set_realtime_push(config)

    def _configure_safety(self):
        for side in SIDES:
            robot = self._robots[side]
            # 避奇异：使用 RM 控制器内置接口（0=不规避奇异点，1=规避奇异点）。
            # 控制器在 rm_movej_canfd 执行期间自行规避奇异，planner 侧不再做过渡状态机。
            try:
                ret = robot.rm_set_avoid_singularity_mode(1)
                if ret == 0:
                    self._log(side, "避奇异模式已开启 rm_set_avoid_singularity_mode(1)")
                else:
                    self._log(side, f"rm_set_avoid_singularity_mode 返回 {ret}")
            except Exception as exc:
                self._log(side, f"rm_set_avoid_singularity_mode 失败：{exc}（忽略，继续）")
            for fn, arg in (("rm_set_collision_detection", 1),
                            ("rm_set_self_collision_enable", True),
                            ("rm_set_collision_state", 4)):
                try:
                    getattr(robot, fn)(arg)
                except Exception:
                    pass

    def disconnect(self):
        for side in SIDES:
            robot = self._robots.get(side)
            if robot is not None:
                try:
                    robot.rm_delete_robot_arm()
                except Exception:
                    pass
        self._robots = {}
        self._connected = False

    @property
    def connected(self):
        return self._connected

    # ---- 状态读取 ----
    def get_joints(self, side):
        """当前关节角(°)。"""
        with self._io_locks[side]:
            ret, joints = self._robots[side].rm_get_joint_degree()
        if ret != 0:
            raise RuntimeError(f"{side} rm_get_joint_degree 失败：{ret}")
        return [float(v) for v in joints[:6]]

    def get_pose(self, side):
        """当前末端位姿 [x,y,z,rx,ry,rz]。"""
        ret, state = self._robots[side].rm_get_current_arm_state()
        if ret != 0:
            raise RuntimeError(f"{side} rm_get_current_arm_state 失败：{ret}")
        return [float(v) for v in state["pose"][:6]]

    def get_system_err(self, side):
        with self._io_locks[side]:
            ret, err = self._robots[side].rm_get_system_err()
        return ret, err

    def clear_system_err(self, side):
        return self._robots[side].rm_clear_system_err()

    def slow_stop(self, side):
        """控制器级软停。"""
        try:
            with self._io_locks[side]:
                return self._robots[side].rm_set_arm_slow_stop()
        except Exception:
            return -1

    # ---- 关节空间运动（回 home / 定位） ----
    def move_joints(self, side, joints_deg, speed=20, block=True):
        """rm_movej 关节空间规划运动（阻塞等待到达）。

        注意：rm_movej 的关节数组长度须等于 arm_dof（RM_65 为 6），
        与 rm_movej_canfd 固定 7 元素不同，不能统一按 7 补齐。
        """
        j = [float(v) for v in joints_deg]
        dof = int(getattr(self._robots[side], "arm_dof", 0) or len(j))
        if len(j) > dof:
            j = j[:dof]
        elif len(j) < dof:
            j = j + [0.0] * (dof - len(j))
        ret = self._robots[side].rm_movej(j, int(speed), 0, 0, 1 if block else 0)
        if ret != 0:
            raise RuntimeError(f"{side} rm_movej 失败 ret={ret}")
        return ret

    def move_to_home(self, home_joints, speed=20):
        """双臂依次运动到 home 位姿（blocking rm_movej）。"""
        for side in SIDES:
            j = home_joints.get(side) if isinstance(home_joints, dict) else None
            if not j:
                self._log(side, "home 位姿缺少该侧数据，跳过")
                continue
            self._log(side, f"回 home 位姿: {[round(float(v), 2) for v in j[:6]]}")
            self.move_joints(side, j, speed=speed, block=True)

    # ---- 下发 ----
    def send_both_joints(self, joints, follow=False, trajectory_mode=2, radio=200):
        """双臂 rm_movej_canfd（CANFD 透传）。

        Args:
            joints: {side: 关节角(°)，6 或 7 元素} None=保持
        Returns:
            {side: ret} ret=0 成功，其它=SDK 错误码（仅含有目标的 side）
        """
        results = {}
        for side, j in joints.items():
            if j is None:
                continue
            j = [float(v) for v in j]
            if len(j) < 7:
                j = j + [0.0] * (7 - len(j))
            try:
                with self._io_locks[side]:
                    ret = self._robots[side].rm_movej_canfd(
                        j, follow, 0.0, trajectory_mode, radio)
                results[side] = int(ret)
                if ret == 0:
                    self._last_joints[side] = j[:6]
            except Exception:
                results[side] = -1000
        return results

    def last_command(self, side):
        with self._lock:
            return list(self._last_joints[side]) if self._last_joints[side] else None
