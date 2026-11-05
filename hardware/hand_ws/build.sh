#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROS_SETUP="${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
[[ -f "$ROS_SETUP" ]] || { echo "missing ROS setup: $ROS_SETUP" >&2; exit 2; }
command -v colcon >/dev/null || { echo 'colcon is required' >&2; exit 2; }

# ROS setup is not nounset-safe on all installations.
set +u
source "$ROS_SETUP"
set -u
cd "$ROOT"
colcon build --base-paths "$ROOT/src/collection" --symlink-install \
  --packages-up-to omnihand_o10_control omnihand_o10_hardware_adapter \
  --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3.12 \
               -DPYTHON_EXECUTABLE=/usr/bin/python3.12
