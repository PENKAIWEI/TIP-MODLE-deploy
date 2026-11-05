"""Model-only dual RM65 controller with validated direct CANFD commands."""

import math
import threading
import time
from pathlib import Path

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState

from arm_model_control.arm_controller import SIDES, DualArmController
from arm_model_control.coordinate_align import SdkKinematics
from arm_model_control.filter_smooth import JointSmoother
from arm_model_control.limits import compute_workspace, parse_urdf_joints, ruckig_limits
from arm_model_control.model_commands import ModelCommandError, ModelCommandGate
from arm_model_control.safety import SafetyGate

OFF, FOLLOW, STOPPING = "off", "follow", "stopping"
PARAMS = {
    "left_arm_ip": "192.168.1.19",
    "right_arm_ip": "192.168.1.18",
    "arm_port": 8080,
    "arm_level": 3,
    "sdk_src": "",
    "urdf_file": "",
    "dry_run": True,
    "dry_run_arm_ref_joints": [0.0, 40.0, 45.0, 0.0, -30.0, 0.0],
    "control_hz": 200.0,
    "target_timeout_sec": 0.3,
    "model_max_delta_rad": 0.2,
    "model_padding_tolerance_rad": 0.0001,
    "max_send_failures": 20,
    "max_step_rad": 0.08,
    "max_j4_step_deg": 40.0,
    "workspace_radius": 0.0,
    "workspace_margin": 0.78,
    "ruckig_vel_scale": 0.5,
    "ruckig_acc_factor": 3.0,
    "ruckig_jerk_factor": 5.0,
    "fk_pos_tol": 0.008,
    "fk_rot_tol": 0.05,
    "singularity_warn_distance_m": 0.05,
    "singularity_stop_distance_m": 0.02,
    "singularity_universal_value_limit": 0.01,
    "singularity_speed_min_scale": 0.2,
    "singularity_limit_qe_deg": 10.0,
    "singularity_limit_qw_deg": 10.0,
    "singularity_limit_d_m": 0.05,
    "udp_push_cycle_ms": 2,
}


