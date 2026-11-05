"""RM65 SDK offline kinematics and limits.

SdkKinematics 持有一个离线 Algo(RM_65, RM_B) 实例，提供与睿尔曼控制器约定
完全一致的 FK / 欧拉↔四元数 / IK 全解 / 限位 / 奇异点 封装。

约定要点（已由 code-explorer 确认）：
  - FK(joint_deg, flag=1) -> [x,y,z,rx,ry,rz]（关节度，姿态弧度）
  - FK(joint_deg, flag=0) -> [x,y,z,w,x,y,z]（四元数 w-first）
  - euler2quaternion([rx,ry,rz] rad) -> [w,x,y,z]
  - quaternion2euler([w,x,y,z]) -> [rx,ry,rz] rad
内部统一四元数 (x,y,z,w) w-last；与 SDK 交互时重排为 [w,x,y,z]。
"""

import math


def _load_sdk(sdk_src=None):
    """Load only the bundled RealMan SDK selected by the launch script."""
    import importlib
    import os
    import sys
    if not sdk_src:
        raise ImportError("sdk_src must point to third_party/realman_sdk/src")
    sdk_root = os.path.realpath(sdk_src)
    expected = os.path.join(sdk_root, "Robotic_Arm", "rm_robot_interface.py")
    if not os.path.isfile(expected):
        raise ImportError(f"bundled RealMan SDK is missing: {expected}")
    loaded = sys.modules.get("Robotic_Arm.rm_robot_interface")
    if loaded is not None:
        if os.path.realpath(loaded.__file__) != os.path.realpath(expected):
            raise ImportError("RealMan SDK was already loaded from another location")
        return dict(vars(loaded))
    if sdk_root not in sys.path:
        sys.path.insert(0, sdk_root)
    mod = importlib.import_module("Robotic_Arm.rm_robot_interface")
    if os.path.realpath(mod.__file__) != os.path.realpath(expected):
        raise ImportError("RealMan SDK resolved outside third_party")
    return dict(vars(mod))


def _find_urdf(explicit=None):
    """定位 rm_65.urdf：优先显式路径，否则向上遍历源码树查找。"""
    import os
    if explicit:
        p = os.path.abspath(str(explicit))
        return p if os.path.isfile(p) else None
    here = os.path.dirname(os.path.abspath(__file__))
    probe = here
    for _ in range(8):
        cand = os.path.join(probe, "rm_65.urdf")
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    return None


def load_urdf_joint_limits(urdf_path, dof=6):
    """解析 URDF 关节限位（弧度→度），按 joint1..jointN 顺序返回 (jmin, jmax)。

    返回 None 表示解析失败或关节数不足。
    """
    import xml.etree.ElementTree as ET
    tree = ET.parse(urdf_path)
    root = tree.getroot()
    limits = {}
    for joint in root.iter("joint"):
        name = (joint.get("name") or "").strip()
        if not name.startswith("joint"):
            continue
        try:
            idx = int(name[len("joint"):])
        except ValueError:
            continue
        lim = joint.find("limit")
        if lim is None:
            continue
        try:
            lower = float(lim.get("lower"))
            upper = float(lim.get("upper"))
        except (TypeError, ValueError):
            continue
        limits[idx] = (math.degrees(lower), math.degrees(upper))
    if len(limits) < dof:
        return None
    jmin = [limits[i + 1][0] for i in range(dof)]
    jmax = [limits[i + 1][1] for i in range(dof)]
    return jmin, jmax


