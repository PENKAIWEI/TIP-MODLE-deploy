// generated from rosidl_generator_c/resource/idl__type_support.h.em
// with input from rokoko_omnihand_msgs:srv/ReadO10ActiveJoints.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/srv/read_o10_active_joints.h"


#ifndef ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__TYPE_SUPPORT_H_
#define ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__TYPE_SUPPORT_H_

#include "rosidl_typesupport_interface/macros.h"

#include "rokoko_omnihand_msgs/msg/rosidl_generator_c__visibility_control.h"

#ifdef __cplusplus
extern "C"
{
#endif

#include "rosidl_runtime_c/message_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  rokoko_omnihand_msgs,
  srv,
  ReadO10ActiveJoints_Request
)(void);

// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  rokoko_omnihand_msgs,
  srv,
  ReadO10ActiveJoints_Response
)(void);

// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  rokoko_omnihand_msgs,
  srv,
  ReadO10ActiveJoints_Event
)(void);

#include "rosidl_runtime_c/service_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
  rosidl_typesupport_c,
  rokoko_omnihand_msgs,
  srv,
  ReadO10ActiveJoints
)(void);

// Forward declare the function to create a service event message for this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
void *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  rokoko_omnihand_msgs,
  srv,
  ReadO10ActiveJoints
)(
  const rosidl_service_introspection_info_t * info,
  rcutils_allocator_t * allocator,
  const void * request_message,
  const void * response_message);

// Forward declare the function to destroy a service event message for this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
bool
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  rokoko_omnihand_msgs,
  srv,
  ReadO10ActiveJoints
)(
  void * event_msg,
  rcutils_allocator_t * allocator);

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__TYPE_SUPPORT_H_
