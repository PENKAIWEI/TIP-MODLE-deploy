#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROS_SETUP="${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
[[ -f "$ROS_SETUP" ]] || { echo "missing ROS setup: $ROS_SETUP" >&2; exit 2; }
command -v colcon >/dev/null || { echo 'colcon is required' >&2; exit 2; }

set +u
source "$ROS_SETUP"
set -u
cd "$ROOT"
colcon build --base-paths "$ROOT/arm_model_control" --packages-select arm_model_control \
  --symlink-install --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3.12
