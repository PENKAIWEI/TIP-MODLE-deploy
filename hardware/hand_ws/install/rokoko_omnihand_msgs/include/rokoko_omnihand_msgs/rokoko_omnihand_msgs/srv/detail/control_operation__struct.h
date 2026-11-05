// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rokoko_omnihand_msgs:srv/ControlOperation.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/srv/control_operation.h"


#ifndef ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__STRUCT_H_
#define ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/ControlOperation in the package rokoko_omnihand_msgs.
typedef struct rokoko_omnihand_msgs__srv__ControlOperation_Request
{
  uint8_t structure_needs_at_least_one_member;
} rokoko_omnihand_msgs__srv__ControlOperation_Request;

// Struct for a sequence of rokoko_omnihand_msgs__srv__ControlOperation_Request.
typedef struct rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence
{
  rokoko_omnihand_msgs__srv__ControlOperation_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence;

// Constants defined in the message

/// Constant 'CLEAR_FAULT_SUCCESS'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_SUCCESS = 30
};

/// Constant 'CLEAR_FAULT_ALREADY_CLEAR'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_ALREADY_CLEAR = 31
};

/// Constant 'CLEAR_FAULT_REJECTED_CONTROL_STATE'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_CONTROL_STATE = 40
};

/// Constant 'CLEAR_FAULT_REJECTED_COMMUNICATION_UNHEALTHY'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_COMMUNICATION_UNHEALTHY = 41
};

/// Constant 'CLEAR_FAULT_REJECTED_ERROR_QUERY_TIMEOUT'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_ERROR_QUERY_TIMEOUT = 42
};

/// Constant 'CLEAR_FAULT_REJECTED_ERROR_STATUS_INVALID'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_ERROR_STATUS_INVALID = 43
};

/// Constant 'CLEAR_FAULT_REJECTED_HARDWARE_ERROR_PRESENT'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_HARDWARE_ERROR_PRESENT = 44
};

/// Constant 'CLEAR_FAULT_REJECTED_FEEDBACK_READ_TIMEOUT'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_FEEDBACK_READ_TIMEOUT = 45
};

/// Constant 'CLEAR_FAULT_REJECTED_FEEDBACK_INVALID'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_FEEDBACK_INVALID = 46
};

/// Constant 'CLEAR_FAULT_REJECTED_LIMITER_INIT_FAILED'.
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response__CLEAR_FAULT_REJECTED_LIMITER_INIT_FAILED = 47
};

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"
// Member 'state'
#include "rokoko_omnihand_msgs/msg/detail/o10_control_state__struct.h"

/// Struct defined in srv/ControlOperation in the package rokoko_omnihand_msgs.
typedef struct rokoko_omnihand_msgs__srv__ControlOperation_Response
{
  bool success;
  uint8_t result_code;
  rosidl_runtime_c__String message;
  rokoko_omnihand_msgs__msg__O10ControlState state;
} rokoko_omnihand_msgs__srv__ControlOperation_Response;

// Struct for a sequence of rokoko_omnihand_msgs__srv__ControlOperation_Response.
typedef struct rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence
{
  rokoko_omnihand_msgs__srv__ControlOperation_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Event__request__MAX_SIZE = 1
};
// response
enum
{
  rokoko_omnihand_msgs__srv__ControlOperation_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/ControlOperation in the package rokoko_omnihand_msgs.
typedef struct rokoko_omnihand_msgs__srv__ControlOperation_Event
{
  service_msgs__msg__ServiceEventInfo info;
  rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence request;
  rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence response;
} rokoko_omnihand_msgs__srv__ControlOperation_Event;

// Struct for a sequence of rokoko_omnihand_msgs__srv__ControlOperation_Event.
typedef struct rokoko_omnihand_msgs__srv__ControlOperation_Event__Sequence
{
  rokoko_omnihand_msgs__srv__ControlOperation_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__srv__ControlOperation_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__STRUCT_H_
