"""Model command and final CANFD dispatch gates, without ROS or hardware."""

import importlib.util
from pathlib import Path
import sys
import threading
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from arm_model_control.model_commands import JOINT_NAMES, ModelCommandGate


def stub(name, **fields):
    module = ModuleType(name)
    module.__dict__.update(fields)
    return module


class FakeNode:
    pass


stubs = {
    "rclpy": stub("rclpy"),
    "rclpy.node": stub("rclpy.node", Node=FakeNode),
    "rclpy.executors": stub("rclpy.executors", SingleThreadedExecutor=object),
    "sensor_msgs.msg": stub("sensor_msgs.msg", JointState=object),
}
spec = importlib.util.spec_from_file_location(
    "model_node_under_test", Path(__file__).parents[1] / "arm_model_control/model_node.py")
module = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, stubs):
    spec.loader.exec_module(module)


class ModelNodeTest(unittest.TestCase):
    def setUp(self):
        self.now_ns = 100_000_000_000
        self.now_mono = 10.0
        clock_patch = patch.object(module.time, "monotonic", side_effect=lambda: self.now_mono)
        clock_patch.start()
        self.addCleanup(clock_patch.stop)
        node = self.node = object.__new__(module.ModelArmNode)
        node._lock = threading.Lock()
        node.gates = {side: ModelCommandGate([-180] * 6, [180] * 6)
                      for side in module.SIDES}
        node.mode = {side: module.OFF for side in module.SIDES}
        node.target = {side: None for side in module.SIDES}
        node.failures = {side: 0 for side in module.SIDES}
        node.faulted = {side: False for side in module.SIDES}
        node.dry_run = False
        node.smoothers = {side: Mock() for side in module.SIDES}
        for smoother in node.smoothers.values():
            smoother.last.return_value = [0.0] * 6
        node.controller = Mock()
        node.controller.get_joints.return_value = [0.0] * 6
        node.controller.send_both_joints.side_effect = lambda q: {side: 0 for side in q}
        node.kin = Mock()
        node.kin.fk.return_value = [0.2, 0.1, 0.3, 1.0, 0.0, 0.0, 0.0]
        node.safety = Mock()
        node.safety.validate.side_effect = lambda q, *_: SimpleNamespace(
            q_target_deg=q, speed_scale=0.5, reason="ok")
        node.get_logger = Mock(return_value=Mock())
        node.get_clock = lambda: SimpleNamespace(
            now=lambda: SimpleNamespace(nanoseconds=self.now_ns))
        node._p = lambda key: {"max_send_failures": 20}[key]

    def command(self, last=0.0):
        self.now_ns += 10_000_000
        self.now_mono += 0.01
        return SimpleNamespace(
            header=SimpleNamespace(stamp=SimpleNamespace(
                sec=self.now_ns // 1_000_000_000,
                nanosec=self.now_ns % 1_000_000_000)),
            name=list(JOINT_NAMES), position=[0.01] * 6 + [last])

    def test_first_fresh_target_arms_without_separate_topic(self):
        self.node._on_command("left", self.command())
        self.assertEqual(self.node.mode["left"], module.FOLLOW)
        self.assertTrue(self.node.gates["left"].enabled)
        self.node.controller.get_joints.assert_called_once_with("left")
        self.node.controller.send_both_joints.assert_not_called()

    def test_valid_target_reaches_final_dispatch(self):
        self.node._on_command("left", self.command())
        self.assertEqual(self.node.mode["left"], module.FOLLOW)
        generation = self.node.gates["left"].generation
        self.node._send({"left": [0.0] * 6}, {"left": generation})
        self.node.controller.send_both_joints.assert_called_once_with({"left": [0.0] * 6})

    def test_nonzero_padding_disables_side(self):
        self.node._on_command("left", self.command(0.01))
        self.assertFalse(self.node.gates["left"].enabled)
        self.node.controller.send_both_joints.assert_not_called()

    def test_disabled_generation_cannot_dispatch_old_target(self):
        self.node._on_command("left", self.command())
        old = self.node.gates["left"].generation
        self.node._stop_locked("left")
        self.node._send({"left": [0.0] * 6}, {"left": old})
        self.node.controller.send_both_joints.assert_not_called()

    def test_stale_first_target_does_not_read_hardware(self):
        self.now_ns += 1_000_000_000
        self.node._on_command("left", SimpleNamespace(
            header=SimpleNamespace(stamp=SimpleNamespace(sec=100, nanosec=0)),
            name=list(JOINT_NAMES), position=[0.0] * 7))
        self.node.controller.get_joints.assert_not_called()
        self.node.controller.send_both_joints.assert_not_called()

    def test_hardware_fault_latch_blocks_new_targets(self):
        self.node.faulted["left"] = True
        self.node._on_command("left", self.command())
        self.node.controller.get_joints.assert_not_called()
        self.node.controller.send_both_joints.assert_not_called()


if __name__ == "__main__":
    unittest.main()
