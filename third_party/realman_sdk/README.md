# RealMan SDK

`src/Robotic_Arm/` is the bundled RM65 Python SDK and `libapi_c.so` used by
`hardware/arm_ws/arm_model_control`. The arm launch script passes this exact
`src` path as `sdk_src` and verifies the imported module resolves here.
The original wrapper documentation is preserved in `UPSTREAM_README.md`.

Platform: Linux x86_64, Python 3.12, glibc compatible with Ubuntu 24.04.
This directory contains the SDK library; ROS 2 and operating system libraries
remain platform dependencies.
