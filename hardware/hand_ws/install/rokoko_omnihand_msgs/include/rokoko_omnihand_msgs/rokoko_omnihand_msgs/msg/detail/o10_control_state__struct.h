// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rokoko_omnihand_msgs:msg/O10ControlState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/o10_control_state.h"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__STRUCT_H_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'EVENT_STARTUP'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_STARTUP = 0
};

/// Constant 'EVENT_TARGET_PROCESSED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_TARGET_PROCESSED = 1
};

/// Constant 'EVENT_TARGET_TIMEOUT'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_TARGET_TIMEOUT = 2
};

/// Constant 'EVENT_FEEDBACK_RECEIVED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_FEEDBACK_RECEIVED = 3
};

/// Constant 'EVENT_ERROR_STATUS_RECEIVED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_ERROR_STATUS_RECEIVED = 4
};

/// Constant 'EVENT_OPERATOR_REQUEST'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_OPERATOR_REQUEST = 5
};

/// Constant 'EVENT_FAULT_CHANGED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_FAULT_CHANGED = 6
};

/// Constant 'EVENT_COMPONENT_STATE_CHANGED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__EVENT_COMPONENT_STATE_CHANGED = 7
};

/// Constant 'PHASE_INITIALIZING'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__PHASE_INITIALIZING = 0
};

/// Constant 'PHASE_IDLE_NOT_READY'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__PHASE_IDLE_NOT_READY = 1
};

/// Constant 'PHASE_IDLE_READY'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__PHASE_IDLE_READY = 2
};

/// Constant 'PHASE_ACTIVE'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__PHASE_ACTIVE = 3
};

/// Constant 'PHASE_PAUSED_TARGET_STALE'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__PHASE_PAUSED_TARGET_STALE = 4
};

/// Constant 'PHASE_FAULT_LATCHED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__PHASE_FAULT_LATCHED = 5
};

/// Constant 'TARGET_NOT_EVALUATED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_NOT_EVALUATED = 0
};

/// Constant 'TARGET_SENT'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_SENT = 1
};

/// Constant 'TARGET_VALID_MOTION_DISABLED'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_VALID_MOTION_DISABLED = 2
};

/// Constant 'TARGET_REJECTED_SCHEMA'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_REJECTED_SCHEMA = 3
};

/// Constant 'TARGET_REJECTED_NAME_ORDER'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_REJECTED_NAME_ORDER = 4
};

/// Constant 'TARGET_REJECTED_NONFINITE'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_REJECTED_NONFINITE = 5
};

/// Constant 'TARGET_REJECTED_LIMIT'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_REJECTED_LIMIT = 6
};

/// Constant 'TARGET_REJECTED_AUX_FIELDS'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_REJECTED_AUX_FIELDS = 7
};

/// Constant 'TARGET_REJECTED_TIMESTAMP'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_REJECTED_TIMESTAMP = 8
};

/// Constant 'TARGET_REJECTED_CONTROL_STATE'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__TARGET_REJECTED_CONTROL_STATE = 9
};

/// Constant 'FAULT_HARDWARE_ERROR'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__FAULT_HARDWARE_ERROR = 1ul
};

/// Constant 'FAULT_COMMAND_READBACK_TIMEOUT'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__FAULT_COMMAND_READBACK_TIMEOUT = 2ul
};

/// Constant 'FAULT_INVALID_FEEDBACK'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__FAULT_INVALID_FEEDBACK = 4ul
};

/// Constant 'FAULT_SAFETY_INVARIANT'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__FAULT_SAFETY_INVARIANT = 8ul
};

/// Constant 'FAULT_COMPONENT_RESTART_OR_DISCONNECT'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__FAULT_COMPONENT_RESTART_OR_DISCONNECT = 16ul
};

/// Constant 'FAULT_ERROR_MONITOR_TIMEOUT'.
enum
{
  rokoko_omnihand_msgs__msg__O10ControlState__FAULT_ERROR_MONITOR_TIMEOUT = 32ul
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'side'
#include "rosidl_runtime_c/string.h"
// Member 'last_target_input_stamp'
// Member 'last_target_received_stamp'
// Member 'last_command_sent_stamp'
// Member 'last_feedback_received_stamp'
// Member 'last_error_status_received_stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/O10ControlState in the package rokoko_omnihand_msgs.
/**
  * O10ControlState — per-side control diagnostics.
  * Wire contract: DOCS/01_知识/06_O10控制状态ROS接口契约.md.
  * This is a read-only diagnostic interface; it does not participate in control
  * decisions.
 */
typedef struct rokoko_omnihand_msgs__msg__O10ControlState
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String side;
  uint8_t event;
  uint8_t phase;
  bool feedback_ready;
  bool error_monitor_ready;
  bool target_ready;
  bool target_fresh;
  bool fault_latched;
  bool motion_enabled;
  uint8_t target_result;
  bool command_published;
  bool slew_limited[10];
  uint32_t fault_reason_mask;
  uint16_t hardware_error_bits[10];
  bool target_time_available;
  builtin_interfaces__msg__Time last_target_input_stamp;
  builtin_interfaces__msg__Time last_target_received_stamp;
  bool command_time_available;
  builtin_interfaces__msg__Time last_command_sent_stamp;
  bool feedback_time_available;
  builtin_interfaces__msg__Time last_feedback_received_stamp;
  bool error_status_time_available;
  builtin_interfaces__msg__Time last_error_status_received_stamp;
} rokoko_omnihand_msgs__msg__O10ControlState;

// Struct for a sequence of rokoko_omnihand_msgs__msg__O10ControlState.
typedef struct rokoko_omnihand_msgs__msg__O10ControlState__Sequence
{
  rokoko_omnihand_msgs__msg__O10ControlState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__msg__O10ControlState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__STRUCT_H_
