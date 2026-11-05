"""RM65 joint target smoothing with Ruckig limits."""

import math
import threading
from arm_model_control.math_utils import angle_diff_deg


class JointSmoother:
    """关节目标时间最优平滑（Ruckig，速度/加速度/加加速度限值来自 URDF）。

    - 目标先夹到关节限位内，输出再夹一次；
    - speed_scale 同比缩放速度/加速度/加加速度（奇异/限位降速）；
    - reset(real_joints) 以真实关节重置，速度/加速度清零；
    - update 返回错误码时保持上一位置并清零速度，不回退到跳变的 EMA；
    - Ruckig 不可用时退化为阻尼 EMA + 单步钳制 max_step_rad。
    """

    def __init__(self, dof=6, dt_sec=0.01,
                 max_step_rad=0.08,
                 max_vel_deg=(80, 80, 80, 100, 100, 120),
                 max_acc_deg=(240, 240, 240, 300, 300, 360),
                 max_jerk_deg=(1200, 1200, 1200, 1600, 1600, 2000),
                 ema_alpha=0.4,
                 jmin_deg=None, jmax_deg=None, limit_margin_deg=0.5):
        self.dof = int(dof)
        self.dt_sec = float(dt_sec)
        self.max_step_deg = math.degrees(float(max_step_rad))
        self._lock = threading.Lock()
        self._last = None
        self._alpha = float(ema_alpha)
        self._base_limits = tuple([float(v) for v in lim[: self.dof]]
                                  for lim in (max_vel_deg, max_acc_deg, max_jerk_deg))
        self._scale = 1.0
        self._jmin = ([float(v) + limit_margin_deg for v in jmin_deg[: self.dof]]
                      if jmin_deg else None)
        self._jmax = ([float(v) - limit_margin_deg for v in jmax_deg[: self.dof]]
                      if jmax_deg else None)
        # 量程 ≥ 360° 的关节（如 RM65 的 J6：±359.8）存在 ±360° 卷绕等值解：
        # IK 返回的等值解与当前角相差整 360°，最短路径差为 0（安全门因此放行），
        # 但直接下发给 Ruckig 会被规划成整圈旋转 —— 即旋转时的大幅度翻转。
        self._wrap_joints = [False] * self.dof
        if jmin_deg and jmax_deg:
            n = min(self.dof, len(jmin_deg), len(jmax_deg))
            for i in range(n):
                self._wrap_joints[i] = (
                    abs(float(jmax_deg[i]) - float(jmin_deg[i])) >= 360.0)
        self.error_count = 0
        self.last_result = None
        self._ruckig = None
        try:
            from ruckig import Ruckig, InputParameter, OutputParameter  # noqa: F401
            self._ruckig = self._init_ruckig()
        except Exception:
            self._ruckig = None

    @staticmethod
    def _apply_ruckig_limits(otg, inp, dof, limits):
        """设置速度/加速度/加加速度上限。

        ruckig>=0.10 把上限放在 InputParameter，旧版(<0.10) 放在 Ruckig
        实例上；两者兼容设置。
        """
        max_vel, max_acc, max_jerk = limits
        for name, vals in (("max_velocity", max_vel),
                           ("max_acceleration", max_acc),
                           ("max_jerk", max_jerk)):
            v = list(vals[: dof])
            if hasattr(otg, name):
                setattr(otg, name, v)
            if hasattr(inp, name):
                setattr(inp, name, v)

    def _scaled_limits(self):
        k = self._scale
        return tuple([v * k for v in lim] for lim in self._base_limits)

    def _init_ruckig(self):
        from ruckig import Ruckig, InputParameter, OutputParameter
        otg = Ruckig(self.dof, self.dt_sec)
        inp = InputParameter(self.dof)
        self._apply_ruckig_limits(otg, inp, self.dof, self._scaled_limits())
        return {"otg": otg, "inp": inp, "out": OutputParameter(self.dof)}

    @property
    def has_ruckig(self):
        return self._ruckig is not None

    def set_speed_scale(self, scale):
        """速度缩放 ∈ [0.05, 1]；变化时重写上限。"""
        scale = max(0.05, min(1.0, float(scale)))
        with self._lock:
            if abs(scale - self._scale) < 1e-3:
                return
            self._scale = scale
            if self._ruckig is not None:
                self._apply_ruckig_limits(
                    self._ruckig["otg"], self._ruckig["inp"],
                    self.dof, self._scaled_limits())

    def _clamp_limits(self, q):
        if self._jmin is None:
            return q
        return [min(max(q[i], self._jmin[i]), self._jmax[i]) for i in range(self.dof)]

    def _nearest_equivalent(self, target, ref):
        """把 target 归一到相对 ref 的最短路径等价角（仅对可整圈关节生效）。

        J6 在 -273° 与 +87° 是同一末端姿态。IK/安全门按最短路径把二者视作
        距离 0，若不归一，Ruckig 会收到相差整 360° 的原始目标并执行整圈旋转。
        """
        if not any(self._wrap_joints):
            return list(target)
        return [(ref[i] + angle_diff_deg(target[i], ref[i]))
                if self._wrap_joints[i] else target[i]
                for i in range(self.dof)]

    def reset(self, current_joints_deg):
        """以当前真实关节重置（速度/加速度清零）。"""
        with self._lock:
            self._last = self._clamp_limits(
                [float(v) for v in current_joints_deg[: self.dof]])
            if self._ruckig is not None:
                self._ruckig["inp"] = self._ruckig["inp"].__class__(self.dof)
                # 重建 InputParameter 后需重新写入上限（ruckig>=0.10 上限在 inp 上）
                self._apply_ruckig_limits(
                    self._ruckig["otg"], self._ruckig["inp"],
                    self.dof, self._scaled_limits())
                # ruckig>=0.10(nanobind) 逐元素赋值不生效，必须整列表赋值
                self._ruckig["inp"].target_position = list(self._last)
                self._ruckig["inp"].current_position = list(self._last)

    def smooth(self, target_joints_deg):
        """返回平滑后的关节目标(°)。"""
        raw = [float(v) for v in target_joints_deg[: self.dof]]
        with self._lock:
            if self._last is None:
                target = self._clamp_limits(raw)
                self._last = target[:]
                return list(target)
            # 先按最短路径归一（整圈关节），再夹限位——顺序不可颠倒，
            # 否则归一会再次越限。
            target = self._clamp_limits(self._nearest_equivalent(raw, self._last))
            if self._ruckig is not None:
                return self._smooth_ruckig(target)
            return self._smooth_ema(target)

    def hold(self):
        """目标=当前位置：按限值减速停止，返回平滑输出；未初始化返回 None。"""
        with self._lock:
            last = list(self._last) if self._last else None
        return self.smooth(last) if last else None

    def _smooth_ruckig(self, target):
        from ruckig import Result
        inp = self._ruckig["inp"]
        out = self._ruckig["out"]
        # ruckig>=0.10(nanobind) 逐元素赋值不生效，必须整列表赋值
        inp.target_position = list(target)
        inp.target_velocity = [0.0] * self.dof
        inp.target_acceleration = [0.0] * self.dof
        try:
            result = self._ruckig["otg"].update(inp, out)
        except Exception:
            result = None
        self.last_result = result
        if result not in (Result.Working, Result.Finished):
            # 规划失败：保持当前位置并清零速度/加速度，下个周期重新规划
            self.error_count += 1
            inp.current_position = list(self._last)
            inp.current_velocity = [0.0] * self.dof
            inp.current_acceleration = [0.0] * self.dof
            return list(self._last)
        res = self._clamp_limits([float(out.new_position[i]) for i in range(self.dof)])
        out.pass_to_input(inp)
        self._last = res
        return list(res)

    def velocity(self):
        """当前 Ruckig 关节速度(°/s)；无 Ruckig 返回 None。"""
        with self._lock:
            if self._ruckig is None:
                return None
            return [float(v) for v in self._ruckig["inp"].current_velocity]

    def at_rest(self, tol_deg_s=0.5):
        vel = self.velocity()
        return vel is None or all(abs(v) < tol_deg_s for v in vel)

    def _smooth_ema(self, target):
        a = self._alpha
        # 单步钳制 + EMA
        last = self._last
        clamped = []
        for i in range(self.dof):
            d = angle_diff_deg(target[i], last[i])
            d = clamp_scalar(d, -self.max_step_deg, self.max_step_deg)
            clamped.append(last[i] + d)
        res = [(1.0 - a) * last[i] + a * clamped[i] for i in range(self.dof)]
        self._last = res
        return res

    def last(self):
        with self._lock:
            return list(self._last) if self._last else None


def clamp_scalar(value, minimum, maximum):
    return max(minimum, min(maximum, value))
