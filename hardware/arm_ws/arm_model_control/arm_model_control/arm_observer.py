# -*- coding: utf-8 -*-
"""双臂 UDP 实时数据接收模块。

在睿尔曼 SDK 三线程模式下开启 UDP 主动上报，将两台机械臂（按 IP 区分左右臂）
实时推送的关节角度、末端位姿封装为 ROS 标准消息格式：

    /observation/left_arm/joint_states   sensor_msgs/JointState
    /observation/right_arm/joint_states  sensor_msgs/JointState
    /observation/left_arm/pose           geometry_msgs/PoseStamped
    /observation/right_arm/pose          geometry_msgs/PoseStamped

- 若运行环境存在 rclpy（ROS 2），会自动创建节点并发布到上述真实话题；
- 否则将消息以与 ROS 消息字段完全一致的字典结构缓存在本地，可通过
  ``get_joint_state()`` / ``get_pose()`` / ``print_summary()`` 获取查看。
"""

import math
import threading
import time

try:
    # Reuse the one RealMan SDK module loaded by arm_model_control.coordinate_align.
    # A second module instance would break ctypes callback types.
    from Robotic_Arm.rm_robot_interface import (
        rm_realtime_arm_state_callback_ptr,
        rm_realtime_push_config_t,
    )
except ImportError as exc:
    raise ImportError("RealMan SDK must be loaded from third_party/realman_sdk/src") from exc

# 可选的 ROS 2 支持
try:
    import rclpy
    from geometry_msgs.msg import PoseStamped as RosPoseStamped
    from sensor_msgs.msg import JointState as RosJointState

    RCLPY_AVAILABLE = True
except ImportError:
    RCLPY_AVAILABLE = False


TOPIC_JOINT_STATES = {
    "left": "/observation/left_arm/joint_states",
    "right": "/observation/right_arm/joint_states",
}
TOPIC_POSE = {
    "left": "/observation/left_arm/pose",
    "right": "/observation/right_arm/pose",
}

JOINT_NAMES = [f"joint{i}" for i in range(1, 8)]


def euler_to_quaternion(roll, pitch, yaw):
    """欧拉角(RPY, rad, R=Rz(yaw)Ry(pitch)Rx(roll))转四元数 (x, y, z, w)。"""
    cr, sr = math.cos(roll / 2), math.sin(roll / 2)
    cp, sp = math.cos(pitch / 2), math.sin(pitch / 2)
    cy, sy = math.cos(yaw / 2), math.sin(yaw / 2)
    return (
        sr * cp * cy - cr * sp * sy,  # x
        cr * sp * cy + sr * cp * sy,  # y
        cr * cp * sy - sr * sp * cy,  # z
        cr * cp * cy + sr * sp * sy,  # w
    )


def ros_stamp(t=None):
    """生成与 builtin_interfaces/Time 一致的时间戳字典。"""
    t = time.time() if t is None else t
    sec = int(t)
    return {"sec": sec, "nanosec": int((t - sec) * 1e9)}


