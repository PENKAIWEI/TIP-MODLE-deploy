"""Paths are relative to this bridge or its sibling hardware deployment."""
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_config(path=None, deployment_root=None):
    filename = Path(path or os.environ.get('TIP_BRIDGE_CONFIG', ROOT / 'config/bridge.json'))
    cfg = json.loads(filename.read_text(encoding='utf-8'))
    positive = ('startup_timeout_s', 'camera_max_age_s', 'camera_sync_tolerance_s',
                'joint_max_age_s', 'state_bracket_s', 'driver_state_max_age_s',
                'source_future_tolerance_s', 'arm_feedback_lead_rad',
                'tactile_fallback_after_s', 'tactile_strict_sample_age_s',
                'tactile_strict_timeout_s')
    for key in positive:
        value = cfg[key]
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f'{key} must be finite and positive')
    if cfg['arm_feedback_lead_rad'] > .06:
        raise ValueError('arm_feedback_lead_rad must be <= 0.06 for the default arm safety gate')
    if cfg['tactile_mode'] not in ('hold', 'strict'):
        raise ValueError('tactile_mode must be hold or strict')
    if set(cfg['camera_roles']) != {'top', 'left_wrist', 'right_wrist'} or len(set(cfg['camera_roles'].values())) != 3:
        raise ValueError('Three distinct camera role bindings are required')
    cfg['deployment_root'] = Path(deployment_root or os.environ.get('TIP_DEPLOY_ROOT', ROOT.parent)).resolve()
    cfg['model_url'] = os.environ.get('TIP_MODEL_URL', os.environ.get('POUR_MODEL_URL', cfg['model_url']))
    cfg['checkpoint'] = os.environ.get('TIP_MODEL_CHECKPOINT', cfg['checkpoint'])
    return cfg


def camera_bindings(cfg):
    import yaml
    path = cfg['deployment_root'] / cfg['camera_config']
    rows = yaml.safe_load(path.read_text(encoding='utf-8'))['cameras']
    result = {}
    for role, name in cfg['camera_roles'].items():
        candidates = [row for row in rows if row.get('name') == name]
        if len(candidates) != 1 or candidates[0].get('enabled') is not True:
            raise ValueError(f'Required camera {role}/{name} is missing, duplicated or disabled')
        row = candidates[0]
        width, height, fps = (int(v) for v in row['color_profile'].split('x'))
        if min(width, height, fps) <= 0:
            raise ValueError('Invalid camera color_profile')
        topic = row['compressed_topic']
        if not isinstance(topic, str) or not topic.startswith('/'):
            raise ValueError('Expected an absolute compressed camera topic')
        result[role] = dict(topic=topic, width=width, height=height, name=name)
    if len({row['topic'] for row in result.values()}) != 3:
        raise ValueError('Camera compressed topics must be distinct')
    return result


CONFIG = load_config()
