# RealSense ROS 2 packages

Bundled Ubuntu 24.04 / ROS 2 Jazzy debs:

- `ros-jazzy-realsense2-camera`
- `ros-jazzy-realsense2-camera-msgs`

Install with:

```bash
sudo dpkg -i third_party/realsense/debs/*.deb
sudo apt-get -f install -y
```

The camera launch then uses the packages already in `/opt/ros/jazzy`; no separate
`REALSENSE_WS_SETUP` is needed. If a local RealSense workspace exists, set
`REALSENSE_WS_SETUP=/path/to/install/setup.bash` to override.

Runtime dependencies `librealsense2` and udev rules must be present in the base
environment; the debs depend on them.
