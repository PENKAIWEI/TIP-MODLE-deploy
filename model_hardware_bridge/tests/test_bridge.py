"""Offline tests against TIP's real pure contracts; fake ROS, no device access."""
import copy
from dataclasses import dataclass
import enum
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time
import types
import unittest
from unittest.mock import Mock, patch

import numpy as np

# This Windows review host has Python 3.10. Only the offline test harness supplies
# the StrEnum base needed to import TIP's actual O10 constants; production still
# requires ROS Jazzy/Python 3.12. Joint names/limits/Side are never duplicated.
if not hasattr(enum, 'StrEnum'):
    class TestStrEnum(str, enum.Enum):
        __str__ = str.__str__
    enum.StrEnum = TestStrEnum

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tip_bridge.config import CONFIG, camera_bindings, load_config

DEPLOY = CONFIG['deployment_root']
sys.path.insert(0, str(DEPLOY / 'hardware/hand_ws/src/collection/o10_contracts'))
sys.path.insert(0, str(DEPLOY / 'hardware/arm_ws/arm_model_control'))
from omnihand_o10_contracts.joints import ACTIVE_JOINT_NAMES, JOINT_LIMITS
from omnihand_o10_contracts.side import Side
from arm_model_control.model_commands import ModelCommandGate
from tip_bridge import controller, sensors, stream
from tip_bridge import common
from tip_bridge.common import FPS, SHAPES, limited, project, q34, reset_pose
from tip_bridge.contracts import (ARM_NAMES, COMMAND_TOPICS, arm_limits,
                                  decode_tactile, joint_feedback, model_image,
                                  pose_vector, split_action)


def limits():
    arm = arm_limits(DEPLOY / CONFIG['arm_urdf'])
    return {side: dict(arm=arm, hand=(JOINT_LIMITS[Side(side)].lower,
                                     JOINT_LIMITS[Side(side)].upper)) for side in ('left', 'right')}