class DualArmUdpObserver:
    """双臂 UDP 实时状态观察者。

    依赖 SDK 三线程模式（RM_TRIPLE_MODE_E），UDP 推送数据到达后由 SDK
    内部接收线程回调 ``_on_udp_state``，按 ``arm_ip`` 区分左右臂。
    """

    def __init__(self, left_ip, right_ip, push_cycle_ms=50):
        self.left_ip = left_ip
        self.right_ip = right_ip
        self.push_cycle_ms = push_cycle_ms

        self._ip_to_side = {left_ip: "left", right_ip: "right"}
        self._callback = None  # 必须持有引用，防止被 GC 导致回调失效
        self._node = None
        self._ros_pubs = {}
        self._ros_msgs = {}  # 复用的 ROS 消息对象（rclpy 可用时才填充）

        # latest[side]["joint_state"] / ["pose"]：与 ROS 消息字段一致的字典
        self.latest = {
            side: {"joint_state": None, "pose": None} for side in ("left", "right")
        }
        self.rx_count = {"left": 0, "right": 0, "unknown": 0}

        # SDK 回调运行在独立接收线程，latest / rx_count 的读写需加锁
        self._lock = threading.Lock()
        self._last_err_log = 0.0

    # ------------------------------------------------------------------ #
    # 启动 / 配置
    # ------------------------------------------------------------------ #
    def start(self, callback_robot, push_robots):
        """注册全局 UDP 回调并为每台机械臂开启主动上报。

        Args:
            callback_robot: 用于注册回调的 RoboticArm 实例（回调为全局注册，任选一台）。
            push_robots: 需要开启 UDP 主动上报的 RoboticArm 实例列表。
        """
        self._callback = rm_realtime_arm_state_callback_ptr(self._on_udp_state)
        callback_robot.rm_realtime_arm_state_call_back(self._callback)
        print("UDP realtime state callback registered")

        for robot in push_robots:
            self.configure_udp_push(robot)

        if RCLPY_AVAILABLE:
            self._init_ros_node()

    def configure_udp_push(self, robot):
        """查询并更新 UDP 主动上报配置（保留原有目标 IP/端口，仅改周期与使能）。"""
        ret, cfg = robot.rm_get_realtime_push()
        if ret == 0 and cfg:
            ip = cfg.get("ip", "")
            if isinstance(ip, bytes):
                ip = ip.decode("utf-8", errors="ignore")
            port = int(cfg.get("port", 8080))
            force_coordinate = int(cfg.get("force_coordinate", -1))
        else:
            ip, port, force_coordinate = "", 8080, -1

        config = rm_realtime_push_config_t(
            cycle=self.push_cycle_ms,  # 5ms 的倍数
            enable=True,
            port=port,
            force_coordinate=force_coordinate,
            ip=ip,
        )
        ret = robot.rm_set_realtime_push(config)
        if ret == 0:
            print(f"UDP push enabled: cycle={self.push_cycle_ms}ms, port={port}, target_ip={ip or '(TCP peer)'}")
        else:
            print(f"UDP push config failed, err={ret}（请检查是否与机械臂同网段/防火墙设置）")
        return ret

    def _init_ros_node(self):
        try:
            if not rclpy.ok():
                rclpy.init()
            self._node = rclpy.create_node("dual_arm_udp_observer")
            self._ros_pubs = {
                ("joint", side): self._node.create_publisher(
                    RosJointState, TOPIC_JOINT_STATES[side], 10)
                for side in ("left", "right")
            }
            self._ros_pubs.update({
                ("pose", side): self._node.create_publisher(
                    RosPoseStamped, TOPIC_POSE[side], 10)
                for side in ("left", "right")
            })
            # 预创建消息对象，回调内只填充字段，避免每帧反复分配
            self._ros_msgs = {
                ("joint", side): RosJointState() for side in ("left", "right")
            }
            self._ros_msgs.update({
                ("pose", side): RosPoseStamped() for side in ("left", "right")
            })
            print("ROS 2 node 'dual_arm_udp_observer' started, publishing 4 topics")
        except Exception as e:  # noqa: BLE001
            print(f"ROS 2 init failed, fallback to local dict mode: {e}")
            self._node = None
            self._ros_pubs = {}

    # ------------------------------------------------------------------ #
    # SDK UDP 回调
    # ------------------------------------------------------------------ #
    def _on_udp_state(self, state):
        """SDK 回调：接收 rm_realtime_arm_joint_state_t，按 IP 区分左右臂。"""
        try:
            if state.errCode != 0:
                return
            arm_ip = state.arm_ip.decode("utf-8", errors="ignore").strip("\x00")
            side = self._ip_to_side.get(arm_ip)
            if side is None:
                with self._lock:
                    self.rx_count["unknown"] += 1
                return

            joint_state = self._build_joint_state(side, state.joint_status)
            pose_stamped = self._build_pose(side, state.waypoint)

            with self._lock:
                self.latest[side]["joint_state"] = joint_state
                self.latest[side]["pose"] = pose_stamped
                self.rx_count[side] += 1

            self._publish_ros(side, joint_state, pose_stamped)
        except Exception as e:  # noqa: BLE001
            # 回调运行在 SDK 接收线程中，必须保证不抛出异常
            self._log_err(f"UDP callback error: {e!r}")

    # ------------------------------------------------------------------ #
    # 消息构建
    # ------------------------------------------------------------------ #
    def _build_joint_state(self, side, js):
        """将 SDK 关节状态构建为 ROS JointState 字典。"""
        return {
            "header": {"stamp": ros_stamp(), "frame_id": f"{side}_arm_base"},
            "name": list(JOINT_NAMES),
            # SDK: 关节角度 °，速度 °/s，电流 mA -> ROS: rad, rad/s, effort(此处为电流 mA)
            # RM65 has six physical joints. The seventh recording slot is
            # explicit zero padding, never a value read from the SDK.
            "position": [math.radians(a) for a in js.joint_position[:6]] + [0.0],
            "velocity": [math.radians(v) for v in js.joint_speed[:6]] + [0.0],
            "effort": list(js.joint_current[:6]) + [0.0],
        }

    def _build_pose(self, side, wp):
        """将 SDK 末端位姿构建为 ROS PoseStamped 字典。"""
        return {
            "header": {"stamp": ros_stamp(), "frame_id": f"{side}_arm_base"},
            "pose": {
                "position": {"x": wp.position.x, "y": wp.position.y, "z": wp.position.z},
                "orientation": self._quaternion_from_waypoint(wp),
            },
        }

    @staticmethod
    def _quaternion_from_waypoint(wp):
        """从路点位姿提取归一化四元数；四元数无效时回退到欧拉角(rad)换算。"""
        q = wp.quaternion
        norm = math.sqrt(q.w * q.w + q.x * q.x + q.y * q.y + q.z * q.z)
        if norm > 1e-6:
            # 归一化，避免数值漂移导致非单位四元数
            return {"x": q.x / norm, "y": q.y / norm, "z": q.z / norm, "w": q.w / norm}
        # 上报中无有效四元数时由欧拉角(rad)换算
        x, y, z, w = euler_to_quaternion(wp.euler.rx, wp.euler.ry, wp.euler.rz)
        return {"x": x, "y": y, "z": z, "w": w}

    def _log_err(self, msg):
        """回调线程错误日志，节流为每秒最多打印一次，避免刷屏。"""
        now = time.time()
        if now - self._last_err_log >= 1.0:
            print(msg)
            self._last_err_log = now

    def _publish_ros(self, side, joint_state, pose_stamped):
        if not self._ros_pubs:
            return
        try:
            js_msg = self._ros_msgs[("joint", side)]
            js_msg.header.stamp.sec = joint_state["header"]["stamp"]["sec"]
            js_msg.header.stamp.nanosec = joint_state["header"]["stamp"]["nanosec"]
            js_msg.header.frame_id = joint_state["header"]["frame_id"]
            js_msg.name = joint_state["name"]
            js_msg.position = joint_state["position"]
            js_msg.velocity = joint_state["velocity"]
            js_msg.effort = joint_state["effort"]
            self._ros_pubs[("joint", side)].publish(js_msg)

            ps_msg = self._ros_msgs[("pose", side)]
            ps_msg.header.stamp.sec = pose_stamped["header"]["stamp"]["sec"]
            ps_msg.header.stamp.nanosec = pose_stamped["header"]["stamp"]["nanosec"]
            ps_msg.header.frame_id = pose_stamped["header"]["frame_id"]
            p = pose_stamped["pose"]["position"]
            o = pose_stamped["pose"]["orientation"]
            ps_msg.pose.position.x, ps_msg.pose.position.y, ps_msg.pose.position.z = p["x"], p["y"], p["z"]
            ps_msg.pose.orientation.x, ps_msg.pose.orientation.y = o["x"], o["y"]
            ps_msg.pose.orientation.z, ps_msg.pose.orientation.w = o["z"], o["w"]
            self._ros_pubs[("pose", side)].publish(ps_msg)
        except Exception as e:  # noqa: BLE001
            self._log_err(f"ROS publish error: {e!r}")

    # ------------------------------------------------------------------ #
    # 查询 / 展示
    # ------------------------------------------------------------------ #
    def get_joint_state(self, side):
        with self._lock:
            return self.latest[side]["joint_state"]

    def get_pose(self, side):
        with self._lock:
            return self.latest[side]["pose"]

    def print_summary(self):
        # 先取快照再打印，避免长时间持锁阻塞 SDK 回调线程
        with self._lock:
            rx = dict(self.rx_count)
            latest = {side: dict(self.latest[side]) for side in ("left", "right")}
        print("\n====== UDP Realtime Observation Summary ======")
        mode = "rclpy publish + local cache" if self._ros_pubs else "local cache (rclpy not found)"
        print(f"Mode: {mode}")
        for side in ("left", "right"):
            ip = self.left_ip if side == "left" else self.right_ip
            print(f"[{side} arm @ {ip}] rx={rx[side]}  "
                  f"topics: {TOPIC_JOINT_STATES[side]}, {TOPIC_POSE[side]}")
            js = latest[side]["joint_state"]
            ps = latest[side]["pose"]
            if js:
                pos_deg = [math.degrees(a) for a in js["position"]]
                print(f"  joint_states: {[f'{a:.3f}' for a in pos_deg]} (deg)")
            if ps:
                p = ps["pose"]["position"]
                o = ps["pose"]["orientation"]
                print(f"  pose: x={p['x']:.4f}, y={p['y']:.4f}, z={p['z']:.4f} m, "
                      f"quat=({o['x']:.4f}, {o['y']:.4f}, {o['z']:.4f}, {o['w']:.4f})")
        print("==============================================\n")

    # ------------------------------------------------------------------ #
    # 停止 / 清理
    # ------------------------------------------------------------------ #
    def stop(self):
        """停止发布并销毁 ROS 节点（在主线程/destroy_node 中调用，勿在 SDK 回调线程调用）。

        释放回调引用并销毁 rclpy 节点与发布者；机械臂断开后 SDK 不再触发回调。
        """
        self._callback = None
        if self._node is not None:
            try:
                self._node.destroy_node()
            except Exception:
                pass
            self._node = None
        self._ros_pubs = {}
        self._ros_msgs = {}
