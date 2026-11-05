// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rokoko_omnihand_msgs:srv/ReadO10ActiveJoints.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/srv/read_o10_active_joints.h"


#ifndef ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__STRUCT_H_
#define ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/ReadO10ActiveJoints in the package rokoko_omnihand_msgs.
typedef struct rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request
{
  uint8_t structure_needs_at_least_one_member;
} rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request;

// Struct for a sequence of rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request.
typedef struct rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence;

// Constants defined in the message

/// Constant 'READ_SUCCESS'.
enum
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__READ_SUCCESS = 0
};

/// Constant 'READ_DEVICE_UNAVAILABLE'.
enum
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__READ_DEVICE_UNAVAILABLE = 1
};

/// Constant 'READ_HARDWARE_ERROR'.
enum
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__READ_HARDWARE_ERROR = 2
};

/// Constant 'READ_INVALID_RESULT'.
enum
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__READ_INVALID_RESULT = 3
};

/// Constant 'READ_INTERNAL_ERROR'.
enum
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__READ_INTERNAL_ERROR = 4
};

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"
// Member 'sample_stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in srv/ReadO10ActiveJoints in the package rokoko_omnihand_msgs.
typedef struct rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response
{
  bool success;
  uint8_t result_code;
  rosidl_runtime_c__String message;
  builtin_interfaces__msg__Time sample_stamp;
  double position[10];
} rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response;

// Struct for a sequence of rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response.
typedef struct rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event__request__MAX_SIZE = 1
};
// response
enum
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/ReadO10ActiveJoints in the package rokoko_omnihand_msgs.
typedef struct rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event
{
  service_msgs__msg__ServiceEventInfo info;
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence request;
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence response;
} rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event;

// Struct for a sequence of rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event.
typedef struct rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event__Sequence
{
  rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__STRUCT_H_
