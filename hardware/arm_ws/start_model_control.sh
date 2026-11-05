#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
THIRD_PARTY="$(cd -- "$ROOT/../../third_party" && pwd -P)"
REALMAN_SRC="$THIRD_PARTY/realman_sdk/src"
VENDOR_PYTHON="$THIRD_PARTY/python"
DRY_RUN=true
CHECK_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --confirm-motion) DRY_RUN=false ;;
    --check-only) CHECK_ONLY=1 ;;
    -h|--help)
      echo 'Usage: bash start_model_control.sh [--check-only | --dry-run | --confirm-motion]'
      exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done
for required in \
  "$ROOT/arm_model_control/arm_model_control/model_node.py" \
  "$ROOT/arm_model_control/arm_model_control/model_commands.py" \
  "$ROOT/arm_model_control/arm_model_control/arm_observer.py" \
  "$REALMAN_SRC/Robotic_Arm/rm_robot_interface.py" \
  "$REALMAN_SRC/Robotic_Arm/libs/linux_x86/libapi_c.so" \
  "$VENDOR_PYTHON/numpy/__init__.py" \
  "$VENDOR_PYTHON/ruckig.cpython-312-x86_64-linux-gnu.so" \
  "$ROOT/rm_65.urdf"; do
  [[ -f "$required" ]] || { echo "missing $required" >&2; exit 2; }
done
[[ -d "$VENDOR_PYTHON/numpy.libs" ]] || {
  echo "missing bundled NumPy native libraries: $VENDOR_PYTHON/numpy.libs" >&2
  exit 2
}
if (( CHECK_ONLY )); then
  echo 'model arm files ready; no ROS node or SDK connection started'
  exit 0
fi
[[ -f "$ROOT/install/setup.bash" ]] || { echo 'run bash build.sh first' >&2; exit 2; }
set +u
source "${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
source "$ROOT/install/setup.bash"
set -u
export PYTHONNOUSERSITE=1
export PYTHONPATH="$VENDOR_PYTHON:$REALMAN_SRC${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="$REALMAN_SRC/Robotic_Arm/libs/linux_x86${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
/usr/bin/python3.12 - "$THIRD_PARTY" <<'PY'
from pathlib import Path
import importlib
import sys

root = Path(sys.argv[1]).resolve()
for name in ("numpy", "ruckig", "Robotic_Arm.rm_robot_interface"):
    module = importlib.import_module(name)
    loaded = Path(module.__file__).resolve()
    if not loaded.is_relative_to(root):
        raise SystemExit(f"{name} resolved outside third_party: {loaded}")
    print(f"{name}: {loaded}")
PY
if [[ "$(ros2 pkg prefix arm_model_control)" != "$ROOT/install/arm_model_control" ]]; then
  echo 'arm_model_control resolves to another workspace' >&2
  exit 2
fi
/usr/bin/python3 - "$ROOT" <<'PY'
from pathlib import Path
import sys
from arm_model_control import model_node
root = Path(sys.argv[1]).resolve()
loaded = Path(model_node.__file__).resolve()
if not loaded.is_relative_to(root):
    raise SystemExit(f"rebuild arm_model_control; loaded {loaded}")
PY
if ! nodes="$(timeout 8 ros2 node list --no-daemon --spin-time 2)"; then
  echo 'cannot inspect ROS graph; refusing another arm connection' >&2
  exit 2
fi
if [[ "$nodes" == *"/arm_model_control_node"* || "$nodes" == *"/teleop_node"* ]]; then
  echo 'another arm controller is visible; stop its owner normally first' >&2
  exit 2
fi
echo "starting model arm receiver (dry_run=$DRY_RUN); a fresh valid joint_cmd can initiate motion"
echo 'inputs: /observation/{left,right}_arm/joint_cmd (joint1..joint7, rad; joint7=0)'
exec ros2 run arm_model_control model_arm_node --ros-args \
  -p dry_run:="$DRY_RUN" \
  -p sdk_src:="$REALMAN_SRC" \
  -p urdf_file:="$ROOT/rm_65.urdf"
