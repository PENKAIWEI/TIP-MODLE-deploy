cmake_minimum_required(VERSION 3.10)
project(rokoko_omnihand_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

# This package owns the wire schema and the numeric enum values for the
# Rokoko-to-OmniHand O10 teleoperation system (architecture invariant A16).
# It owns no nodes, algorithms, state or config defaults.
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RawHandFrame.msg"
  "msg/RetargetingState.msg"
  "msg/O10ControlState.msg"
  "srv/ReadO10ActiveJoints.srv"
  "srv/ControlOperation.srv"
  DEPENDENCIES std_msgs geometry_msgs builtin_interfaces
)


ament_package()
