#!/usr/bin/env bash
# 不要用 set -u：source ROS setup.bash 会读未定义变量（如 AMENT_TRACE_SETUP_FILES）
set -eo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LAUNCH_PID=""
GUARD_PID=""
STOPPING=0

ROS_SETUP="${ROS_SETUP:-/opt/ros/jazzy/setup.bash}"
source "$ROS_SETUP"
if [[ -z "${REALSENSE_WS_SETUP:-}" && -f "/home/hit/node_ws/install/setup.bash" ]]; then
    REALSENSE_WS_SETUP="/home/hit/node_ws/install/setup.bash"
fi
if [[ -n "${REALSENSE_WS_SETUP:-}" ]]; then
    source "$REALSENSE_WS_SETUP"
fi

launch_group_is_alive() {
    [[ -n "$LAUNCH_PID" ]] && kill -0 -- "-$LAUNCH_PID" 2>/dev/null
}

stop_launch_group() {
    if (( STOPPING )); then
        return
    fi
    STOPPING=1

    if launch_group_is_alive; then
        echo "[realsense] stopping camera process group $LAUNCH_PID"
        kill -INT -- "-$LAUNCH_PID" 2>/dev/null || true
        for _ in {1..50}; do
            launch_group_is_alive || break
            sleep 0.1
        done
    fi

    if launch_group_is_alive; then
        echo "[realsense] WARN: graceful stop timed out; sending SIGTERM"
        kill -TERM -- "-$LAUNCH_PID" 2>/dev/null || true
        for _ in {1..30}; do
            launch_group_is_alive || break
            sleep 0.1
        done
    fi

    if launch_group_is_alive; then
        echo "[realsense] WARN: forced stop required; sending SIGKILL"
        kill -KILL -- "-$LAUNCH_PID" 2>/dev/null || true
    fi

    if [[ -n "$GUARD_PID" ]]; then
        kill -TERM -- "-$GUARD_PID" 2>/dev/null || true
        wait "$GUARD_PID" 2>/dev/null || true
    fi
    if [[ -n "$LAUNCH_PID" ]]; then
        wait "$LAUNCH_PID" 2>/dev/null || true
    fi
}

handle_signal() {
    stop_launch_group
    exit 130
}

handle_exit() {
    status=$?
    trap - EXIT
    stop_launch_group
    exit "$status"
}

trap handle_signal INT TERM HUP
trap handle_exit EXIT

echo "[realsense] starting supervised camera launch"
setsid ros2 launch "$SCRIPT_DIR/rs_4cam.launch.py" "$@" &
LAUNCH_PID=$!

# 独立会话中的守护进程处理本脚本被 SIGKILL 后无法执行 trap 的情况。
setsid bash -c '
owner_pid=$1
launch_pgid=$2
while kill -0 "$owner_pid" 2>/dev/null; do
    sleep 0.2
done
if kill -0 -- "-$launch_pgid" 2>/dev/null; then
    kill -INT -- "-$launch_pgid" 2>/dev/null || true
    for _ in {1..50}; do
        kill -0 -- "-$launch_pgid" 2>/dev/null || exit 0
        sleep 0.1
    done
    kill -TERM -- "-$launch_pgid" 2>/dev/null || true
    for _ in {1..30}; do
        kill -0 -- "-$launch_pgid" 2>/dev/null || exit 0
        sleep 0.1
    done
    kill -KILL -- "-$launch_pgid" 2>/dev/null || true
fi
' realsense-launch-guard "$$" "$LAUNCH_PID" >/dev/null 2>&1 &
GUARD_PID=$!

echo "[realsense] supervisor active (launch pid=$LAUNCH_PID); press Ctrl-C to stop all cameras"
if wait "$LAUNCH_PID"; then
    STATUS=0
else
    STATUS=$?
fi

# ros2 launch 不论正常或异常返回，都不能留下同一进程组内的相机节点。
stop_launch_group
trap - EXIT INT TERM HUP
exit "$STATUS"
