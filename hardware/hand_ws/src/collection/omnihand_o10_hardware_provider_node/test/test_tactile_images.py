"""Contract checks for the fourteen raw Image topics; no hardware is opened."""

from dataclasses import replace
import threading
from types import SimpleNamespace
import unittest

import numpy as np

from omnihand_o10_contracts import Side
from omnihand_o10_hardware_adapter.contracts import (
    BackendCode,
    HardwareResponse,
    TactileSample,
)
from omnihand_o10_hardware_adapter.node import ProductionO10ProviderNode
from omnihand_o10_hardware_adapter.tactile_region_image import (
    O10TactileImagePublisher,
    tactile_region_images,
    tactile_region_to_image,
)


# Expected HxW and topic order come from the model's raw-input contract.
EXPECTED = (
    ("dorsum", "back", 11, 12, 102),
    ("palm", "palm", 14, 15, 78),
    ("thumb", "thumb/distal", 8, 2, 16),
    ("index", "index/distal", 9, 2, 18),
    ("middle", "middle/distal", 9, 2, 18),
    ("ring", "ring/distal", 9, 2, 18),
    ("little", "pinky/distal", 9, 2, 18),
)


def sample(side=Side.RIGHT, fill=None, stamp=1234.125):
    return TactileSample(
        side=side,
        stamp=stamp,
        **{
            name: tuple(range(count)) if fill is None else (fill,) * count
            for name, _, _, _, count in EXPECTED
        },
    )


def pixels(message):
    return np.frombuffer(message.data, dtype=np.uint8).reshape(
        message.height, message.step
    )[:, :message.width]


class RecordingNode:
    def __init__(self):
        self.topics = {}

    def create_publisher(self, message_type, topic, depth):
        if topic in self.topics:
            raise AssertionError(f"duplicate topic: {topic}")
        messages = []
        self.topics[topic] = messages
        return SimpleNamespace(publish=messages.append)


