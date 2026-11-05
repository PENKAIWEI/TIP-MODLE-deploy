"""ROS IO for TIP's joint_cmd arm receiver and HAND-2.0/Camera-2.1 interfaces.

History, numeric alignment and tactile feed are ported from pour_deploy.sensors.
The old combined arm target, status and prepare/stop services are not used.
"""
from collections import deque
import math
import os
import threading
import time

import numpy as np

from .common import CAMERAS, PATCHES, vector, project, emit
from .config import CONFIG, camera_bindings
from .contracts import (COMMAND_TOPICS, SIDES, arm_limits, decode_tactile,
                        joint_feedback, model_image, pose_vector, split_action)


class Store:
    def __init__(self, config=None):
        self.config = CONFIG if config is None else config
        self.lock = threading.RLock()
        self.rows = {k: deque(maxlen=512) for k in (*CAMERAS, 'la', 'lh', 'ra', 'rh', 'lp', 'rp')}
        self.events = deque(maxlen=12000)
        self.sequence = 0
        self.anchors = []
        self.error = None
        self.camera_metadata = {}
        self.snapshot_metadata = {}
        self.patch_stamps = [None] * 14
        self.last_hand_stamps = [None, None]

    def add(self, key, value, stamp, metadata=None):
        value = np.asarray(value).copy()
        if not math.isfinite(stamp) or not np.isfinite(value).all():
            raise ValueError('Nonfinite sensor')
        with self.lock:
            rows = self.rows[key]
            if rows and stamp < rows[-1][0]:
                raise ValueError('Source time reversed ' + key)
            if rows and stamp == rows[-1][0]:
                return False
            if key in ('lp', 'rp') and rows:
                value[3:] = np.unwrap(np.stack([rows[-1][1][3:], value[3:]]), axis=0)[1]
            if metadata is not None:
                if len(rows) == rows.maxlen:
                    self.camera_metadata.pop((key, rows[0][0]), None)
                self.camera_metadata[key, stamp] = dict(metadata)
            rows.append((stamp, value))
            if key == 'top' and len(self.anchors) < 16:
                self.anchors.append(stamp)
            return True

    def patch(self, index, raw, stamp):
        if not math.isfinite(stamp):
            raise ValueError('Nonfinite tactile timestamp')
        with self.lock:
            previous = self.patch_stamps[index]
            if previous is not None and stamp <= previous:
                if stamp == previous:
                    return
                raise ValueError('Tactile source time reversed')
            self.patch_stamps[index] = stamp
            side = index // 7
            old = self.last_hand_stamps[side]
            if stamp <= time.monotonic():
                self.last_hand_stamps[side] = stamp if old is None else max(old, stamp)
            self.sequence += 1
            self.events.append(dict(sequence=self.sequence, patch=index,
                                    raw=np.asarray(raw).tolist(), timestamp=stamp))

    def after(self, sequence):
        with self.lock:
            if self.events and sequence < self.events[0]['sequence'] - 1:
                raise ValueError('Tactile feed queue overrun; restart the observation session')
            return [e.copy() for e in self.events if e['sequence'] > sequence]

    def latest(self, key, now, age=None):
        age = self.config['joint_max_age_s'] if age is None else age
        rows = self.rows[key]
        if not rows or not 0 <= now - rows[-1][0] <= age:
            raise ValueError('Missing/stale ' + key)
        return rows[-1][1].copy()

    def joints(self):
        with self.lock:
            now = time.monotonic()
            return np.concatenate([self.latest(k, now) for k in ('la', 'lh', 'ra', 'rh')])

    def continuous(self, key, stamp):
        rows = self.rows[key]
        if not rows or rows[0][0] > stamp or rows[-1][0] < stamp:
            raise ValueError('Waiting for state bracket ' + key)
        times = np.asarray([r[0] for r in rows])
        r = int(np.searchsorted(times, stamp))
        if times[r] == stamp:
            return rows[r][1].copy()
        l = r - 1
        gap = self.config['state_bracket_s']
        if stamp-times[l] > gap or times[r]-stamp > gap:
            raise ValueError('State interpolation gap ' + key)
        return rows[l][1] + (rows[r][1]-rows[l][1])*(stamp-times[l])/(times[r]-times[l])

    def snapshot(self):
        with self.lock:
            now = time.monotonic()
            for stamp, top in reversed(self.rows['top']):
                if not 0 <= now-stamp <= self.config['camera_max_age_s']:
                    continue
                try:
                    images, times = {'top': top}, {'top': stamp}
                    for key in CAMERAS[1:]:
                        if not self.rows[key] or self.rows[key][-1][0] < stamp:
                            raise ValueError('Waiting for wrist bracket')
                        row = min(self.rows[key], key=lambda x: abs(x[0]-stamp))
                        if not 0 <= now-row[0] <= self.config['camera_max_age_s']:
                            raise ValueError('Stale wrist image')
                        images[key], times[key] = row[1], row[0]
                    if max(times.values())-min(times.values()) > self.config['camera_sync_tolerance_s']:
                        raise ValueError('Three-camera timestamp spread exceeded')
                    state = np.concatenate([self.continuous(k, stamp) for k in ('la', 'lh', 'ra', 'rh', 'lp', 'rp')])
                    self.snapshot_metadata = {k: dict(self.camera_metadata.get((k, t), {}), monotonic_stamp=t)
                                              for k, t in times.items()}
                    return images, vector(state, 46), stamp
                except ValueError:
                    continue
        raise ValueError('No fresh aligned three-camera/state46 observation')


