"""Model joint-command contract, independent of ROS and the hardware SDK.

The recording interface contains seven slots, while RM65 has six joints. The
seventh slot is checked as padding and is never treated as a physical joint.
Callers serialize this gate with their control-loop lock.
"""

import math


JOINT_NAMES = tuple(f"joint{i}" for i in range(1, 8))


class ModelCommandError(ValueError):
    """A command cannot be executed under the active control session."""


class ModelCommandGate:
    def __init__(self, jmin_deg, jmax_deg, *, timeout_sec=0.3,
                 max_delta_rad=0.2, padding_tolerance_rad=0.0001,
                 future_tolerance_sec=0.02, first_command_timeout_sec=10.0):
        self.jmin = tuple(float(v) for v in jmin_deg)
        self.jmax = tuple(float(v) for v in jmax_deg)
        if len(self.jmin) != 6 or len(self.jmax) != 6:
            raise ValueError("model arm commands require the six-joint RM65")
        if any(not math.isfinite(lo) or not math.isfinite(hi) or lo >= hi
               for lo, hi in zip(self.jmin, self.jmax)):
            raise ValueError("invalid RM65 joint limits")
        values = (timeout_sec, max_delta_rad, padding_tolerance_rad,
                  future_tolerance_sec, first_command_timeout_sec)
        if any(not math.isfinite(float(v)) or float(v) <= 0 for v in values):
            raise ValueError("model command tolerances must be finite and positive")
        self.timeout_sec = float(timeout_sec)
        self.first_command_timeout_sec = float(first_command_timeout_sec)
        self.max_delta_deg = math.degrees(float(max_delta_rad))
        self.padding_tolerance_rad = float(padding_tolerance_rad)
        self.future_tolerance_ns = int(float(future_tolerance_sec) * 1e9)
        self.generation = 0
        self.enabled = False
        self.enabled_after_ns = 0
        self.last_stamp_ns = 0
        self.last_receive_monotonic = None
        self.enabled_monotonic = 0.0

    def enable(self, now_ns, now_monotonic):
        self.generation += 1
        self.enabled = True
        self.enabled_after_ns = int(now_ns)
        self.last_stamp_ns = int(now_ns)
        self.last_receive_monotonic = None
        self.enabled_monotonic = float(now_monotonic)

    def disable(self):
        self.generation += 1
        self.enabled = False
        self.last_receive_monotonic = None

    def expired(self, now_monotonic):
        if not self.enabled:
            return False
        if self.last_receive_monotonic is None:
            return now_monotonic - self.enabled_monotonic > self.first_command_timeout_sec
        return now_monotonic - self.last_receive_monotonic > self.timeout_sec

    def accept(self, names, positions, stamp_ns, *, now_ns, now_monotonic,
               current_deg):
        """Validate a stamped seven-slot radian target; return six degrees.

        Successful input advances the sequence and watchdog. The caller must
        still apply its geometric safety gate before dispatching the target.
        A safety failure must disable this gate; it must not refresh a target.
        """
        if not self.enabled:
            raise ModelCommandError("model input is disabled; fresh command initialization required")
        if self.expired(now_monotonic):
            raise ModelCommandError("command stream timed out; stop before a new command session")
        stamp_ns = int(stamp_ns)
        now_ns = int(now_ns)
        if stamp_ns <= self.last_stamp_ns or stamp_ns <= 0:
            raise ModelCommandError("command predates enable or is duplicated/out of order")
        if now_ns - stamp_ns > int(self.timeout_sec * 1e9):
            raise ModelCommandError("command timestamp is stale")
        if stamp_ns - now_ns > self.future_tolerance_ns:
            raise ModelCommandError("command timestamp is in the future")
        if len(names) != 7 or len(set(names)) != 7 or set(names) != set(JOINT_NAMES):
            raise ModelCommandError("name must contain joint1 through joint7 exactly once")
        if len(positions) != 7:
            raise ModelCommandError("position must contain seven recording-interface slots")
        by_name = dict(zip(names, positions))
        try:
            q_rad = [float(by_name[name]) for name in JOINT_NAMES]
            current = [float(v) for v in current_deg]
        except (ValueError, TypeError, OverflowError) as exc:
            raise ModelCommandError("joint positions must be numeric") from exc
        if len(current) != 6 or not all(math.isfinite(v) for v in q_rad + current):
            raise ModelCommandError("target and current joint positions must be finite")
        if abs(q_rad[6]) > self.padding_tolerance_rad:
            raise ModelCommandError("joint7 is RM65 padding and must be approximately zero")
        q_deg = [math.degrees(v) for v in q_rad[:6]]
        for i, (q, cur, lo, hi) in enumerate(zip(q_deg, current, self.jmin, self.jmax)):
            if q < lo or q > hi:
                raise ModelCommandError(f"joint{i + 1} target is outside limits")
            # Absolute positions: do not turn a large multi-turn jump into a
            # small error by wrapping it modulo 360 degrees.
            if abs(q - cur) > self.max_delta_deg:
                raise ModelCommandError(f"joint{i + 1} target jump exceeds model_max_delta_rad")
        self.last_stamp_ns = stamp_ns
        self.last_receive_monotonic = float(now_monotonic)
        return q_deg
