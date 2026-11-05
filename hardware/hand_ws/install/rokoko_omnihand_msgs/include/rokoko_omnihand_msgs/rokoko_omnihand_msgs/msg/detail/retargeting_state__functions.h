// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from rokoko_omnihand_msgs:msg/RetargetingState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/retargeting_state.h"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__FUNCTIONS_H_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "rokoko_omnihand_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "rokoko_omnihand_msgs/msg/detail/retargeting_state__struct.h"

/// Initialize msg/RetargetingState message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * rokoko_omnihand_msgs__msg__RetargetingState
 * )) before or use
 * rokoko_omnihand_msgs__msg__RetargetingState__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
bool
rokoko_omnihand_msgs__msg__RetargetingState__init(rokoko_omnihand_msgs__msg__RetargetingState * msg);

/// Finalize msg/RetargetingState message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
void
rokoko_omnihand_msgs__msg__RetargetingState__fini(rokoko_omnihand_msgs__msg__RetargetingState * msg);

/// Create msg/RetargetingState message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * rokoko_omnihand_msgs__msg__RetargetingState__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
rokoko_omnihand_msgs__msg__RetargetingState *
rokoko_omnihand_msgs__msg__RetargetingState__create(void);

/// Destroy msg/RetargetingState message.
/**
 * It calls
 * rokoko_omnihand_msgs__msg__RetargetingState__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
void
rokoko_omnihand_msgs__msg__RetargetingState__destroy(rokoko_omnihand_msgs__msg__RetargetingState * msg);

/// Check for msg/RetargetingState message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
bool
rokoko_omnihand_msgs__msg__RetargetingState__are_equal(const rokoko_omnihand_msgs__msg__RetargetingState * lhs, const rokoko_omnihand_msgs__msg__RetargetingState * rhs);

/// Copy a msg/RetargetingState message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
bool
rokoko_omnihand_msgs__msg__RetargetingState__copy(
  const rokoko_omnihand_msgs__msg__RetargetingState * input,
  rokoko_omnihand_msgs__msg__RetargetingState * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_type_hash_t *
rokoko_omnihand_msgs__msg__RetargetingState__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_runtime_c__type_description__TypeDescription *
rokoko_omnihand_msgs__msg__RetargetingState__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_runtime_c__type_description__TypeSource *
rokoko_omnihand_msgs__msg__RetargetingState__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
const rosidl_runtime_c__type_description__TypeSource__Sequence *
rokoko_omnihand_msgs__msg__RetargetingState__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of msg/RetargetingState messages.
/**
 * It allocates the memory for the number of elements and calls
 * rokoko_omnihand_msgs__msg__RetargetingState__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
bool
rokoko_omnihand_msgs__msg__RetargetingState__Sequence__init(rokoko_omnihand_msgs__msg__RetargetingState__Sequence * array, size_t size);

/// Finalize array of msg/RetargetingState messages.
/**
 * It calls
 * rokoko_omnihand_msgs__msg__RetargetingState__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
void
rokoko_omnihand_msgs__msg__RetargetingState__Sequence__fini(rokoko_omnihand_msgs__msg__RetargetingState__Sequence * array);

/// Create array of msg/RetargetingState messages.
/**
 * It allocates the memory for the array and calls
 * rokoko_omnihand_msgs__msg__RetargetingState__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
rokoko_omnihand_msgs__msg__RetargetingState__Sequence *
rokoko_omnihand_msgs__msg__RetargetingState__Sequence__create(size_t size);

/// Destroy array of msg/RetargetingState messages.
/**
 * It calls
 * rokoko_omnihand_msgs__msg__RetargetingState__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
void
rokoko_omnihand_msgs__msg__RetargetingState__Sequence__destroy(rokoko_omnihand_msgs__msg__RetargetingState__Sequence * array);

/// Check for msg/RetargetingState message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
bool
rokoko_omnihand_msgs__msg__RetargetingState__Sequence__are_equal(const rokoko_omnihand_msgs__msg__RetargetingState__Sequence * lhs, const rokoko_omnihand_msgs__msg__RetargetingState__Sequence * rhs);

/// Copy an array of msg/RetargetingState messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_rokoko_omnihand_msgs
bool
rokoko_omnihand_msgs__msg__RetargetingState__Sequence__copy(
  const rokoko_omnihand_msgs__msg__RetargetingState__Sequence * input,
  rokoko_omnihand_msgs__msg__RetargetingState__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__FUNCTIONS_H_