class IO:
    def __init__(self, config=None):
        import rclpy
        from rclpy.node import Node
        from rclpy.qos import QoSProfile, ReliabilityPolicy
        from rclpy.executors import SingleThreadedExecutor
        from rclpy.signals import SignalHandlerOptions
        from sensor_msgs.msg import JointState, CompressedImage, Image
        from geometry_msgs.msg import PoseStamped
        from rokoko_omnihand_msgs.msg import O10ControlState
        from omnihand_o10_contracts.joints import JOINT_LIMITS, ACTIVE_JOINT_NAMES
        from omnihand_o10_contracts.side import Side

        self.config = CONFIG if config is None else config
        bindings = camera_bindings(self.config)
        arm_bounds = arm_limits(self.config['deployment_root'] / self.config['arm_urdf'])
        self.limits = {s: {'arm': arm_bounds,
                          'hand': (JOINT_LIMITS[Side(s)].lower, JOINT_LIMITS[Side(s)].upper)} for s in SIDES}
        self.rclpy, self.JointState, self.names = rclpy, JointState, ACTIVE_JOINT_NAMES
        self.store = Store(self.config)
        self.state, self.source_ns = {}, {}
        self.lock = threading.RLock()
        self.outputs = None
        self.enabled = False
        self.execution_fence = None
        self.execution_started = None
        self.last_publish_ns = 0
        self.image_condition = threading.Condition()
        self.image_stop = False
        self.image_jobs = {k: deque(maxlen=1) for k in CAMERAS}
        self.image_threads = []
        rclpy.init(args=[], signal_handler_options=SignalHandlerOptions.NO)
        self.node = Node('tip_model_bridge_' + str(os.getpid()))
        self.qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.subs = []

        def subscribe(kind, topic, fn, qos=None, camera=False):
            def receive(msg):
                try:
                    receipt = time.monotonic()
                    source = msg.header.stamp
                    ns = source.sec * 10**9 + source.nanosec
                    if ns <= 0:
                        raise ValueError('Missing source timestamp ' + topic)
                    ros_now = self.node.get_clock().now().nanoseconds
                    age = (ros_now - ns) * 1e-9
                    if age < -self.config['source_future_tolerance_s']:
                        raise ValueError('Future source timestamp ' + topic)
                    previous = self.source_ns.get(topic)
                    if previous is not None and ns <= previous:
                        if ns == previous:
                            return
                        if camera:
                            with self.store.lock:
                                for key in CAMERAS:
                                    self.store.rows[key].clear()
                                self.store.camera_metadata.clear()
                        self.store.error = 'Source clock restarted; restart bridge session: ' + topic
                        return
                    self.source_ns[topic] = ns
                    # Convert elapsed ROS source age into the local monotonic domain.
                    # Never compare epoch ROS seconds directly with monotonic seconds.
                    fn(msg, receipt - age)
                except Exception as exc:
                    if camera:
                        emit('camera_frame_dropped', topic=topic, reason=str(exc))
                    else:
                        self.store.error = str(exc)
            self.subs.append(self.node.create_subscription(kind, topic, receive, self.qos if qos is None else qos))

        for side, ak, hk, pk in [('left', 'la', 'lh', 'lp'), ('right', 'ra', 'rh', 'rp')]:
            subscribe(JointState, f'/observation/{side}_arm/joint_states',
                      lambda m, t, k=ak: self.store.add(k, joint_feedback(m, arm=True), t))
            subscribe(JointState, f'/o10/{side}/joint_states',
                      lambda m, t, k=hk: self.store.add(k, joint_feedback(m, arm=False, hand_names=self.names), t))
            subscribe(PoseStamped, f'/observation/{side}_arm/pose',
                      lambda m, t, k=pk: self.store.add(k, pose_vector(m), t))
            def hand_status(msg, stamp, expected=side):
                if msg.side != expected:
                    raise ValueError('O10 state side differs from topic')
                with self.lock:
                    self.state[expected] = (stamp, msg)
            subscribe(O10ControlState, f'/o10_control/{side}/state', hand_status, 10)
            for j, patch in enumerate(PATCHES):
                index = (0 if side == 'left' else 7) + j
                subscribe(Image, f'/observation/{side}_hand/tactile/{patch}',
                          lambda m, t, k=index: self.store.patch(k, decode_tactile(m, k), t))

        for camera in CAMERAS:
            def image_worker(key=camera):
                while True:
                    with self.image_condition:
                        self.image_condition.wait_for(lambda: self.image_stop or self.image_jobs[key])
                        if self.image_stop:
                            return
                        data, stamp, metadata = self.image_jobs[key].pop()
                    try:
                        image = model_image(data, bindings[key])
                        self.store.add(key, image, stamp, metadata)
                    except Exception as exc:
                        emit('camera_frame_dropped', camera=key, reason=str(exc))
            thread = threading.Thread(target=image_worker, daemon=True)
            self.image_threads.append(thread)
            thread.start()
            def queue_image(msg, stamp, key=camera):
                fmt = msg.format.lower()
                if not any(codec in fmt for codec in ('jpeg', 'jpg', 'png')):
                    raise ValueError('Unsupported compressed image format ' + msg.format)
                metadata = dict(role=key, source_stamp_ns=msg.header.stamp.sec*10**9+msg.header.stamp.nanosec,
                                frame_id=msg.header.frame_id, format=msg.format)
                with self.image_condition:
                    if not self.image_stop:
                        self.image_jobs[key].append((bytes(msg.data), stamp, metadata))
                        self.image_condition.notify_all()
            subscribe(CompressedImage, bindings[camera]['topic'], queue_image, camera=True)
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.node)
        self.thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.thread.start()

    def check(self, prepared=False):
        if self.store.error:
            raise ValueError(self.store.error)
        if prepared and not self.enabled:
            raise ValueError('Bridge outputs are not enabled')
        with self.lock:
            for side in SIDES:
                row = self.state.get(side)
                if row is None or not 0 <= time.monotonic()-row[0] <= self.config['driver_state_max_age_s']:
                    raise ValueError('Missing/stale hand driver state ' + side)
                msg = row[1]
                if msg.fault_latched or msg.fault_reason_mask or msg.phase == 5:
                    raise ValueError(side + ' hand fault latched; recover through the hardware operator interface')
                if not msg.feedback_ready or not msg.error_monitor_ready or not msg.motion_enabled:
                    raise ValueError(side + ' hand driver is not ready')
                if prepared and msg.target_result >= 3:
                    raise ValueError(side + ' hand rejected target: ' + str(msg.target_result))
        # The current arm receiver exposes feedback, but no aggregate health/ACK topic.
        return self.store.joints()

    def tactile_health(self):
        now = time.monotonic()
        with self.store.lock:
            for side in range(2):
                times = [e['timestamp'] for e in self.store.events if e['patch']//7 == side and e['timestamp'] <= now]
                previous = self.store.last_hand_stamps[side]
                if previous is not None and previous <= now:
                    times.append(previous)
                self.store.last_hand_stamps[side] = max(times) if times else None
            stamps = tuple(self.store.last_hand_stamps)
        if any(t is None or t > now for t in stamps):
            raise ValueError('Both hands require real causal tactile history')
        ages = tuple(now-t for t in stamps)
        if self.config['tactile_mode'] == 'strict' and max(ages) > self.config['tactile_strict_timeout_s']:
            raise ValueError('Tactile stream timed out under strict policy')
        reused = tuple(side for side, age in zip(SIDES, ages) if age > self.config['tactile_fallback_after_s'])
        if reused != getattr(self, '_tactile_reused_hands', ()):
            emit('tactile_fallback', source='local', reused_hands=reused,
                 hand_age_ms=dict(zip(SIDES, [age*1000 for age in ages])),
                 max_hold_ms=None if self.config['tactile_mode'] == 'hold' else self.config['tactile_strict_timeout_s']*1000)
        self._tactile_reused_hands = reused

    def conflicts(self):
        for topic in COMMAND_TOPICS:
            endpoints = self.node.get_publishers_info_by_topic(topic)
            others = [e.node_name for e in endpoints if e.node_name != self.node.get_name()]
            if others:
                raise ValueError('Competing target publisher ' + topic + ': ' + str(others))

    def enable(self):
        self.check()
        self.conflicts()
        if self.outputs is not None:
            raise ValueError('Output publishers already exist')
        self.outputs = [self.node.create_publisher(self.JointState, topic, 1) for topic in COMMAND_TOPICS]
        deadline = time.monotonic() + 2
        while not all(pub.get_subscription_count() == 1 for pub in self.outputs):
            if time.monotonic() > deadline:
                raise ValueError('Each command topic must have exactly one driver subscriber')
            time.sleep(.02)
        self.check()
        self.conflicts()
        self.execution_fence = self.node.get_clock().now().nanoseconds
        self.execution_started = time.monotonic()
        self.enabled = True
        # First actual publish starts arm motion; there is no prepare/enable service.

    def hands_acked(self):
        self.check(prepared=True)
        with self.store.lock:
            if any(self.store.rows[k][-1][0] <= self.execution_started for k in ('la', 'ra')):
                return False
        with self.lock:
            for side in SIDES:
                msg = self.state[side][1]
                stamp = msg.last_command_sent_stamp
                if not msg.command_time_available or stamp.sec*10**9+stamp.nanosec <= self.execution_fence:
                    return False
        return True

    def publish(self, q):
        if not self.enabled or self.outputs is None:
            raise ValueError('Outputs not enabled')
        actual = project(self.check(prepared=True), self.limits, feedback=True)
        q = project(q, self.limits)
        # Do not let queued model targets run far ahead of actual arm feedback.
        lead = self.config['arm_feedback_lead_rad']
        for start in (0, 17):
            q[start:start+6] = np.clip(q[start:start+6], actual[start:start+6]-lead, actual[start:start+6]+lead)
        q = project(q, self.limits)
        now = self.node.get_clock().now()
        if now.nanoseconds <= max(self.last_publish_ns, self.execution_fence):
            raise ValueError('ROS command clock did not advance')
        rows = split_action(q, self.names)
        # Construct all messages before publishing any side; same stamp on all four.
        messages = []
        for names, values in rows:
            msg = self.JointState()
            msg.header.stamp = now.to_msg()
            msg.name = list(names)
            msg.position = values.tolist()
            messages.append(msg)
        self.last_publish_ns = now.nanoseconds
        for pub, msg in zip(self.outputs, messages):
            pub.publish(msg)

    def stop(self):
        if not self.enabled:
            return
        self.enabled = False
        # Stop arm publication: native target_timeout_sec (default .3 s) then decelerates.
        # O10 gets one fresh measured hold target; no old policy target is replayed.
        try:
            q = self.store.joints()
            stamp = self.node.get_clock().now().to_msg()
            for pub, start, side in zip(self.outputs[2:], (7, 24), SIDES):
                msg = self.JointState()
                msg.header.stamp = stamp
                msg.name = list(self.names)
                msg.position = np.clip(q[start:start+10], *self.limits[side]['hand']).tolist()
                pub.publish(msg)
        except Exception as exc:
            emit('hand_hold_unavailable', reason=str(exc))
        emit('outputs_stopped', arm_stop='native_command_timeout', arm_acceptance_feedback=False)

    def close(self):
        self.stop()
        with self.image_condition:
            self.image_stop = True
            self.image_condition.notify_all()
        self.executor.shutdown(timeout_sec=2)
        self.thread.join(timeout=2)
        for thread in self.image_threads:
            thread.join(timeout=2)
        self.node.destroy_node()
        if self.rclpy.ok():
            self.rclpy.shutdown()
