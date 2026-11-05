"""Offline deployment contract inspection: no ROS node or network request."""
import argparse
import json

from .common import q34, reset_pose
from .config import CONFIG, camera_bindings
from .contracts import ARM_NAMES, COMMAND_TOPICS, arm_limits
from .stream import TACTILE_POLICY


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    cameras = camera_bindings(CONFIG)
    bounds = arm_limits(CONFIG['deployment_root'] / CONFIG['arm_urdf'])
    pose = q34(reset_pose())
    for start in (0, 17):
        if any(q < lo or q > hi for q, lo, hi in zip(pose[start:start+6], *bounds)):
            raise ValueError('Reset pose exceeds the deployment arm limits')
    print(json.dumps(dict(deployment_root=str(CONFIG['deployment_root']),
                          cameras=cameras, command_topics=COMMAND_TOPICS,
                          arm_joint_names=ARM_NAMES, arm_limits_rad=bounds,
                          state_dim=46, action_dim=34, tactile_policy=TACTILE_POLICY,
                          reset_source=reset_pose().get('source'),
                          arm_ack_topic=None, physical_outputs=False), indent=2))


if __name__ == '__main__':
    main()
