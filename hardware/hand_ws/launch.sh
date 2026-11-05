#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
DEPLOY_ROOT="$(cd -- "$ROOT/../.." && pwd -P)"
SDK_ROOT="$DEPLOY_ROOT/third_party/omnihand_sdk"
CONFIG="$ROOT/config/hand.json"
ROS_SETUP="${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
CHECK_ONLY=0
CONFIRM_MOTION=0

usage() {
  echo 'Usage: bash hardware/hand_ws/launch.sh --check-only | --confirm-motion'
}
fail() { echo "[hand] ERROR: $*" >&2; exit 2; }

for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    --confirm-motion) CONFIRM_MOTION=1 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; fail "unknown option: $arg" ;;
  esac
done
((CHECK_ONLY == 0 || CONFIRM_MOTION == 0)) || fail 'choose one mode'

[[ -f "$CONFIG" ]] || fail "missing $CONFIG"
command -v python3 >/dev/null || fail 'python3 is required to read hand.json'
# Transfer validated JSON values as data; never execute configuration contents.
CONFIG_VALUES="$(python3 - "$CONFIG" <<'PY'
import json
import math
import re
import sys
from decimal import Decimal


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate field: {key}")
        result[key] = value
    return result


try:
    with open(sys.argv[1], encoding="utf-8-sig") as stream:
        config = json.load(stream, object_pairs_hook=unique_object)
    if not isinstance(config, dict):
        raise ValueError("configuration must be a JSON object")
    allowed = {
        "hand_sides", "left_hcan_serial_number",
        "right_hcan_serial_number", "tactile_rate_hz",
    }
    unknown = config.keys() - allowed
    if unknown:
        raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
    sides = config.get("hand_sides")
    if sides not in ("left", "right", "both"):
        raise ValueError("hand_sides must be left, right or both")
    rate = config.get("tactile_rate_hz")
    if type(rate) not in (int, float) or not math.isfinite(rate) or rate < 0:
        raise ValueError("tactile_rate_hz must be a finite nonnegative JSON number")
    serials = []
    for side in ("left", "right"):
        key = f"{side}_hcan_serial_number"
        serial = config.get(key, "")
        if key in config or sides in (side, "both"):
            if not isinstance(serial, str) or re.fullmatch(r"[0-9]+", serial) is None:
                raise ValueError(f"{key} must be a nonempty string of digits")
        serials.append(serial)
    if sides == "both" and serials[0] == serials[1]:
        raise ValueError("HCAN serials must differ")
    # Fixed decimal form works with ROS YAML; normalize every zero spelling.
    rate_text = format(Decimal(str(rate)), "f") if rate else "0"
except (OSError, UnicodeError, ValueError, OverflowError) as error:
    print(f"[hand] ERROR: {sys.argv[1]}: {error}", file=sys.stderr)
    sys.exit(2)

print(sides)
print(*serials, sep="\n")
print(rate_text)
PY
)" || fail 'could not load hand.json'
mapfile -t CONFIG_FIELDS <<<"$CONFIG_VALUES"
HAND_SIDES="${CONFIG_FIELDS[0]}"
LEFT_HCAN_SERIAL_NUMBER="${CONFIG_FIELDS[1]}"
RIGHT_HCAN_SERIAL_NUMBER="${CONFIG_FIELDS[2]}"
TACTILE_RATE_HZ="${CONFIG_FIELDS[3]}"
selected() { [[ "$HAND_SIDES" == both || "$HAND_SIDES" == "$1" ]]; }

for path in \
  "$ROOT/src/collection/o10_contracts/package.xml" \
  "$ROOT/src/collection/ros_interfaces/package.xml" \
  "$ROOT/src/collection/omnihand_o10_control_node/package.xml" \
  "$ROOT/src/collection/omnihand_o10_hardware_provider_node/package.xml" \
  "$SDK_ROOT/omnihand/__init__.py" \
  "$SDK_ROOT/omnihand/omnihand_core.cpython-312-x86_64-linux-gnu.so"; do
  [[ -f "$path" ]] || fail "missing $path"
done

if ((CHECK_ONLY)); then
  echo "[hand] configuration OK: sides=$HAND_SIDES, tactile=${TACTILE_RATE_HZ}Hz"
  echo '[hand] This checks files and configuration only; no ROS node or hardware is started.'
  exit 0
fi
((CONFIRM_MOTION)) || fail 'physical commands are possible; pass --confirm-motion'
[[ -f "$ROS_SETUP" ]] || fail "missing ROS setup: $ROS_SETUP"
[[ -f "$ROOT/install/setup.bash" ]] || fail 'workspace is not built; run bash hardware/hand_ws/build.sh'
command -v setsid >/dev/null || fail 'setsid is required'
command -v timeout >/dev/null || fail 'timeout is required'

set +u
source "$ROS_SETUP"
source "$ROOT/install/setup.bash"
set -u

