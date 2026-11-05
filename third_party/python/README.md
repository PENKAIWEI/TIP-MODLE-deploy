# Arm Python runtime dependencies

Bundled from this host's Python 3.12 installation:

- NumPy 2.5.1, including `numpy.libs/` native dependencies.
- Ruckig 0.19.4, Linux x86_64 CPython 3.12 extension.

`hardware/arm_ws/start_model_control.sh` prepends this directory to `PYTHONPATH`,
disables the user site, and checks the actual import paths before starting the
arm node. ROS 2 packages and Python standard library remain system dependencies.
