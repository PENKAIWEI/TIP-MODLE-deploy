"""Angle and quaternion operations used by RM65 safety validation."""

import math

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def wrap_angle_deg(deg):
    return (float(deg) + 180.0) % 360.0 - 180.0

def angle_diff_deg(a_deg, b_deg):
    return wrap_angle_deg(float(a_deg) - float(b_deg))

def quat_normalize(quat):
    norm = math.sqrt(sum(float(v) * float(v) for v in quat))
    return tuple(float(v) / norm for v in quat) if norm >= 1e-9 else (0.0, 0.0, 0.0, 1.0)

def quat_inverse(quat):
    x, y, z, w = quat_normalize(quat)
    return (-x, -y, -z, w)

def quat_multiply(lhs, rhs):
    lx, ly, lz, lw = lhs
    rx, ry, rz, rw = rhs
    return (lw*rx+lx*rw+ly*rz-lz*ry, lw*ry-lx*rz+ly*rw+lz*rx,
            lw*rz+lx*ry-ly*rx+lz*rw, lw*rw-lx*rx-ly*ry-lz*rz)

def quat_to_rotvec(quat):
    x, y, z, w = quat_normalize(quat)
    if w < 0.0:
        x, y, z, w = -x, -y, -z, -w
    angle = 2.0 * math.acos(clamp(w, -1.0, 1.0))
    s = math.sqrt(max(0.0, 1.0 - w*w))
    return (x*2.0, y*2.0, z*2.0) if s < 1e-9 else (x/s*angle, y/s*angle, z/s*angle)
