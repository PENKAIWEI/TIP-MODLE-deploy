"""Publish raw mono8 regions; model history and alignment belong to the Bridge."""

from __future__ import annotations

from sensor_msgs.msg import Image

from omnihand_o10_contracts import Side

from .adapters.ros_wire import _ros_time
from .contracts import TactileSample

__all__ = [
    "O10TactileImagePublisher",
    "REGION_ORDER",
    "tactile_region_images",
    "tactile_region_to_image",
]


# Per-hand model order. A future Bridge maps left to blocks 0..6 and right to
# 7..13 by topic, not by cross-topic callback arrival order.
REGION_ORDER = ("dorsum", "palm", "thumb", "index", "middle", "ring", "little")

_TOPIC_SUFFIXES = {
    "thumb": "thumb/distal",
    "index": "index/distal",
    "middle": "middle/distal",
    "ring": "ring/distal",
    "little": "pinky/distal",
    "palm": "palm",
    "dorsum": "back",
}

# Protocol grid cells are expressed top-to-bottom on the canonical right-hand
# diagram. Raw point indices run bottom-to-top.
_LAYOUTS = {
    "thumb": (2, 8, (2,) * 8, (0,) * 8, False),
    "index": (2, 9, (2,) * 9, (0,) * 9, False),
    "middle": (2, 9, (2,) * 9, (0,) * 9, False),
    "ring": (2, 9, (2,) * 9, (0,) * 9, False),
    "little": (2, 9, (2,) * 9, (0,) * 9, False),
    "palm": (
        15,
        14,
        (11, 14, 8, 6, 5, 4, 4, 4, 4, 4, 4, 4, 3, 2),
        (4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2),
        True,
    ),
    "dorsum": (
        12,
        11,
        (4, 8, 10, 10, 12, 12, 12, 10, 10, 8, 6),
        (4, 2, 1, 1, 0, 0, 0, 1, 1, 2, 3),
        False,
    ),
}


def _coordinates(name: str):
    width, height, row_lengths, offsets, reverse_row = _LAYOUTS[name]
    cells = []
    for row in range(height - 1, -1, -1):
        xs = range(offsets[row], offsets[row] + row_lengths[row])
        if reverse_row:
            xs = reversed(tuple(xs))
        cells.extend((x, row) for x in xs)
    return width, height, tuple(cells)


_COORDINATES = {name: _coordinates(name) for name in REGION_ORDER}


def tactile_region_to_image(sample: TactileSample, region: str) -> Image:
    """Keep raw uint8 values at native HxW, without resizing or normalization."""

    width, height, cells = _COORDINATES[region]
    values = getattr(sample, region)
    if len(values) < len(cells):
        raise ValueError(f"{region} has {len(values)} values, need at least {len(cells)}")

    # The vendor palm frame has one reserved final value; the diagram defines
    # only cells 0..76.
    values = values[: len(cells)]
    pixels = bytearray(width * height)
    for value, (x, y) in zip(values, cells):
        if sample.side is Side.LEFT:
            x = width - 1 - x
        pixels[y * width + x] = value

    message = Image()
    message.header.stamp = _ros_time(sample.stamp)
    message.height = height
    message.width = width
    message.encoding = "mono8"
    message.is_bigendian = 0
    message.step = width
    message.data = bytes(pixels)
    return message


def tactile_region_images(sample: TactileSample):
    """Return back, palm and five fingers with the same source sample stamp."""

    return tuple(
        (region, tactile_region_to_image(sample, region)) for region in REGION_ORDER
    )


class O10TactileImagePublisher:
    """Own exactly seven model-facing sensor_msgs/Image topics for one hand."""

    def __init__(self, node, side: Side) -> None:
        self._side = Side.from_value(side)
        self._publishers = {
            region: node.create_publisher(
                Image,
                f"/observation/{self._side.value}_hand/tactile/"
                f"{_TOPIC_SUFFIXES[region]}",
                10,
            )
            for region in REGION_ORDER
        }

    def publish(self, sample: TactileSample) -> None:
        if sample.side is not self._side:
            raise ValueError(
                f"cannot publish {sample.side.value} tactile images on "
                f"{self._side.value} topics"
            )
        for region, image in tactile_region_images(sample):
            self._publishers[region].publish(image)
