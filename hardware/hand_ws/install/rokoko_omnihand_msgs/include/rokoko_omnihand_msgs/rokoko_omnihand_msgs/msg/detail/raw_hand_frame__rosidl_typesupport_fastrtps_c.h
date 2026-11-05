// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from rokoko_omnihand_msgs:msg/RawHandFrame.idl
// generated code does not contain a copyright notice
#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "rokoko_omnihand_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "rokoko_omnihand_msgs/msg/detail/raw_hand_frame__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
bool cdr_serialize_rokoko_omnihand_msgs__msg__RawHandFrame(
  const rokoko_omnihand_msgs__msg__RawHandFrame * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
bool cdr_deserialize_rokoko_omnihand_msgs__msg__RawHandFrame(
  eprosima::fastcdr::Cdr &,
  rokoko_omnihand_msgs__msg__RawHandFrame * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
size_t get_serialized_size_rokoko_omnihand_msgs__msg__RawHandFrame(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
size_t max_serialized_size_rokoko_omnihand_msgs__msg__RawHandFrame(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
bool cdr_serialize_key_rokoko_omnihand_msgs__msg__RawHandFrame(
  const rokoko_omnihand_msgs__msg__RawHandFrame * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
size_t get_serialized_size_key_rokoko_omnihand_msgs__msg__RawHandFrame(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
size_t max_serialized_size_key_rokoko_omnihand_msgs__msg__RawHandFrame(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, rokoko_omnihand_msgs, msg, RawHandFrame)();

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
