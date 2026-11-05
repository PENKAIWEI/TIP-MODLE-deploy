// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from rokoko_omnihand_msgs:msg/RawHandFrame.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/raw_hand_frame.h"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__STRUCT_H_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'actor_name'
// Member 'node_names'
#include "rosidl_runtime_c/string.h"
// Member 'positions'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'orientations'
#include "geometry_msgs/msg/detail/quaternion__struct.h"

/// Struct defined in msg/RawHandFrame in the package rokoko_omnihand_msgs.
/**
  * RawHandFrame — per-side Rokoko raw hand frame published by the Rokoko receiver
  * node on /rokoko/{left,right}/raw_hand. Read-only source data for retargeting.
  *
  * Hand side is expressed by the Topic name, NOT by a field here (Spec decision 5).
  * The canonical 21 Rokoko node spellings are NOT owned by this package; they are
  * fixed by the versioned official JSON v3 fixture in rokoko_hand_receiver. This
  * message only carries the 21 names/positions/quaternions as data arrays, already
  * reordered into the project canonical order (Spec decision 6):
  *   Hand, then Thumb/Index/Middle/Ring/Little, each Proximal/Medial/Distal/Tip.
 */
typedef struct rokoko_omnihand_msgs__msg__RawHandFrame
{
  /// stamp = local ROS time at which the UDP datagram was received on this host
  /// (Spec decisions 4, 50). frame_id is set by the publisher and is not used to
  /// encode the hand side.
  std_msgs__msg__Header header;
  /// The single Rokoko Actor selected for this run (Spec decision 3). One run
  /// selects exactly one Actor (configurable index, default 0).
  uint32_t actor_index;
  rosidl_runtime_c__String actor_name;
  /// Scene-level source timestamp carried VERBATIM from the Rokoko source (Spec
  /// decisions 4, 50). Its epoch/unit is UNCONFIRMED: it MUST NOT be converted to
  /// ROS time, subtracted from ROS time or used for control timing.
  double source_timestamp;
  /// Canonical-ordered 21 node data arrays (Spec decisions 5, 6, 49).
  /// Positions are Rokoko world coordinates, unmodified: no re-relativization,
  /// mirroring, filtering or normalization (Spec decision 7).
  /// Orientations are x, y, z, w quaternions, unmodified (Spec decision 7).
  rosidl_runtime_c__String node_names[21];
  geometry_msgs__msg__Point positions[21];
  geometry_msgs__msg__Quaternion orientations[21];
} rokoko_omnihand_msgs__msg__RawHandFrame;

// Struct for a sequence of rokoko_omnihand_msgs__msg__RawHandFrame.
typedef struct rokoko_omnihand_msgs__msg__RawHandFrame__Sequence
{
  rokoko_omnihand_msgs__msg__RawHandFrame * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} rokoko_omnihand_msgs__msg__RawHandFrame__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__STRUCT_H_