class TactileImagesTest(unittest.TestCase):
    def test_exact_fourteen_topics_and_wire_fields(self):
        node = RecordingNode()
        expected_topics = []
        for side in (Side.LEFT, Side.RIGHT):
            publisher = O10TactileImagePublisher(node, side)
            publisher.publish(sample(side))
            for _, suffix, height, width, _ in EXPECTED:
                topic = f"/observation/{side.value}_hand/tactile/{suffix}"
                expected_topics.append(topic)
                messages = node.topics[topic]
                self.assertEqual(len(messages), 1)
                msg = messages[0]
                self.assertEqual(msg.encoding, "mono8")
                self.assertEqual((msg.height, msg.width), (height, width))
                self.assertEqual(msg.step, width)
                self.assertEqual(msg.is_bigendian, 0)
                self.assertEqual(len(msg.data), height * width)
                self.assertEqual(msg.header.stamp.sec, 1234)
                self.assertEqual(msg.header.stamp.nanosec, 125_000_000)
        self.assertEqual(list(node.topics), expected_topics)

    def test_regions_follow_back_palm_fingers_order(self):
        self.assertEqual(
            [region for region, _ in tactile_region_images(sample())],
            [row[0] for row in EXPECTED],
        )

    def test_raw_range_is_not_normalized_or_resized(self):
        for side in (Side.LEFT, Side.RIGHT):
            for region, _, height, width, _ in EXPECTED:
                with self.subTest(side=side, region=region):
                    msg = tactile_region_to_image(sample(side, fill=255), region)
                    array = pixels(msg)
                    self.assertEqual(array.dtype, np.uint8)
                    self.assertEqual(array.shape, (height, width))
                    self.assertEqual(int(array.max()), 255)

    def test_zero_reading_is_published(self):
        node = RecordingNode()
        O10TactileImagePublisher(node, Side.LEFT).publish(sample(Side.LEFT, fill=0))
        self.assertEqual(len(node.topics), 7)
        for messages in node.topics.values():
            self.assertEqual(len(messages), 1)
            self.assertFalse(np.any(pixels(messages[0])))

    def test_finger_row_order_and_left_mirror(self):
        for region, _, height, width, count in EXPECTED[2:]:
            expected_right = np.arange(count, dtype=np.uint8).reshape(height, width)[::-1]
            right = pixels(tactile_region_to_image(sample(), region))
            left = pixels(tactile_region_to_image(sample(Side.LEFT), region))
            np.testing.assert_array_equal(right, expected_right)
            np.testing.assert_array_equal(left, expected_right[:, ::-1])

    def test_palm_and_back_keep_layout_and_reserved_cell_rule(self):
        right_palm = pixels(tactile_region_to_image(sample(), "palm"))
        self.assertEqual(int(right_palm[13, 3]), 0)
        self.assertEqual(int(right_palm[13, 2]), 1)
        self.assertEqual(int(right_palm[0, 4]), 76)
        reserved_only = replace(sample(fill=0), palm=(0,) * 77 + (255,))
        self.assertFalse(np.any(pixels(tactile_region_to_image(reserved_only, "palm"))))
        for region, cells in (("palm", 77), ("dorsum", 102)):
            filled = pixels(tactile_region_to_image(sample(fill=255), region))
            self.assertEqual(int(np.count_nonzero(filled)), cells)
            right = pixels(tactile_region_to_image(sample(), region))
            left = pixels(tactile_region_to_image(sample(Side.LEFT), region))
            np.testing.assert_array_equal(left, right[:, ::-1])
        right_back = pixels(tactile_region_to_image(sample(), "dorsum"))
        self.assertEqual(int(right_back[10, 3]), 0)
        self.assertEqual(int(right_back[0, 7]), 101)

    def test_wrong_side_does_not_publish(self):
        node = RecordingNode()
        publisher = O10TactileImagePublisher(node, Side.LEFT)
        with self.assertRaises(ValueError):
            publisher.publish(sample(Side.RIGHT))
        self.assertTrue(all(not messages for messages in node.topics.values()))

    def test_invalid_samples_are_rejected(self):
        for invalid in (-1, 256, 0.5, True):
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                sample(fill=invalid)
        with self.assertRaises(ValueError):
            replace(sample(), thumb=(0,) * 15)

    def test_new_samples_keep_their_own_timestamp(self):
        node = RecordingNode()
        publisher = O10TactileImagePublisher(node, Side.RIGHT)
        publisher.publish(sample(stamp=1234.125))
        publisher.publish(sample(stamp=1234.25))
        for messages in node.topics.values():
            self.assertEqual(
                [msg.header.stamp.nanosec for msg in messages],
                [125_000_000, 250_000_000],
            )

    def test_provider_success_publishes_only_region_images(self):
        for side in (Side.LEFT, Side.RIGHT):
            node, runtime = self.provider_runtime(
                side, HardwareResponse.success_result(sample(side))
            )
            ProductionO10ProviderNode._read_and_publish_tactile(runtime, side, 1)
            self.assertEqual(len(node.topics), 7)
            self.assertTrue(all(len(messages) == 1 for messages in node.topics.values()))

    def test_provider_failed_read_does_not_publish_fake_zero_frames(self):
        node, runtime = self.provider_runtime(
            Side.LEFT, HardwareResponse.failure(BackendCode.HARDWARE_ERROR, "read failed")
        )
        ProductionO10ProviderNode._read_and_publish_tactile(runtime, Side.LEFT, 1)
        self.assertTrue(all(not messages for messages in node.topics.values()))
        self.assertEqual(runtime.errors, ["read failed"])

    def test_provider_discards_inflight_sample_after_stream_stops(self):
        for stopped in ("closed", "timer_removed", "generation_changed"):
            with self.subTest(stopped=stopped):
                node, runtime = self.provider_runtime(
                    Side.LEFT, HardwareResponse.success_result(sample(Side.LEFT))
                )
                if stopped == "closed":
                    runtime._closed = True
                elif stopped == "timer_removed":
                    runtime._tactile_timers.clear()
                else:
                    runtime._tactile_stream_generation[Side.LEFT] = 2
                ProductionO10ProviderNode._read_and_publish_tactile(runtime, Side.LEFT, 1)
                self.assertTrue(all(not messages for messages in node.topics.values()))

    @staticmethod
    def provider_runtime(side, result):
        node = RecordingNode()
        errors = []
        runtime = SimpleNamespace(
            _hardware_locks={side: threading.Lock()},
            _applications={side: SimpleNamespace(read_tactile=lambda: result)},
            _background_lock=threading.Lock(),
            _closed=False,
            _tactile_timers={side: object()},
            _tactile_stream_generation={side: 1},
            _tactile_image_publishers={side: O10TactileImagePublisher(node, side)},
            get_logger=lambda: SimpleNamespace(
                error=lambda message, **kwargs: errors.append(message)
            ),
            errors=errors,
        )
        return node, runtime


if __name__ == "__main__":
    unittest.main()