class ModelArmNode(Node):
    def __init__(self):
        super().__init__("arm_model_control_node")
        for name, default in PARAMS.items():
            self.declare_parameter(name, default)
        self._p = lambda name: self.get_parameter(name).value
        p = self._p
        self._require_bundled_dependencies(str(p("sdk_src")))
        self.dry_run = bool(p("dry_run"))
        self._lock = threading.Lock()
        self._running = False
        self._observer = None
        self.controller = None

        self.kin = SdkKinematics(
            sdk_src=str(p("sdk_src")) or None, arm_model_name="RM_65",
            urdf_file=str(p("urdf_file")) or None, logger=self.get_logger())
        if self.kin.dof != 6:
            raise RuntimeError("model control requires six-joint RM65")
        self.kin.set_singularity_thresholds(
            limit_qe_deg=float(p("singularity_limit_qe_deg")),
            limit_qw_deg=float(p("singularity_limit_qw_deg")),
            limit_d_m=float(p("singularity_limit_d_m")))
        workspace_r, workspace_sphere = self._workspace()
        vel, acc, jerk = ruckig_limits(
            self.kin.jspeed, float(p("ruckig_vel_scale")),
            float(p("ruckig_acc_factor")), float(p("ruckig_jerk_factor")))
        hz = float(p("control_hz"))
        if not math.isfinite(hz) or hz <= 0:
            raise ValueError("control_hz must be positive")
        self.smoothers = {
            side: JointSmoother(
                dof=6, dt_sec=1.0 / hz,
                max_step_rad=float(p("max_step_rad")),
                max_vel_deg=vel, max_acc_deg=acc, max_jerk_deg=jerk,
                jmin_deg=self.kin.jmin, jmax_deg=self.kin.jmax)
            for side in SIDES
        }
        if not self.dry_run and not all(s.has_ruckig for s in self.smoothers.values()):
            raise RuntimeError("hardware model control requires Ruckig")
        self.gates = {
            side: ModelCommandGate(
                self.kin.jmin, self.kin.jmax,
                timeout_sec=float(p("target_timeout_sec")),
                max_delta_rad=float(p("model_max_delta_rad")),
                padding_tolerance_rad=float(p("model_padding_tolerance_rad")))
            for side in SIDES
        }
        self.safety = SafetyGate(
            self.kin, max_step_rad=float(p("max_step_rad")),
            fk_pos_tol_m=float(p("fk_pos_tol")),
            fk_rot_tol_rad=float(p("fk_rot_tol")),
            workspace_r_m=workspace_r, workspace_sphere_m=workspace_sphere,
            singularity_warn_m=float(p("singularity_warn_distance_m")),
            singularity_stop_m=float(p("singularity_stop_distance_m")),
            speed_min_scale=float(p("singularity_speed_min_scale")),
            universal_value_limit=float(p("singularity_universal_value_limit")),
            max_j4_step_deg=float(p("max_j4_step_deg")))
        self.mode = {side: OFF for side in SIDES}
        self.target = {side: None for side in SIDES}
        self.failures = {side: 0 for side in SIDES}
        self.faulted = {side: False for side in SIDES}

        if not self.dry_run:
            self._connect_hardware()
        for side in SIDES:
            self.create_subscription(
                JointState, f"/observation/{side}_arm/joint_cmd",
                lambda msg, s=side: self._on_command(s, msg), 1)
        self._running = True
        self._thread = threading.Thread(target=self._control_loop, daemon=True)
        self._thread.start()

    @staticmethod
    def _require_bundled_dependencies(sdk_src):
        import numpy
        import ruckig

        sdk_root = Path(sdk_src).resolve()
        if (sdk_root.name, sdk_root.parent.name, sdk_root.parent.parent.name) != (
                "src", "realman_sdk", "third_party"):
            raise RuntimeError("sdk_src must point to third_party/realman_sdk/src")
        third_party = sdk_root.parent.parent
        for name, module in (("numpy", numpy), ("ruckig", ruckig)):
            if not Path(module.__file__).resolve().is_relative_to(third_party):
                raise RuntimeError(f"{name} must load from third_party")

    def _workspace(self):
        p = self._p
        configured = float(p("workspace_radius"))
        r_max = None
        if self.kin.urdf_path:
            joints = parse_urdf_joints(self.kin.urdf_path, 6)
            if joints:
                r_max = compute_workspace(joints, self.kin.jmin, self.kin.jmax).r_max
        if configured > 0:
            return configured, max(configured, r_max or 0.95)
        if r_max is None:
            raise RuntimeError("RM65 URDF workspace could not be calculated")
        return r_max * float(p("workspace_margin")), r_max

    def _connect_hardware(self):
        p = self._p
        self.controller = DualArmController(
            left_ip=p("left_arm_ip"), right_ip=p("right_arm_ip"),
            port=int(p("arm_port")), level=int(p("arm_level")),
            sdk_src=str(p("sdk_src")) or None,
            udp_push_cycle_ms=int(p("udp_push_cycle_ms")), logger=self.get_logger())
        try:
            self.controller.connect()
            if any(int(getattr(robot, "arm_dof", 0)) != 6
                   for robot in self.controller._robots.values()):
                raise RuntimeError("connected hardware is not six-joint RM65")
            from arm_model_control.arm_observer import DualArmUdpObserver
            self._observer = DualArmUdpObserver(
                self.controller.ips["left"], self.controller.ips["right"],
                push_cycle_ms=int(p("udp_push_cycle_ms")))
            robots = self.controller._robots
            self._observer.start(robots["left"], [robots["left"], robots["right"]])
            if not self._observer._ros_pubs:
                raise RuntimeError("arm feedback ROS publishers did not start")
        except Exception:
            if self._observer is not None:
                self._observer.stop()
            self.controller.disconnect()
            raise

    def _stop_locked(self, side):
        self.gates[side].disable()
        self.target[side] = None
        if self.mode[side] != OFF:
            self.mode[side] = STOPPING

    def _arm_from_first_command(self, side, stamp_ns):
        """Initialize from current feedback without publishing a movement."""
        gate = self.gates[side]
        now_ns = self.get_clock().now().nanoseconds
        if stamp_ns <= 0 or stamp_ns <= gate.last_stamp_ns:
            raise ModelCommandError("first command timestamp is repeated or out of order")
        if now_ns - stamp_ns > int(gate.timeout_sec * 1e9):
            raise ModelCommandError("first command timestamp is stale")
        if stamp_ns - now_ns > gate.future_tolerance_ns:
            raise ModelCommandError("first command timestamp is in the future")
        current = (list(self._p("dry_run_arm_ref_joints"))[:6]
                   if self.dry_run else self.controller.get_joints(side))
        if len(current) != 6 or not all(math.isfinite(v) for v in current):
            raise ModelCommandError("invalid six-joint feedback")
        with self._lock:
            if self.faulted[side] or self.mode[side] != OFF or gate.enabled:
                return
            self.smoothers[side].reset(current)
            self.target[side] = None
            self.failures[side] = 0
            # The command itself is the activation event. Keep the previous
            # timestamp watermark check above, then allow this fresh stamp.
            gate.enable(stamp_ns - 1, time.monotonic())

    def _on_command(self, side, msg):
        try:
            if not 0 <= msg.header.stamp.nanosec < 1_000_000_000:
                raise ModelCommandError("invalid nanosecond timestamp")
            stamp_ns = int(msg.header.stamp.sec) * 1_000_000_000 + int(msg.header.stamp.nanosec)
            with self._lock:
                gate = self.gates[side]
                if self.faulted[side] or self.mode[side] == STOPPING:
                    return
                first = not gate.enabled
            if first:
                self._arm_from_first_command(side, stamp_ns)
            with self._lock:
                if not gate.enabled or self.faulted[side]:
                    return
                generation = gate.generation
                current = self.smoothers[side].last()
                q = gate.accept(
                    msg.name, msg.position, stamp_ns,
                    now_ns=self.get_clock().now().nanoseconds,
                    now_monotonic=time.monotonic(), current_deg=current or [])
            fk = self.kin.fk(q, flag=0)
            result = self.safety.validate(
                q, current, fk[:3], (fk[4], fk[5], fk[6], fk[3]), 0.0, 0)
            if result.q_target_deg is None:
                raise ModelCommandError(f"safety gate: {result.reason}")
            with self._lock:
                if generation != gate.generation or not gate.enabled:
                    return
                if gate.expired(time.monotonic()):
                    raise ModelCommandError("command expired during validation")
                self.mode[side] = FOLLOW
                self.target[side] = (list(result.q_target_deg),
                                     float(result.speed_scale), gate.last_receive_monotonic)
        except Exception as exc:
            with self._lock:
                self._stop_locked(side)
            self.get_logger().warning(f"{side}: target rejected and disabled: {exc}")

    def _control_loop(self):
        dt = 1.0 / float(self._p("control_hz"))
        timeout = float(self._p("target_timeout_sec"))
        next_tick = time.perf_counter()
        while self._running:
            try:
                with self._lock:
                    for side, gate in self.gates.items():
                        if gate.expired(time.monotonic()):
                            self._stop_locked(side)
                    generations = {side: gate.generation for side, gate in self.gates.items()}
                    modes = dict(self.mode)
                    targets = dict(self.target)
                now = time.monotonic()
                commands = {}
                for side in SIDES:
                    if modes[side] == OFF:
                        continue
                    smoother = self.smoothers[side]
                    target = targets[side]
                    if modes[side] == FOLLOW and target and now - target[2] <= timeout:
                        smoother.set_speed_scale(target[1])
                        output = smoother.smooth(target[0])
                    else:
                        smoother.set_speed_scale(1.0)
                        output = smoother.hold()
                        if modes[side] == STOPPING and smoother.at_rest():
                            with self._lock:
                                if self.mode[side] == STOPPING:
                                    self.mode[side] = OFF
                    if output is not None:
                        commands[side] = output
                if commands:
                    self._send(commands, generations)
            except Exception as exc:
                self.get_logger().error(f"control loop error: {exc!r}")
            next_tick += dt
            delay = next_tick - time.perf_counter()
            if delay > 0:
                time.sleep(delay)
            elif delay < -5 * dt:
                next_tick = time.perf_counter()

    def _send(self, commands, generations):
        # The lock spans the final SDK call so an old session cannot dispatch.
        with self._lock:
            for side in commands:
                if self.gates[side].expired(time.monotonic()):
                    self._stop_locked(side)
            valid = {side: q for side, q in commands.items()
                     if generations[side] == self.gates[side].generation}
            results = (self.controller.send_both_joints(valid)
                       if self.controller is not None and valid else {})
        for side, code in results.items():
            if code == 0:
                self.failures[side] = 0
                continue
            self.failures[side] += 1
            self.get_logger().warning(f"{side}: rm_movej_canfd failed: {code}")
            if self.failures[side] >= int(self._p("max_send_failures")):
                self.controller.slow_stop(side)
                with self._lock:
                    self._stop_locked(side)
                    self.mode[side] = OFF
                    self.faulted[side] = True
                self.get_logger().error(f"{side}: repeated CANFD failure; restart required")

    def destroy_node(self):
        self._running = False
        if hasattr(self, "_thread"):
            self._thread.join(timeout=1.0)
        if self._observer is not None:
            self._observer.stop()
        if self.controller is not None and self.controller.connected:
            for side in SIDES:
                if self.mode[side] != OFF:
                    self.controller.slow_stop(side)
            self.controller.disconnect()
        super().destroy_node()


def main():
    rclpy.init()
    node = ModelArmNode()
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
