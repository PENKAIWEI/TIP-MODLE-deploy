"""Pure data conversions; no ROS node, device connection or SDK import."""
import io
import math
import xml.etree.ElementTree as ET

import numpy as np

from .common import SHAPES, vector

SIDES = ('left', 'right')
ARM_NAMES = tuple(f'joint{i}' for i in range(1, 8))
ARM_COMMANDS = tuple(f'/observation/{side}_arm/joint_cmd' for side in SIDES)
HAND_COMMANDS = tuple(f'/o10_control/{side}/command' for side in SIDES)
COMMAND_TOPICS = ARM_COMMANDS + HAND_COMMANDS


def joint_feedback(msg, *, arm, hand_names=()):
    expected = ARM_NAMES if arm else tuple(hand_names)
    values = vector(msg.position, len(expected))
    names = tuple(msg.name)
    if names:
        if len(names) != len(expected) or len(set(names)) != len(expected) or set(names) != set(expected):
            raise ValueError('Unexpected feedback joint names')
        by_name = dict(zip(names, values))
        values = np.array([by_name[name] for name in expected])
    # O10 Provider intentionally omits names; use its canonical fixed order.
    if arm:
        if abs(values[6]) > 1e-4:
            raise ValueError('Arm feedback joint7 must be zero padding')
        values[6] = 0.
    return values


def pose_vector(msg):
    p, q = msg.pose.position, msg.pose.orientation
    vector([p.x, p.y, p.z, q.x, q.y, q.z, q.w], 7)
    norm = math.sqrt(q.x*q.x + q.y*q.y + q.z*q.z + q.w*q.w)
    if abs(norm - 1) > .01:
        raise ValueError('Invalid end-effector quaternion')
    roll = math.atan2(2*(q.w*q.x + q.y*q.z), 1-2*(q.x*q.x + q.y*q.y))
    pitch = math.asin(max(-1., min(1., 2*(q.w*q.y - q.z*q.x))))
    yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y + q.z*q.z))
    return np.asarray([p.x, p.y, p.z, roll, pitch, yaw])


def decode_tactile(msg, index):
    if msg.encoding != 'mono8' or (msg.height, msg.width) != SHAPES[index]:
        raise ValueError('Unexpected native tactile shape or encoding')
    if msg.step < msg.width or len(msg.data) != msg.height * msg.step:
        raise ValueError('Invalid tactile byte layout')
    return np.frombuffer(bytes(msg.data), np.uint8).reshape(msg.height, msg.step)[:, :msg.width].copy()


def model_image(data, binding):
    """Training-compatible resize with padding, RGB then JPEG quality 90."""
    import cv2
    from PIL import Image
    with Image.open(io.BytesIO(data)) as image:
        if image.size != (binding['width'], binding['height']):
            raise ValueError(f'Camera size {image.size} differs from color_profile')
        rgb = np.asarray(image.convert('RGB'))
    h, w = rgb.shape[:2]
    scale = 224 / max(h, w)
    hh, ww = round(h*scale), round(w*scale)
    resized = cv2.resize(rgb, (ww, hh), interpolation=cv2.INTER_AREA)
    out = np.zeros((224, 224, 3), np.uint8)
    y, x = (224-hh)//2, (224-ww)//2
    out[y:y+hh, x:x+ww] = resized
    ok, jpeg = cv2.imencode('.jpg', cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    if not ok:
        raise ValueError('Camera JPEG encoding failed')
    return jpeg.reshape(-1).copy()


def split_action(q, hand_names):
    q = vector(q, 34).copy()
    if np.max(np.abs(q[[6, 23]])) > 1e-4:
        raise ValueError('Action padding must remain zero')
    q[[6, 23]] = 0.
    return ((ARM_NAMES, q[:7]), (ARM_NAMES, q[17:24]),
            (tuple(hand_names), q[7:17]), (tuple(hand_names), q[24:34]))


def arm_limits(path):
    """URDF intersected with RM65 reference bounds; driver is final authority."""
    joints = {j.get('name'): j for j in ET.parse(path).getroot().iter('joint')}
    lo, hi = [], []
    nominal = np.deg2rad([178, 130, 135, 178, 128, 360])
    for i, name in enumerate(ARM_NAMES[:6]):
        limit = joints[name].find('limit')
        lo.append(max(float(limit.get('lower')), -nominal[i]))
        hi.append(min(float(limit.get('upper')), nominal[i]))
    if not np.isfinite([lo, hi]).all() or np.any(np.asarray(lo) >= hi):
        raise ValueError('Invalid arm URDF limits')
    return lo, hi