def stamp(ns):
    return types.SimpleNamespace(sec=ns//10**9, nanosec=ns % 10**9)


class JointState:
    def __init__(self):
        self.header = types.SimpleNamespace(stamp=stamp(0), frame_id='')
        self.name, self.position, self.velocity, self.effort = [], [], [], []


class FakeNow:
    last_ns = 0
    def __init__(self):
        self.nanoseconds = max(time.time_ns(), self.last_ns+1)
        type(self).last_ns = self.nanoseconds
    def to_msg(self):
        return stamp(self.nanoseconds)


class Publisher:
    def __init__(self, topic):
        self.topic, self.messages = topic, []
    def get_subscription_count(self):
        return 1
    def publish(self, msg):
        self.messages.append(msg)


class Node:
    instances = []
    def __init__(self, name):
        self.name, self.publishers, self.subscribers = name, [], {}
        self.others = {}
        self.instances.append(self)
    def get_name(self):
        return self.name
    def get_clock(self):
        return types.SimpleNamespace(now=FakeNow)
    def create_subscription(self, kind, topic, fn, qos):
        self.subscribers[topic] = fn
        return (kind, topic, qos)
    def create_publisher(self, kind, topic, qos):
        pub = Publisher(topic)
        self.publishers.append(pub)
        return pub
    def get_publishers_info_by_topic(self, topic):
        return [types.SimpleNamespace(node_name=n) for n in self.others.get(topic, ())]
    def destroy_node(self):
        pass


class Executor:
    def add_node(self, node):
        pass
    def spin(self):
        pass
    def shutdown(self, **kwargs):
        pass


def fake_ros():
    modules = {}
    definitions = {
        'rclpy': dict(init=Mock(), ok=lambda: True, shutdown=Mock()),
        'rclpy.node': dict(Node=Node),
        'rclpy.qos': dict(QoSProfile=lambda **kwargs: kwargs,
                         ReliabilityPolicy=types.SimpleNamespace(BEST_EFFORT=1)),
        'rclpy.executors': dict(SingleThreadedExecutor=Executor),
        'rclpy.signals': dict(SignalHandlerOptions=types.SimpleNamespace(NO=0)),
        'sensor_msgs.msg': dict(JointState=JointState, CompressedImage=type('CompressedImage', (), {}), Image=type('Image', (), {})),
        'geometry_msgs.msg': dict(PoseStamped=type('PoseStamped', (), {})),
        'rokoko_omnihand_msgs.msg': dict(O10ControlState=type('O10ControlState', (), {})),
    }
    for name, values in definitions.items():
        module = types.ModuleType(name)
        module.__dict__.update(values)
        modules[name] = module
    return modules


def populate(robot):
    now = time.monotonic()
    q = q34(reset_pose())
    for key, values in [('la', q[:7]), ('lh', q[7:17]), ('ra', q[17:24]), ('rh', q[24:])]:
        robot.store.rows[key].clear()
        robot.store.add(key, values, now)
    for side in ('left', 'right'):
        robot.state[side] = (now, types.SimpleNamespace(
            fault_latched=False, fault_reason_mask=0, phase=2,
            feedback_ready=True, error_monitor_ready=True, motion_enabled=True,
            target_result=0, command_time_available=True,
            last_command_sent_stamp=FakeNow().to_msg()))
    return q


class ConversionTests(unittest.TestCase):
    def test_commands_are_accepted_by_target_arm_gate_without_unit_or_name_changes(self):
        q = q34(reset_pose())
        project(q, limits())
        rows = split_action(q, ACTIVE_JOINT_NAMES)
        for index, offset in ((0, 0), (1, 17)):
            gate = ModelCommandGate(*np.rad2deg(limits()['left']['arm']))
            gate.enable(1_000_000_000, 10.)
            names, values = rows[index]
            current = np.rad2deg(q[offset:offset+6])
            result = gate.accept(names, values, 1_010_000_000, now_ns=1_010_000_000,
                                 now_monotonic=10.01, current_deg=current)
            np.testing.assert_allclose(result, current)
        self.assertEqual(rows[2][0], ACTIVE_JOINT_NAMES)
        np.testing.assert_array_equal(rows[2][1], q[7:17])
        np.testing.assert_array_equal(rows[3][1], q[24:34])
        self.assertEqual(len(rows), 4)

    def test_padding_nonfinite_and_limits_rejected(self):
        for index, value in ((6, .00011), (23, .001), (0, math.nan), (0, 100.)):
            with self.subTest(index=index, value=value):
                q = q34(reset_pose())
                q[index] = value
                with self.assertRaises(ValueError):
                    project(q, limits())

    def test_command_limits_are_strict_like_target_driver(self):
        q = q34(reset_pose())
        q[0] = limits()['left']['arm'][0][0] - 1e-6
        with self.assertRaises(ValueError):
            project(q, limits())
        project(q, limits(), feedback=True)

    def test_joint_feedback_reorders_named_arm_and_accepts_unnamed_hand(self):
        msg = JointState()
        msg.name, msg.position = list(reversed(ARM_NAMES)), [0., 6., 5., 4., 3., 2., 1.]
        np.testing.assert_array_equal(joint_feedback(msg, arm=True), [1, 2, 3, 4, 5, 6, 0])
        msg.name, msg.position = [], list(range(10))
        np.testing.assert_array_equal(joint_feedback(msg, arm=False, hand_names=ACTIVE_JOINT_NAMES), range(10))
        msg.name = ['unknown']*10
        with self.assertRaises(ValueError):
            joint_feedback(msg, arm=False, hand_names=ACTIVE_JOINT_NAMES)

    def test_pose_xyzw_to_rpy(self):
        msg = types.SimpleNamespace(pose=types.SimpleNamespace(
            position=types.SimpleNamespace(x=1., y=2., z=3.),
            orientation=types.SimpleNamespace(x=0., y=0., z=math.sqrt(.5), w=math.sqrt(.5))))
        np.testing.assert_allclose(pose_vector(msg), [1, 2, 3, 0, 0, math.pi/2], atol=1e-12)

    def test_tactile_native_layout_and_row_padding(self):
        raw = np.arange(11*14, dtype=np.uint8).reshape(11, 14)
        msg = types.SimpleNamespace(encoding='mono8', height=11, width=12, step=14, data=raw.tobytes())
        np.testing.assert_array_equal(decode_tactile(msg, 0), raw[:, :12])
        msg.data = msg.data[:-1]
        with self.assertRaises(ValueError):
            decode_tactile(msg, 0)

    def test_image_rgb_resize_padding_and_source_resolution(self):
        from PIL import Image
        data = io.BytesIO()
        Image.new('RGB', (640, 480), color=(255, 0, 0)).save(data, format='PNG')
        encoded = model_image(data.getvalue(), dict(width=640, height=480))
        with Image.open(io.BytesIO(encoded.tobytes())) as image:
            rgb = np.asarray(image)
        self.assertEqual(rgb.shape, (224, 224, 3))
        self.assertGreater(rgb[112, 112, 0], 240)
        self.assertLess(rgb[112, 112, 2], 10)
        self.assertLess(int(rgb[0].max()), 10)
        with self.assertRaises(ValueError):
            model_image(data.getvalue(), dict(width=1280, height=720))

    def test_limiter_keeps_expected_per_tick_bounds(self):
        q = q34(reset_pose())
        target = q.copy()
        target[0] += .2
        target[11] += .3
        result = limited(target, q, limits())
        self.assertAlmostEqual(result[0]-q[0], .02)
        self.assertAlmostEqual(result[11]-q[11], .025)


class StoreTests(unittest.TestCase):
    def aligned_store(self, stamps=(10., 10., 10.)):
        store = sensors.Store()
        for key, t in zip(('top', 'left_wrist', 'right_wrist'), stamps):
            store.add(key, [1, 2, 3], t, dict(frame_id=key, source_stamp_ns=int(t*1e9)))
        for key, n in [('la', 7), ('lh', 10), ('ra', 7), ('rh', 10), ('lp', 6), ('rp', 6)]:
            store.add(key, np.zeros(n), 9.99)
            store.add(key, np.ones(n), 10.01)
        return store

    def test_state46_interpolation_and_camera_metadata(self):
        store = self.aligned_store()
        with patch('tip_bridge.sensors.time.monotonic', return_value=10.05):
            images, state, t = store.snapshot()
        np.testing.assert_allclose(state, np.full(46, .5))
        self.assertEqual(set(images), {'top', 'left_wrist', 'right_wrist'})
        self.assertEqual(t, 10.)
        self.assertEqual(store.snapshot_metadata['top']['frame_id'], 'top')

    def test_missing_stale_and_unsynchronized_observations_fail(self):
        for kind in ('missing', 'stale', 'spread', 'bracket'):
            with self.subTest(kind=kind):
                store = self.aligned_store()
                if kind == 'missing':
                    store.rows['right_wrist'].clear()
                if kind == 'spread':
                    store.config = dict(CONFIG, camera_sync_tolerance_s=.01)
                    store.rows['right_wrist'].append((10.03, np.ones(3)))
                    store.rows['right_wrist'].popleft()
                if kind == 'bracket':
                    store.rows['la'].pop()
                with patch('tip_bridge.sensors.time.monotonic', return_value=10.3 if kind == 'stale' else 10.05):
                    with self.assertRaises(ValueError):
                        store.snapshot()

    def test_duplicate_frames_do_not_advance_calibration_and_reversal_fails(self):
        store = sensors.Store()
        store.add('top', [1], 10.)
        self.assertFalse(store.add('top', [2], 10.))
        self.assertEqual(store.anchors, [10.])
        with self.assertRaises(ValueError):
            store.add('top', [3], 9.)

    def test_upload_overrun_rejected_even_on_first_batch(self):
        store = sensors.Store()
        store.events.append(dict(sequence=2))
        with self.assertRaises(ValueError):
            store.after(0)


class TactileTests(unittest.TestCase):
    def test_hold_uses_last_causal_packet_without_expiry_or_future_leak(self):
        s = stream.DualStream()
        s.update(0, np.ones(SHAPES[0]), 10.)
        s.update(0, np.full(SHAPES[0], 9), 1000.)
        raw, valid, latest = s.sample([9., 10.01, 10.051, 610.])
        self.assertEqual(valid[0].tolist(), [False, True, True, True])
        np.testing.assert_array_equal(raw[0, -1, :11, :12], 1.)
        self.assertEqual(latest, 10.)
        self.assertIsNone(stream.TACTILE_STREAM_TIMEOUT_S)

    def test_invalid_latest_stays_masked(self):
        s = stream.DualStream()
        s.update(0, np.ones(SHAPES[0]), 10.)
        s.update(0, np.ones(SHAPES[0]), 10.1, valid=False)
        raw, valid, _ = s.sample([610.])
        self.assertFalse(valid[0, 0])
        self.assertEqual(raw.sum(), 0)

    def test_optional_strict_policy_masks_old_sample(self):
        s = stream.DualStream()
        s.update(0, np.ones(SHAPES[0]), 10.)
        with patch.object(stream, 'TACTILE_MAX_SAMPLE_AGE_S', .05):
            _, valid, _ = s.sample([10.049, 10.051])
        self.assertEqual(valid[0].tolist(), [True, False])

    def test_client_long_bilateral_pause_survives_queue_eviction_and_recovers(self):
        robot = sensors.IO.__new__(sensors.IO)
        robot.config, robot.store = CONFIG, sensors.Store()
        with patch('tip_bridge.sensors.time.monotonic', return_value=10.):
            robot.store.patch(0, np.zeros(SHAPES[0]), 10.)
            robot.store.patch(7, np.zeros(SHAPES[7]), 10.)
        robot.store.events.clear()
        with patch('tip_bridge.sensors.time.monotonic', return_value=610.), patch('tip_bridge.sensors.emit'):
            robot.tactile_health()
            self.assertEqual(robot._tactile_reused_hands, ('left', 'right'))
            self.assertEqual(robot.store.last_hand_stamps, [10., 10.])
            robot.store.patch(0, np.zeros(SHAPES[0]), 610.)
            robot.tactile_health()
            self.assertEqual(robot._tactile_reused_hands, ('right',))

    def test_future_packet_never_replaces_real_history(self):
        robot = sensors.IO.__new__(sensors.IO)
        robot.config, robot.store = CONFIG, sensors.Store()
        with patch('tip_bridge.sensors.time.monotonic', return_value=10.):
            for k in (0, 7):
                robot.store.patch(k, np.zeros(SHAPES[k]), 10.)
                robot.store.patch(k, np.zeros(SHAPES[k]), 1000.)
        with patch('tip_bridge.sensors.time.monotonic', return_value=610.), patch('tip_bridge.sensors.emit'):
            robot.tactile_health()
        self.assertEqual(robot.store.last_hand_stamps, [10., 10.])

    def test_one_hand_missing_cannot_borrow_other_hand_history(self):
        robot = sensors.IO.__new__(sensors.IO)
        robot.config, robot.store = CONFIG, sensors.Store()
        robot.store.patch(0, np.zeros(SHAPES[0]), time.monotonic())
        with self.assertRaises(ValueError):
            robot.tactile_health()


class RosAdapterTests(unittest.TestCase):
    def setUp(self):
        # Windows 3.10 monotonic/time_ns may tick every 15 ms; the fake ROS rig
        # supplies a fine-grained monotonic clock and strictly increasing stamps.
        self.clock = patch('tip_bridge.sensors.time.monotonic', time.perf_counter)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.logging = patch('tip_bridge.sensors.emit')
        self.logging.start()
        self.addCleanup(self.logging.stop)
        self.modules = patch.dict(sys.modules, fake_ros())
        self.modules.start()
        self.robot = sensors.IO()
        self.addCleanup(self.modules.stop)
        self.addCleanup(self.robot.close)
        self.q = populate(self.robot)

    def test_initialization_subscribes_to_target_contract_without_publishers(self):
        node = self.robot.node
        self.assertEqual(node.publishers, [])
        self.assertEqual(len(node.subscribers), 25)
        self.assertIn('/observation/head/images/compressed', node.subscribers)
        self.assertIn('/observation/left_arm/pose', node.subscribers)
        self.assertIn('/o10_control/right/state', node.subscribers)
        self.assertFalse(any('/sandisk/' in t for t in node.subscribers))

    def test_enable_creates_four_publishers_but_sends_no_targets(self):
        self.robot.enable()
        self.assertEqual(tuple(p.topic for p in self.robot.outputs), COMMAND_TOPICS)
        self.assertTrue(all(not p.messages for p in self.robot.outputs))

    def test_publish_splits_both_arms_and_hands_with_shared_ros_stamp(self):
        self.robot.enable()
        self.robot.publish(self.q)
        msgs = [p.messages[-1] for p in self.robot.outputs]
        for msg in msgs[:2]:
            self.assertEqual(msg.name, list(ARM_NAMES))
            self.assertEqual(len(msg.position), 7)
            self.assertEqual(msg.position[6], 0.)
            self.assertEqual(msg.velocity, [])
        for msg in msgs[2:]:
            self.assertEqual(msg.name, list(ACTIVE_JOINT_NAMES))
        self.assertTrue(all(m.header.stamp == msgs[0].header.stamp for m in msgs))
        np.testing.assert_allclose(msgs[0].position, self.q[:7])
        np.testing.assert_allclose(msgs[1].position, self.q[17:24])

    def test_no_publish_before_enable_or_for_malformed_action(self):
        with self.assertRaises(ValueError):
            self.robot.publish(self.q)
        self.robot.enable()
        self.q[23] = .001
        with self.assertRaises(ValueError):
            self.robot.publish(self.q)
        self.assertTrue(all(not p.messages for p in self.robot.outputs))

    def test_arm_targets_do_not_run_ahead_of_measured_feedback(self):
        self.robot.enable()
        q = self.q.copy()
        q[0] += .3
        self.robot.publish(q)
        self.assertAlmostEqual(self.robot.outputs[0].messages[-1].position[0]-self.q[0], .06)

    def test_competing_publisher_blocks_enable_before_publisher_creation(self):
        self.robot.node.others[COMMAND_TOPICS[0]] = ['another_bridge']
        with self.assertRaisesRegex(ValueError, 'Competing'):
            self.robot.enable()
        self.assertEqual(self.robot.node.publishers, [])

    def test_stale_feedback_and_hand_fault_block_all_four_outputs(self):
        self.robot.enable()
        self.robot.store.rows['ra'].clear()
        with self.assertRaises(ValueError):
            self.robot.publish(self.q)
        populate(self.robot)
        self.robot.state['left'][1].fault_latched = True
        with self.assertRaises(ValueError):
            self.robot.publish(self.q)
        self.assertTrue(all(not p.messages for p in self.robot.outputs))

    def test_stop_sends_measured_hands_once_and_no_arm_targets(self):
        self.robot.enable()
        self.robot.publish(self.q)
        counts = [len(p.messages) for p in self.robot.outputs]
        self.robot.stop()
        self.robot.stop()
        self.assertEqual([len(p.messages) for p in self.robot.outputs], [counts[0], counts[1], counts[2]+1, counts[3]+1])
        np.testing.assert_allclose(self.robot.outputs[2].messages[-1].position, self.q[7:17])

    def test_hands_ack_requires_new_command_and_new_arm_feedback(self):
        self.robot.enable()
        self.assertFalse(self.robot.hands_acked())
        populate(self.robot)
        self.assertTrue(self.robot.hands_acked())
        self.robot.state['right'][1].last_command_sent_stamp = stamp(1)
        self.assertFalse(self.robot.hands_acked())

    def test_ros_feedback_callback_uses_named_joint_order(self):
        msg = JointState()
        msg.header.stamp = stamp(time.time_ns())
        msg.name = list(reversed(ARM_NAMES))
        msg.position = list(reversed(self.q[:7]))
        self.robot.node.subscribers['/observation/left_arm/joint_states'](msg)
        self.assertIsNone(self.robot.store.error)
        np.testing.assert_array_equal(self.robot.store.rows['la'][-1][1], self.q[:7])

    def test_future_sensor_message_is_not_accepted(self):
        msg = JointState()
        msg.header.stamp = stamp(time.time_ns()+1_000_000_000)
        msg.position = self.q[:7].tolist()
        self.robot.node.subscribers['/observation/left_arm/joint_states'](msg)
        self.assertIn('Future', self.robot.store.error)


class ControllerTests(unittest.TestCase):
    def test_shadow_inference_runs_actions_without_enabling_or_publishing(self):
        import threading
        now = [100.]
        q = q34(reset_pose())
        robot = Mock()
        robot.limits = limits()
        robot.store.anchors = list(range(16))
        robot.check.return_value = q
        worker = Mock()
        worker.error = None
        worker.updates, worker.discarded = 1, 0
        worker.buffer = types.SimpleNamespace(lock=threading.RLock(), actions=None,
                                             next_action=Mock(return_value=(0, 0, q)))
        valid = dict(schema='sandisk100_dual_o10_v1', state_dim=46, physical_action_dim=34,
                     model_action_dim=48, ready=True, tactile_policy=stream.TACTILE_POLICY)
        with patch.object(controller, 'rpc', return_value=valid), \
             patch.object(controller, 'Workers', return_value=worker), \
             patch.object(controller, 'aligned_snapshot'), patch.object(controller, 'check_stop'), \
             patch.object(controller, 'emit'), patch.object(controller.time, 'monotonic', side_effect=lambda: now[0]), \
             patch.object(controller.time, 'sleep', side_effect=lambda dt: now.__setitem__(0, now[0]+dt)):
            controller.infer(types.SimpleNamespace(execute=False, duration=.05), robot)
        robot.enable.assert_not_called()
        robot.publish.assert_not_called()
        self.assertGreater(worker.buffer.next_action.call_count, 0)
        worker.close.assert_called_once()

    def test_late_slow_or_fast_results_are_discarded_before_buffer_update(self):
        import threading
        @dataclass
        class Update:
            session_id: str
            chunk_id: int
            revision: int
            observation_time: float
            sensor_time: float
            actions: object
            valid_from: int
            fps: float
        module = types.ModuleType('openpi.fastslow.buffer')
        module.ActionUpdate = Update
        for stage in ('slow', 'fast'):
            with self.subTest(stage=stage):
                clock, count, anchors, accepted = [100.], [0], {}, []
                worker = controller.Workers.__new__(controller.Workers)
                worker.io = types.SimpleNamespace(limits=limits())
                worker.stop, worker.ready, worker.calibrated = threading.Event(), threading.Event(), threading.Event()
                worker.calibrated.set()
                worker.session, worker.error, worker.updates, worker.discarded = 'test', None, 0, 0
                worker.feed_aligned_snapshot = lambda last, timeout: ({}, np.zeros(46), clock[0]-.01, 0.)
                def apply(update, now):
                    accepted.append(update)
                    worker.stop.set()
                    return True
                worker.buffer = types.SimpleNamespace(lock=threading.RLock(), apply=apply)
                def rpc(route, data=None, body=None):
                    if route == '/slow':
                        count[0] += 1
                        with np.load(io.BytesIO(body), allow_pickle=False) as fields:
                            anchors[count[0]] = float(fields['timestamp'])
                        if count[0] == 1 and stage == 'slow':
                            clock[0] += .28
                        return dict(chunk_id=count[0], slow_ms=1.)
                    if count[0] == 1 and stage == 'fast':
                        clock[0] += .28
                    return dict(session_id='test', chunk_id=count[0], revision=1,
                                observation_time=anchors[count[0]], sensor_time=anchors[count[0]],
                                actions=np.tile(q34(reset_pose()), (30, 1)).tolist(), valid_from=0, fps=FPS, fast_ms=1.)
                with patch.dict(sys.modules, {'openpi.fastslow.buffer': module}), \
                     patch.object(controller, 'rpc', side_effect=rpc), patch.object(controller, 'emit'), \
                     patch.object(controller.time, 'monotonic', side_effect=lambda: clock[0]):
                    worker.model()
                self.assertIsNone(worker.error)
                self.assertEqual(worker.discarded, 1)
                self.assertEqual([u.chunk_id for u in accepted], [2])

    def test_shadow_reset_never_enables_outputs(self):
        robot = types.SimpleNamespace(limits=limits(), enable=Mock())
        with patch.object(controller, 'ready', return_value=q34(reset_pose())), patch.object(controller, 'emit'):
            controller.reset(types.SimpleNamespace(execute=False), robot)
        robot.enable.assert_not_called()

    def test_mismatching_remote_contract_and_tactile_policy_are_rejected(self):
        valid = dict(schema='sandisk100_dual_o10_v1', state_dim=46, physical_action_dim=34,
                     model_action_dim=48, ready=True, live_budget_ok=True, tactile_policy=stream.TACTILE_POLICY)
        for changes in (dict(state_dim=45), dict(tactile_policy={})):
            with self.subTest(changes=changes):
                robot = Mock()
                with patch.object(controller, 'rpc', return_value=dict(valid, **changes)):
                    with self.assertRaises(ValueError):
                        controller.infer(types.SimpleNamespace(execute=True), robot)
                robot.enable.assert_not_called()

    def test_camera_gate_allows_calibrated_acknowledged_bilateral_pause(self):
        worker = controller.Workers.__new__(controller.Workers)
        worker.stop = __import__('threading').Event()
        worker.calibrated = __import__('threading').Event()
        worker.calibrated.set()
        worker.fed, worker.sequence = 10., 14
        store = sensors.Store()
        store.sequence = 14
        store.snapshot = Mock(return_value=({}, np.zeros(46), 610.))
        worker.io = types.SimpleNamespace(store=store, tactile_health=Mock())
        with patch.object(controller.time, 'monotonic', return_value=610.01):
            result = worker.feed_aligned_snapshot(-math.inf, .1)
        self.assertEqual(result[2], 610.)
        worker.io.tactile_health.assert_called_once()
        self.assertEqual(worker.fed, 10.)


class ConfigurationTests(unittest.TestCase):
    def test_camera_topics_follow_target_yaml(self):
        bindings = camera_bindings(CONFIG)
        self.assertEqual(bindings['top']['topic'], '/observation/head/images/compressed')
        import yaml
        cfg = copy.deepcopy(CONFIG)
        with tempfile.TemporaryDirectory() as tmp:
            rows = yaml.safe_load((DEPLOY / cfg['camera_config']).read_text(encoding='utf-8'))
            rows['cameras'][0]['compressed_topic'] = '/custom/head/compressed'
            path = Path(tmp) / 'cameras.yaml'
            path.write_text(yaml.safe_dump(rows), encoding='utf-8')
            cfg['camera_config'] = str(path)
            self.assertEqual(camera_bindings(cfg)['top']['topic'], '/custom/head/compressed')
            rows['cameras'][0]['enabled'] = False
            path.write_text(yaml.safe_dump(rows), encoding='utf-8')
            with self.assertRaises(ValueError):
                camera_bindings(cfg)

    def test_invalid_config_is_rejected(self):
        cfg = json.loads((ROOT / 'config/bridge.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'config.json'
            for key, value in [('camera_max_age_s', -1), ('tactile_mode', 'unknown'), ('arm_feedback_lead_rad', .2)]:
                with self.subTest(key=key):
                    path.write_text(json.dumps(dict(cfg, **{key: value})), encoding='utf-8')
                    with self.assertRaises(ValueError):
                        load_config(path)


class TransportTests(unittest.TestCase):
    def test_npz_transport_preserves_jpeg_bytes_and_state_without_pickle(self):
        state = np.arange(46, dtype=np.float64)
        jpeg = np.arange(255, dtype=np.uint8)
        body = common.pack(session=np.asarray('session'), state=state, timestamp=10.,
                           top=jpeg, left_wrist=jpeg, right_wrist=jpeg)
        with np.load(io.BytesIO(body), allow_pickle=False) as result:
            np.testing.assert_array_equal(result['state'], state)
            np.testing.assert_array_equal(result['top'], jpeg)
            self.assertEqual(result['session'].item(), 'session')

    def test_http_connection_reused_and_ambiguous_post_never_retried(self):
        import threading
        connection = Mock()
        response = Mock(status=200)
        response.read.return_value = b'{}'
        connection.getresponse.return_value = response
        connection.sock = None
        with patch.object(common, 'token', return_value='test-only'), \
             patch.object(common, '_rpc_local', threading.local()), \
             patch.object(common.http.client, 'HTTPConnection', return_value=connection) as factory:
            common.rpc('/feed', dict(session_id='test', frames=[]))
            common.rpc('/fast', dict(session_id='test', chunk_id=1))
            self.assertEqual(factory.call_count, 1)
            connection.getresponse.side_effect = OSError('ambiguous connection loss')
            with self.assertRaises(RuntimeError):
                common.rpc('/reset', dict(anchors=[]))
            self.assertEqual(connection.request.call_count, 3)
            connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