export PYTHONNOUSERSITE=1
export PYTHONPATH="$SDK_ROOT${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="$SDK_ROOT/omnihand${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
RUNTIME_PREFIX="${DEXHIT_COLLECTION_PREFIX:-${CONDA_PREFIX:-}}"
if [[ -n "$RUNTIME_PREFIX" ]]; then
  [[ -d "$RUNTIME_PREFIX/lib/python3.12/site-packages" ]] || fail "invalid Python 3.12 environment: $RUNTIME_PREFIX"
  export PYTHONPATH="$RUNTIME_PREFIX/lib/python3.12/site-packages:$PYTHONPATH"
  export LD_LIBRARY_PATH="$RUNTIME_PREFIX/lib:$LD_LIBRARY_PATH"
fi
command -v ros2 >/dev/null || fail 'ros2 is required'
/usr/bin/python3 -c 'import numpy, omnihand, rokoko_omnihand_msgs' \
  || fail 'Python cannot import numpy, OmniHand SDK, or ROS message package'

existing_nodes="$(timeout 10 ros2 node list 2>/dev/null || true)"
for node in /omnihand_o10_hardware_provider /o10_control_node; do
  if grep -Fxq "$node" <<<"$existing_nodes"; then
    fail "$node is already running"
  fi
done

LOG_DIR="${OMNIHAND_LOG_DIR:-${TMPDIR:-/tmp}/tip-hand-$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$LOG_DIR"
PIDS=()
cleanup() {
  local pid
  trap - EXIT INT TERM
  for pid in "${PIDS[@]}"; do
    kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null || true
  done
  for pid in "${PIDS[@]}"; do wait "$pid" 2>/dev/null || true; done
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

wait_for_node() {
  local expected="$1" pid="$2" attempts
  for ((attempts=0; attempts<30; attempts++)); do
    kill -0 "$pid" 2>/dev/null || fail "$expected exited; inspect $LOG_DIR"
    if timeout 5 ros2 node list 2>/dev/null | grep -Fxq "$expected"; then return 0; fi
    sleep 1
  done
  fail "$expected did not appear; inspect $LOG_DIR"
}

PROVIDER=(--ros-args -p "sides:=$HAND_SIDES")
if selected left; then
  PROVIDER+=(
    -p o10.left.transport:=hcan
    -p o10.left.hand_device_id:=1
    -p o10.left.canfd_channel_id:=0
    -p "o10.left.hcan_serial_number:='$LEFT_HCAN_SERIAL_NUMBER'"
  )
fi
if selected right; then
  PROVIDER+=(
    -p o10.right.transport:=hcan
    -p o10.right.hand_device_id:=1
    -p o10.right.canfd_channel_id:=0
    -p "o10.right.hcan_serial_number:='$RIGHT_HCAN_SERIAL_NUMBER'"
  )
fi
setsid ros2 run omnihand_o10_hardware_adapter omnihand_o10_hardware_provider \
  "${PROVIDER[@]}" >"$LOG_DIR/provider.log" 2>&1 &
PIDS+=("$!")
wait_for_node /omnihand_o10_hardware_provider "${PIDS[-1]}"

CONTROL=(--ros-args -p "sides:=$HAND_SIDES")
add_control_params() {
  local side="$1"
  CONTROL+=(
    -p "${side}.max_joint_rates:=[8.221747440645,12.055238476275,6.011412609369,1.171863926339,10.596641887108,10.596641887108,1.209263838882,10.596641887108,1.321463576510,10.596641887108]"
    -p "${side}.max_time_credit:=0.1"
    -p "${side}.slew_compare_epsilon:=[0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001]"
    -p "${side}.target_input_stale_timeout:=2.0"
    -p "${side}.target_receive_stale_timeout:=2.0"
    -p "${side}.control_check_period:=0.05"
    -p "${side}.error_poll_period:=0.2"
    -p "${side}.error_query_timeout:=2.0"
    -p "${side}.command_readback_timeout:=4.0"
    -p "${side}.provider_heartbeat_timeout:=5.0"
    -p "${side}.init_read_retry_period:=0.1"
    -p "${side}.init_error_retry_period:=0.1"
    -p "${side}.read_service_timeout:=1.0"
    -p "${side}.clear_fault_error_timeout:=1.0"
    -p "${side}.clear_fault_read_timeout:=1.0"
  )
}
if selected left; then add_control_params left; fi
if selected right; then add_control_params right; fi
setsid ros2 run omnihand_o10_control o10_control_node \
  "${CONTROL[@]}" >"$LOG_DIR/control.log" 2>&1 &
PIDS+=("$!")
wait_for_node /o10_control_node "${PIDS[-1]}"

if [[ "$TACTILE_RATE_HZ" != 0 ]]; then
  for side in left right; do
    if selected "$side"; then
      timeout 10 ros2 topic pub --once "/o10/$side/tactile_cmd" \
        std_msgs/msg/Float32 "{data: $TACTILE_RATE_HZ}" >/dev/null \
        || fail "could not enable $side tactile stream"
    fi
  done
fi

echo "[hand] running: sides=$HAND_SIDES; logs=$LOG_DIR"
echo '[hand] Bridge publishes /o10_control/{side}/command; Ctrl-C stops both nodes.'
while true; do
  for pid in "${PIDS[@]}"; do
    kill -0 "$pid" 2>/dev/null || fail "a child exited; inspect $LOG_DIR"
  done
  sleep 2
done
