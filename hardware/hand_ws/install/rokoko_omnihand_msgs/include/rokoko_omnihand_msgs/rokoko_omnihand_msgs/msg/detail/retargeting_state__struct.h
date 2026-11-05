// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rokoko_omnihand_msgs:msg/RetargetingState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/retargeting_state.h"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__STRUCT_H_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'PHASE_INITIALIZING'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_INITIALIZING = 0
};

/// Constant 'PHASE_COLLECTING_LENGTHS'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_COLLECTING_LENGTHS = 1
};

/// Constant 'PHASE_WAITING_FIRST_VALID_IK'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_WAITING_FIRST_VALID_IK = 2
};

/// Constant 'PHASE_TRACKING'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_TRACKING = 3
};

/// Constant 'PHASE_STALE'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_STALE = 4
};

/// Constant 'PHASE_RECOVERY_CONFIRMING'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_RECOVERY_CONFIRMING = 5
};

/// Constant 'PHASE_RECOVERY_RESUMING'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_RECOVERY_RESUMING = 6
};

/// Constant 'PHASE_MODEL_ERROR'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__PHASE_MODEL_ERROR = 7
};

/// Constant 'LENGTH_COLLECTING'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__LENGTH_COLLECTING = 0
};

/// Constant 'LENGTH_FROZEN'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__LENGTH_FROZEN = 1
};

/// Constant 'LENGTH_CURRENT_INVALID'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__LENGTH_CURRENT_INVALID = 2
};

/// Constant 'IK_UNINITIALIZED'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_UNINITIALIZED = 0
};

/// Constant 'IK_VALID'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_VALID = 1
};

/// Constant 'IK_INPUT_INVALID'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_INPUT_INVALID = 2
};

/// Constant 'IK_SIDE_INVALID'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_SIDE_INVALID = 3
};

/// Constant 'IK_RESIDUAL_EXCEEDED'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_RESIDUAL_EXCEEDED = 4
};

/// Constant 'IK_SOLVER_ERROR'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_SOLVER_ERROR = 5
};

/// Constant 'IK_NOT_RUN_LENGTH_COLLECTING'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_NOT_RUN_LENGTH_COLLECTING = 6
};

/// Constant 'IK_NOT_RUN_STALE'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_NOT_RUN_STALE = 7
};

/// Constant 'IK_MAPPING_VALID'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_MAPPING_VALID = 8
};

/// Constant 'IK_MAPPING_REJECTED'.
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__IK_MAPPING_REJECTED = 9
};

/// Constant 'SOLVER_NOT_RUN'.
/**
  * Named wire value for a finger whose solver was not executed.
 */
enum
{
  rokoko_omnihand_msgs__msg__RetargetingState__SOLVER_NOT_RUN = 0
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'side'
#include "rosidl_runtime_c/string.h"
// Member 'input_stamp'
// Member 'solve_finished_stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/RetargetingState in the package rokoko_omnihand_msgs.
/**
  * RetargetingState — per-side retargeting diagnostics.
  * Wire contract: DOCS/01_知识/05_手部重定向状态ROS接口契约.md.
  * This is a read-only diagnostic interface; it does not participate in O10
  * control decisions.
 */
typedef struct rokoko_omnihand_msgs__msg__RetargetingState
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String side;
  builtin_interfaces__msg__Time input_stamp;
  bool solve_executed;
  builtin_interfaces__msg__Time solve_finished_stamp;
  double solve_duration_sec;
  uint8_t phase;
  bool ready;
  bool stale;
  bool command_published;
  uint8_t length_state[5];
  uint8_t ik_state[5];
  /// Legacy field name: in mapping mode the thumb element reports mapping
  /// validity; use ik_state to distinguish mapping from an IK solve.
  bool has_valid_ik[5];
  bool used_previous_valid_target[5];
  bool residual_available[5];
  double normalized_residual[5];
  bool target_projection_applied[5];
  bool target_projection_distance_available[5];
  double normalized_target_projection_distance[5];
  int32_t solver_result_code[5];
  uint32_t solver_evaluations[5];
  uint32_t recovery_valid_count;
  double recovery_valid_duration_sec;
} rokoko_omnihand_msgs__msg__RetargetingState;

// Struct for a sequence of rokoko_omnihand_msgs__msg__RetargetingState.
typedef struct rokoko_omnihand_msgs__msg__RetargetingState__Sequence
{
  rokoko_omnihand_msgs__msg__RetargetingState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__msg__RetargetingState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__STRUCT_H_
