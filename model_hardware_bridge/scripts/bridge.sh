#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
DEPLOY="${TIP_DEPLOY_ROOT:-$(dirname -- "$ROOT")}"
export TIP_DEPLOY_ROOT="$DEPLOY"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
PYTHON="${TIP_BRIDGE_PYTHON:-/usr/bin/python3}"
mode="${1:-help}"
if (( $# )); then shift; fi
case "$mode" in
  check)
    exec "$PYTHON" -m tip_bridge.inspect_config "$@" ;;
  model-status)
    exec "$PYTHON" -c 'import json; from tip_bridge.common import rpc; print(json.dumps(rpc("/status"), indent=2))' ;;
  stop)
    mkdir -p "$ROOT/runs"
    touch "$ROOT/runs/STOP"
    echo 'Requested bridge stop; arms stop through their native command watchdog.'
    exit 0 ;;
  observe|reset|infer)
    for setup in "${ROS_SETUP:-/opt/ros/jazzy/setup.bash}" "$DEPLOY/hardware/hand_ws/install/setup.bash"; do
      [[ -f "$setup" ]] || { echo "missing setup: $setup" >&2; exit 2; }
      set +u
      source "$setup"
      set -u
    done
    if [[ -n "${TIP_OPENPI_SRC:-}" ]]; then
      [[ -f "$TIP_OPENPI_SRC/openpi/fastslow/buffer.py" ]] || { echo 'TIP_OPENPI_SRC must contain openpi/fastslow/buffer.py' >&2; exit 2; }
      export PYTHONPATH="$ROOT:$TIP_OPENPI_SRC${PYTHONPATH:+:$PYTHONPATH}"
    fi
    exec "$PYTHON" -m tip_bridge.controller "$mode" "$@" ;;
  *)
    cat <<'EOF'
Usage (from TIP_demo_deploy):
  bash model_hardware_bridge/scripts/bridge.sh check
  bash model_hardware_bridge/scripts/bridge.sh observe --duration 5
  bash model_hardware_bridge/scripts/bridge.sh model-status
  bash model_hardware_bridge/scripts/bridge.sh reset [--execute --confirm-motion]
  bash model_hardware_bridge/scripts/bridge.sh infer [--execute --confirm-motion] [--duration 10]
  bash model_hardware_bridge/scripts/bridge.sh stop
Hardware receivers must be started through their existing hardware/* launchers.
Only explicit --execute --confirm-motion allows reset/infer to publish actions.
EOF
    ;;
esac