class SdkKinematics:
    """睿尔曼 SDK Algo 封装（离线，不连真臂）。"""

    def __init__(self, sdk_src=None, arm_model_name="RM_65", urdf_file=None, logger=None):
        sdk = _load_sdk(sdk_src)
        self._sdk = sdk
        Algo = sdk["Algo"]
        model_map = {
            "RM_65": sdk["rm_robot_arm_model_e"].RM_MODEL_RM_65_E,
            "RM_75": sdk["rm_robot_arm_model_e"].RM_MODEL_RM_75_E,
            "ECO_65": sdk["rm_robot_arm_model_e"].RM_MODEL_ECO_65_E,
            "GEN_72": sdk["rm_robot_arm_model_e"].RM_MODEL_GEN_72_E,
        }
        arm_model = model_map.get(arm_model_name, model_map["RM_65"])
        force_type = sdk["rm_force_type_e"].RM_MODEL_RM_B_E
        self.algo = Algo(arm_model, force_type)
        self.dof = int(getattr(self.algo, "arm_dof", 6)) or 6
        self.model_name = arm_model_name
        try:
            self.jmin = [float(v) for v in self.algo.rm_algo_get_joint_min_limit()][: self.dof]
            self.jmax = [float(v) for v in self.algo.rm_algo_get_joint_max_limit()][: self.dof]
            self.jspeed = [float(v) for v in self.algo.rm_algo_get_joint_max_speed()][: self.dof]
        except Exception:
            self.jmin = [-178.0, -130.0, -135.0, -178.0, -128.0, -360.0][: self.dof]
            self.jmax = [178.0, 130.0, 135.0, 178.0, 128.0, 360.0][: self.dof]
            self.jspeed = [180.0, 180.0, 225.0, 225.0, 225.0, 225.0][: self.dof]

        # 关节限位：URDF 覆盖（与 SDK 取交集，取更保守一侧）
        self.urdf_path = None
        self.urdf_vel_deg = None
        self.joint_limits_source = "sdk"
        urdf_path = _find_urdf(urdf_file)
        if urdf_path:
            try:
                urdf_limits = load_urdf_joint_limits(urdf_path)
                if urdf_limits:
                    u_min, u_max = urdf_limits
                    n = min(self.dof, len(u_min))
                    for i in range(n):
                        self.jmin[i] = max(self.jmin[i], u_min[i])
                        self.jmax[i] = min(self.jmax[i], u_max[i])
                    self.urdf_path = urdf_path
                    self.joint_limits_source = "urdf"
                # URDF 速度限制(°/s)与 SDK 取更保守一侧
                from arm_model_control.limits import load_joint_limits
                full = load_joint_limits(urdf_path, self.dof)
                if full:
                    self.urdf_vel_deg = list(full.vel_deg)
                    for i in range(min(self.dof, len(full.vel_deg))):
                        if full.vel_deg[i] > 0.0:
                            self.jspeed[i] = min(self.jspeed[i], full.vel_deg[i])
            except Exception:
                pass
        if logger is not None:
            logger.info(
                "关节限位来源=" + self.joint_limits_source
                + (" urdf=" + self.urdf_path if self.urdf_path else ""))

    # ---- 姿态转换（约定一致性核心）----
    def euler_to_quat(self, euler_rad):
        """欧拉 [rx,ry,rz](rad) -> 四元数 (x,y,z,w)。SDK 返回 [w,x,y,z]。"""
        wxyz = list(self.algo.rm_algo_euler2quaternion(list(euler_rad)))
        w, x, y, z = wxyz[0], wxyz[1], wxyz[2], wxyz[3]
        return (x, y, z, w)

    def quat_to_euler(self, quat_xyzw):
        """四元数 (x,y,z,w) -> 欧拉 [rx,ry,rz](rad)。SDK 输入 [w,x,y,z]。"""
        wxyz = [quat_xyzw[3], quat_xyzw[0], quat_xyzw[1], quat_xyzw[2]]
        return list(self.algo.rm_algo_quaternion2euler(wxyz))

    # ---- 正运动学 ----
    def fk(self, joints_deg, flag=1):
        """FK：关节角(度) -> [x,y,z,rx,ry,rz](rad) 或 flag=0 [x,y,z,w,x,y,z]。"""
        return list(self.algo.rm_algo_forward_kinematics(list(joints_deg), flag))

    # ---- 逆运动学全解 ----
    def ik_all(self, q_in_deg, target_pos, target_quat_xyzw):
        """IK 全解。

        Args:
            q_in_deg: 参考关节角(°)，6 元素（内部补齐 7）。
            target_pos: [x,y,z] m。
            target_quat_xyzw: 目标姿态 (x,y,z,w)。

        Returns:
            dict: result(0=成功), num, q_solve(list[list[float]] 各组解°),
                  q_ref。失败 result!=0 时 q_solve=[]。
        """
        q_in7 = list(q_in_deg[:6]) + [0.0] * (7 - len(q_in_deg))
        # 四元数 (x,y,z,w) -> SDK [w,x,y,z]
        q_pose = list(target_pos) + [target_quat_xyzw[3], target_quat_xyzw[0],
                                      target_quat_xyzw[1], target_quat_xyzw[2]]
        params = self._sdk["rm_inverse_kinematics_params_t"](
            q_in=q_in7, q_pose=q_pose, flag=0
        )
        solve = self.algo.rm_algo_inverse_kinematics_all(params)
        num = int(getattr(solve, "num", 0))
        result = int(getattr(solve, "result", 1))
        q_solve = []
        if result == 0 and num > 0:
            for i in range(num):
                row = list(solve.q_solve[i])[: self.dof]
                q_solve.append([float(v) for v in row])
        return {
            "result": result,
            "num": num,
            "q_solve": q_solve,
            "q_ref": [float(v) for v in solve.q_ref][: self.dof],
        }

    def ik_select(self, weight, ik_all_result):
        """SDK 选解 -> 最优索引（取 ik_all_result 的全解结构体）。"""
        return int(self.algo.rm_algo_ikine_select_ik_solve(list(weight), ik_all_result["_solve"]))

    # ---- 限位 / 速度校验 ----
    def check_position_limit(self, q_deg):
        """0=未超限, i=第i关节超限, -1=非6DoF。

        注意：SDK 包装器 rm_algo_ikine_check_joint_position_limit 直接传 list 会
        触发 ctypes.ArgumentError（绑定要求 POINTER(c_float)），此处手动转数组。
        """
        import ctypes
        arr = (ctypes.c_float * 8)(*([float(v) for v in q_deg[:6]] + [0.0, 0.0]))
        return int(self.algo.rm_algo_ikine_check_joint_position_limit(arr))

    def check_velocity_limit(self, dt_sec, q_ref_deg, q_deg):
        """0=未超速, i=第i关节超速, -1=非6DoF。"""
        q_ref8 = list(q_ref_deg[:6]) + [0.0] * (8 - len(q_ref_deg))
        q8 = list(q_deg[:6]) + [0.0] * (8 - len(q_deg))
        return int(self.algo.rm_algo_ikine_check_joint_velocity_limit(
            float(dt_sec), q_ref8, q8))

    # ---- 奇异点 ----
    def singularity_analyse(self, q_deg):
        """解析法奇异点（6DoF）。返回 (code, shoulder_distance_m)。
        code: 0=正常 -1=肩部 -2=肘部 -3=腕部。"""
        code, dist = self.algo.rm_algo_kin_robot_singularity_analyse(list(q_deg[:6]))
        return int(code), float(dist)

    def universal_singularity(self, q_deg, limit=0.01):
        """雅可比最小奇异值兜底（7 长度）。0=正常 -1=奇异 -2=失败。"""
        q7 = list(q_deg[:6]) + [0.0] * (7 - len(q_deg))
        return int(self.algo.rm_algo_universal_singularity_analyse(q7, float(limit)))

    def set_singularity_thresholds(self, limit_qe_deg=10.0, limit_qw_deg=10.0, limit_d_m=0.05):
        self.algo.rm_algo_kin_set_singularity_thresholds(
            float(limit_qe_deg), float(limit_qw_deg), float(limit_d_m))
