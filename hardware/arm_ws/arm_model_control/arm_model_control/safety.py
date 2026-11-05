"""阶段四：安全约束校验门。

SafetyGate 对 IK 解执行多重校验，全部通过才放行：
  1. 工作空间边界（水平到达 + 可达球）
  2. 关节限位（SDK check_joint_position_limit）
  3. 单步最大变化量（max_step_rad）
  4. 正运动学残差（FK(q_target) vs 目标位姿）
  5. 三层奇异点（解析 + 雅可比兜底）-> 速度缩放/冻结

参考 Pico safety_hooks + 奇异点三层检测。
"""

import math
from dataclasses import dataclass

from arm_model_control.coordinate_align import SdkKinematics
from arm_model_control.math_utils import (
    angle_diff_deg,
    quat_inverse,
    quat_multiply,
    quat_to_rotvec,
)

STATUS_HOLD = 0
STATUS_NORMAL = 1
STATUS_RISK = 2
STATUS_SINGULARITY = 3
STATUS_ESCAPE = 4  # 已废弃：避奇异现由 RM 控制器 rm_set_avoid_singularity_mode 处理


@dataclass
class SafetyResult:
    q_target_deg: list | None   # 校验通过的关节目标(°)，None=该周期不下发(hold)
    valid: bool
    risk: float
    speed_scale: float
    status_code: int
    reason: str


class SafetyGate:
    """IK 解安全校验门 + 速度缩放。"""

    def __init__(self, kin: SdkKinematics,
                 max_step_rad=0.08,
                 fk_pos_tol_m=0.008,
                 fk_rot_tol_rad=0.05,
                 workspace_r_m=0.6,
                 workspace_sphere_m=0.95,
                 singularity_warn_m=0.08,
                 singularity_stop_m=0.04,
                 speed_min_scale=0.2,
                 universal_value_limit=0.015,
                 max_j4_step_deg=40.0):
        self.kin = kin
        self.max_step_deg = math.degrees(float(max_step_rad))
        # 第 4 轴（腕部俯仰）单步上限：比整体 90° 更严，专门拦翻腕式跳变。
        self.max_j4_step_deg = float(max_j4_step_deg)
        self.fk_pos_tol = float(fk_pos_tol_m)
        self.fk_rot_tol = float(fk_rot_tol_rad)
        self.workspace_r = float(workspace_r_m)
        self.workspace_sphere = float(workspace_sphere_m)
        self.warn_m = float(singularity_warn_m)
        self.stop_m = float(singularity_stop_m)
        self.speed_min = float(speed_min_scale)
        self.universal_limit = float(universal_value_limit)

    def validate(self, q_target_deg, q_current_deg,
                 target_pos, target_quat_xyzw, ik_risk, ik_sing_code):
        """多重校验。失败返回 hold。"""
        # 1) 工作空间边界（目标位置）
        horizontal = math.sqrt(target_pos[0] ** 2 + target_pos[1] ** 2)
        sphere = math.sqrt(sum(v * v for v in target_pos))
        if horizontal > self.workspace_r or sphere > self.workspace_sphere:
            return self._hold(ik_risk, f"workspace h={horizontal:.3f} s={sphere:.3f}")

        # 2) 关节限位
        for i, v in enumerate(q_target_deg[: self.kin.dof]):
            if v < self.kin.jmin[i] or v > self.kin.jmax[i]:
                return self._hold(ik_risk, f"joint_limit i={i} v={v:.2f}")
        if self.kin.check_position_limit(q_target_deg) != 0:
            return self._hold(ik_risk, "position_limit_sdk")

        # 3) 单步最大变化量（关节角走最短路径，避免 ±180° 跨象限误判）
        dq = [angle_diff_deg(q_target_deg[i], q_current_deg[i])
              for i in range(self.kin.dof)]
        max_dq = max(abs(v) for v in dq)
        # 只拦截翻转分支/完全错误解(~180°)；正常跟随步进交由 executor 平滑器钳制。
        if max_dq > 90.0:
            return self._hold(ik_risk, f"step_exceeded {max_dq:.3f}>90.0")
        # 3b) 第 4 轴单独更严：禁止翻腕式的大幅翻转（J4∓180）
        if len(dq) > 3 and abs(dq[3]) > self.max_j4_step_deg:
            return self._hold(
                ik_risk, f"j4_step {abs(dq[3]):.2f}>{self.max_j4_step_deg:.0f}")

        # 4) FK 残差
        fk = self.kin.fk(q_target_deg, flag=0)  # [x,y,z,w,x,y,z]
        fk_pos = fk[:3]
        # FK 四元数输出 [w,x,y,z] -> (x,y,z,w)
        fk_quat_xyzw = (fk[4], fk[5], fk[6], fk[3])
        resid_pos = math.sqrt(sum(
            (fk_pos[i] - target_pos[i]) ** 2 for i in range(3)))
        q_err = quat_multiply(target_quat_xyzw, quat_inverse(fk_quat_xyzw))
        rv = quat_to_rotvec(q_err)
        resid_rot = math.sqrt(sum(v * v for v in rv))
        if resid_pos > self.fk_pos_tol or resid_rot > self.fk_rot_tol:
            return self._hold(ik_risk,
                              f"fk_residual pos={resid_pos:.4f} rot={resid_rot:.4f}")

        # 5) 三层奇异点 -> 速度缩放
        code, dist = self.kin.singularity_analyse(q_target_deg)
        risk = max(ik_risk, self._risk_from_distance(dist))
        if self.kin.universal_singularity(q_target_deg, self.universal_limit) < 0:
            risk = max(risk, 1.0)
        speed = max(self.speed_min, 1.0 - (1.0 - self.speed_min) * risk)

        if dist <= self.stop_m or code < 0 and dist < self.warn_m * 0.5:
            return SafetyResult(
                None, False, risk, speed, STATUS_SINGULARITY,
                f"hard_singularity code={code} dist={dist:.4f}")
        if risk > 0.0:
            return SafetyResult(
                list(q_target_deg), True, risk, speed, STATUS_RISK,
                f"risk_zone risk={risk:.3f} speed={speed:.2f} code={code}")
        return SafetyResult(
            list(q_target_deg), True, risk, speed, STATUS_NORMAL,
            f"ok resid_pos={resid_pos:.4f} resid_rot={resid_rot:.4f} code={code}")

    def _hold(self, risk, reason):
        return SafetyResult(None, False, risk, 0.0, STATUS_HOLD, reason)

    def _risk_from_distance(self, shoulder_dist_m):
        if shoulder_dist_m >= self.warn_m:
            return 0.0
        if shoulder_dist_m <= self.stop_m:
            return 1.0
        return (self.warn_m - shoulder_dist_m) / (self.warn_m - self.stop_m)
