"""Launch configured RealSense cameras, or validate YAML with --check-config."""

import argparse
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

import yaml


DEFAULT_CONFIG = Path(__file__).resolve().with_name("config.yaml")
TOPIC_FIELDS = ("image_topic", "compressed_topic", "camera_info_topic")


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silently overwritten mapping keys."""


def _unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("YAML mapping keys must be strings")
        if key in mapping:
            raise ValueError(f"Duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def validate_cameras(document):
    if not isinstance(document, dict) or document.keys() != {"cameras"}:
        raise ValueError("YAML root must contain exactly one key: cameras")
    configured = document["cameras"]
    if not isinstance(configured, list) or not configured:
        raise ValueError("cameras must be a non-empty list")
    required = {"id", "name", "serial", "enabled", "color_module", "color_profile", *TOPIC_FIELDS}
    seen = {key: set() for key in ("id", "name", "serial")}
    seen_topics = set()
    cameras = []
    for index, camera in enumerate(configured):
        label = f"cameras[{index}]"
        if not isinstance(camera, dict):
            raise ValueError(f"{label} must be a mapping")
        if camera.keys() != required:
            raise ValueError(f"{label} must contain exactly: {', '.join(sorted(required))}")
        if type(camera["id"]) is not int or camera["id"] <= 0:
            raise ValueError(f"{label}.id must be a positive integer")
        if not isinstance(camera["name"], str) or not re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_]*", camera["name"]
        ):
            raise ValueError(f"{label}.name must be a label with letters, digits, underscores; no leading digit")
        if not isinstance(camera["serial"], str) or not re.fullmatch(r"[0-9]+", camera["serial"]):
            raise ValueError(f"{label}.serial must be a quoted string of digits")
        if type(camera["enabled"]) is not bool:
            raise ValueError(f"{label}.enabled must be true or false (without quotes)")
        if camera["color_module"] not in ("rgb_camera", "depth_module"):
            raise ValueError(f"{label}.color_module must be rgb_camera or depth_module")
        if not isinstance(camera["color_profile"], str) or not re.fullmatch(
            r"[1-9][0-9]*x[1-9][0-9]*x[1-9][0-9]*", camera["color_profile"]
        ):
            raise ValueError(f"{label}.color_profile must be WIDTHxHEIGHTxFPS with positive integers")
        for key in TOPIC_FIELDS:
            topic = camera[key]
            if not isinstance(topic, str) or not re.fullmatch(
                r"/[A-Za-z_][A-Za-z0-9_]*(?:/[A-Za-z_][A-Za-z0-9_]*)*", topic
            ):
                raise ValueError(f"{label}.{key} must be a full absolute ROS topic with valid name segments")
            if topic in seen_topics:
                raise ValueError(f"{label}.{key} is duplicated: {topic}")
            seen_topics.add(topic)
        for key in seen:
            if camera[key] in seen[key]:
                raise ValueError(f"{label}.{key} is duplicated: {camera[key]}")
            seen[key].add(camera[key])
        cameras.append(dict(camera))
    if not any(camera["enabled"] for camera in cameras):
        raise ValueError("At least one camera must be enabled")
    return tuple(cameras)


def load_cameras(path=DEFAULT_CONFIG):
    """Return validated camera mappings; no ROS imports or hardware access."""
    path = Path(path)
    try:
        with path.open(encoding="utf-8-sig") as stream:
            document = yaml.load(stream, Loader=UniqueKeyLoader)
        return validate_cameras(document)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        raise ValueError(f"{path}: {exc}") from exc



def _load_cameras():
    return load_cameras()


def _managed_camera_pids(cameras):
    node_names = {f"__node:=cam{camera['id']}" for camera in cameras}
    pids = []
    for process in os.scandir("/proc"):
        if not process.name.isdigit():
            continue
        try:
            with open(f"/proc/{process.name}/cmdline", "rb") as cmdline_file:
                arguments = [
                    argument.decode(errors="replace")
                    for argument in cmdline_file.read().split(b"\0")
                    if argument
                ]
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
        if (
            arguments
            and os.path.basename(arguments[0]) == "realsense2_camera_node"
            and node_names.intersection(arguments)
        ):
            pids.append(int(process.name))
    return pids


def _stop_old_camera_nodes(cameras):
    pids = _managed_camera_pids(cameras)
    if not pids:
        return

    print(f"[realsense] stopping old configured camera nodes: {pids}")
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        remaining = _managed_camera_pids(cameras)
        if not remaining:
            return
        time.sleep(0.1)

    print(f"[realsense] force stopping unresponsive nodes: {remaining}")
    for pid in remaining:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        if not _managed_camera_pids(cameras):
            return
        time.sleep(0.1)
    raise RuntimeError("old configured camera nodes could not be stopped")


def _discover_devices():
    try:
        result = subprocess.run(
            ["rs-enumerate-devices", "-s"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        return [], f"RealSense discovery failed: {exc}"

    devices = {}
    for line in result.stdout.splitlines():
        columns = re.split(r"\s{2,}", line.strip())
        if len(columns) >= 2 and columns[1].isdigit():
            devices[columns[1]] = columns[0]

    return sorted(devices.items()), None


def _camera_group(camera):
    from launch.actions import GroupAction, IncludeLaunchDescription
    from launch.launch_description_sources import PythonLaunchDescriptionSource
    from ament_index_python.packages import get_package_share_directory
    from launch_ros.actions import SetRemap

    idx = camera["id"]
    serial = camera["serial"]
    color_module = camera["color_module"]
    color_profile = camera["color_profile"]
    camera_prefix = f"/cam{idx}/cam{idx}/color/"
    return GroupAction(
        actions=[
            SetRemap(src=camera_prefix + "image_raw", dst=camera["image_topic"]),
            SetRemap(
                src=camera_prefix + "image_raw/compressed",
                dst=camera["compressed_topic"],
            ),
            SetRemap(
                src=camera_prefix + "camera_info",
                dst=camera["camera_info_topic"],
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory("realsense2_camera"),
                        "launch",
                        "rs_launch.py",
                    )
                ),
                launch_arguments={
                    "camera_namespace": f"cam{idx}",
                    "camera_name": f"cam{idx}",
                    "serial_no": f"_{serial}",
                    "enable_color": "true",
                    f"{color_module}.color_profile": color_profile,
                    f"{color_module}.color_format": "RGB8",
                    "enable_depth": "false",
                    "publish_tf": "false",
                }.items(),
            ),
        ]
    )


def generate_launch_description():
    # Validate before stopping any processes or accessing devices.
    cameras = _load_cameras()
    from launch import LaunchDescription
    from launch.actions import LogInfo

    _stop_old_camera_nodes(cameras)
    devices, error = _discover_devices()
    if error:
        return LaunchDescription([LogInfo(msg=f"[realsense] {error}; no camera started")])
    if not devices:
        return LaunchDescription(
            [LogInfo(msg="[realsense] no connected RealSense device; no camera started")]
        )

    connected_devices = dict(devices)
    actions = [LogInfo(msg=f"[realsense] detected {len(devices)} device(s)")]
    for camera in cameras:
        idx = camera["id"]
        observation_name = camera["name"]
        serial = camera["serial"]
        color_profile = camera["color_profile"]
        if not camera["enabled"]:
            actions.append(LogInfo(msg=f"[realsense] cam{idx}: {observation_name} disabled; skipped"))
            continue
        name = connected_devices.get(serial)
        if name is None:
            actions.append(
                LogInfo(
                    msg=(
                        f"[realsense] cam{idx}: {observation_name} ({serial}) "
                        "not connected; skipped"
                    )
                )
            )
            continue
        actions.append(
            LogInfo(
                msg=(
                    f"[realsense] cam{idx}: {name} ({serial}) "
                    f"name={observation_name} [{color_profile} RGB8]\n"
                    f"  image_topic: {camera['image_topic']}\n"
                    f"  compressed_topic: {camera['compressed_topic']}\n"
                    f"  camera_info_topic: {camera['camera_info_topic']}"
                )
            )
        )
        actions.append(_camera_group(camera))
    extra_devices = set(connected_devices) - {camera["serial"] for camera in cameras}
    if extra_devices:
        actions.append(
            LogInfo(
                msg=(
                    f"[realsense] {len(extra_devices)} unconfigured device(s) "
                    "ignored; see cameras in config.yaml"
                )
            )
        )
    return LaunchDescription(actions)


def main():
    parser = argparse.ArgumentParser(description="Validate config.yaml without ROS or hardware")
    parser.add_argument("--check-config", action="store_true", help="Check YAML without ROS or hardware")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="YAML file to check")
    args = parser.parse_args()
    if not args.check_config:
        parser.error("Use --check-config for validation; start cameras using launch.sh")
    try:
        cameras = load_cameras(args.config)
    except ValueError as exc:
        print(f"[camera-config] ERROR: {exc}", file=sys.stderr)
        return 1
    for camera in cameras:
        state = "enabled" if camera["enabled"] else "disabled"
        print(
            f"[camera-config] {state}: cam{camera['id']} name={camera['name']} "
            f"serial={camera['serial']} [{camera['color_module']} {camera['color_profile']} RGB8]"
        )
        for key in TOPIC_FIELDS:
            print(f"  {key}: {camera[key]}")
    print("[camera-config] PASS: configuration only; device support and connectivity not checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
