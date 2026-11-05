"""由 URDF 提取关节位置/速度限制与工作空间包络，并导出 Ruckig 运动学限值。

只依赖 numpy 与标准库（不需要 SDK / 真机），可单独测试。
"""

import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import numpy as np


@dataclass
class UrdfJoint:
    name: str
    xyz: tuple
    rpy: tuple
    axis: tuple
    lower: float      # rad
    upper: float      # rad
    velocity: float   # rad/s


@dataclass
class JointLimits:
    jmin_deg: list
    jmax_deg: list
    vel_deg: list     # °/s（URDF velocity）


@dataclass
class Workspace:
    r_max: float          # 基座原点到末端的最大距离(m)
    horizontal_max: float
    z_min: float
    z_max: float
    samples: int


def _floats(text, n, default):
    try:
        v = tuple(float(t) for t in (text or "").split())
        return v if len(v) == n else default
    except ValueError:
        return default


def parse_urdf_joints(urdf_path, dof=6):
    """按 joint1..jointN 顺序返回 [UrdfJoint]；失败返回 None。"""
    root = ET.parse(urdf_path).getroot()
    found = {}
    for joint in root.iter("joint"):
        name = (joint.get("name") or "").strip()
        if not name.startswith("joint") or not name[5:].isdigit():
            continue
        lim = joint.find("limit")
        if lim is None:
            continue
        origin = joint.find("origin")
        axis = joint.find("axis")
        try:
            found[int(name[5:])] = UrdfJoint(
                name=name,
                xyz=_floats(origin.get("xyz") if origin is not None else None, 3, (0.0,) * 3),
                rpy=_floats(origin.get("rpy") if origin is not None else None, 3, (0.0,) * 3),
                axis=_floats(axis.get("xyz") if axis is not None else None, 3, (0.0, 0.0, 1.0)),
                lower=float(lim.get("lower")),
                upper=float(lim.get("upper")),
                velocity=float(lim.get("velocity", "0") or 0.0),
            )
        except (TypeError, ValueError):
            continue
    if any(i + 1 not in found for i in range(dof)):
        return None
    return [found[i + 1] for i in range(dof)]


def load_joint_limits(urdf_path, dof=6):
    joints = parse_urdf_joints(urdf_path, dof)
    if joints is None:
        return None
    return JointLimits(
        jmin_deg=[math.degrees(j.lower) for j in joints],
        jmax_deg=[math.degrees(j.upper) for j in joints],
        vel_deg=[math.degrees(j.velocity) for j in joints],
    )


def _rpy_matrix(r, p, y):
    cr, sr, cp, sp, cy, sy = (math.cos(r), math.sin(r), math.cos(p),
                              math.sin(p), math.cos(y), math.sin(y))
    return np.array([
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr]])


def _axis_angle_matrix(axis, angle):
    a = np.asarray(axis, dtype=float)
    a = a / np.linalg.norm(a)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(angle) * K + (1 - math.cos(angle)) * (K @ K)


def urdf_fk(joints, q_rad):
    """URDF 正运动学，返回末端(joint6 坐标系原点)在基座系位置 (3,)。"""
    T = np.eye(4)
    for j, q in zip(joints, q_rad):
        Tj = np.eye(4)
        Tj[:3, :3] = _rpy_matrix(*j.rpy) @ _axis_angle_matrix(j.axis, q)
        Tj[:3, 3] = j.xyz
        T = T @ Tj
    return T[:3, 3]


def compute_workspace(joints, jmin_deg=None, jmax_deg=None, samples=4000, seed=0):
    """在关节限位内均匀采样 FK，得到可达包络统计。"""
    rng = np.random.default_rng(seed)
    lo = np.array([math.radians(v) for v in jmin_deg]) if jmin_deg else \
        np.array([j.lower for j in joints])
    hi = np.array([math.radians(v) for v in jmax_deg]) if jmax_deg else \
        np.array([j.upper for j in joints])
    pts = np.array([urdf_fk(joints, rng.uniform(lo, hi)) for _ in range(samples)])
    r = np.linalg.norm(pts, axis=1)
    return Workspace(
        r_max=float(r.max()),
        horizontal_max=float(np.hypot(pts[:, 0], pts[:, 1]).max()),
        z_min=float(pts[:, 2].min()),
        z_max=float(pts[:, 2].max()),
        samples=samples,
    )


def ruckig_limits(vel_deg, vel_scale=0.5, acc_factor=3.0, jerk_factor=5.0):
    """由 URDF 速度(°/s)导出 Ruckig 的 (vel, acc, jerk)。

    vel = URDF·vel_scale；acc = vel·acc_factor (°/s²)；jerk = acc·jerk_factor (°/s³)。
    """
    vel = [float(v) * float(vel_scale) for v in vel_deg]
    acc = [v * float(acc_factor) for v in vel]
    jerk = [a * float(jerk_factor) for a in acc]
    return vel, acc, jerk
