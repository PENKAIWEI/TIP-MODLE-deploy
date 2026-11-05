# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target rokoko_omnihand_msgs::rokoko_omnihand_msgs
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${rokoko_omnihand_msgs_TARGETS}.
if(rokoko_omnihand_msgs_TARGETS AND NOT TARGET rokoko_omnihand_msgs::rokoko_omnihand_msgs)
  add_library(rokoko_omnihand_msgs::rokoko_omnihand_msgs INTERFACE IMPORTED)
  set_target_properties(rokoko_omnihand_msgs::rokoko_omnihand_msgs PROPERTIES
    INTERFACE_LINK_LIBRARIES "${rokoko_omnihand_msgs_TARGETS}")
endif()
