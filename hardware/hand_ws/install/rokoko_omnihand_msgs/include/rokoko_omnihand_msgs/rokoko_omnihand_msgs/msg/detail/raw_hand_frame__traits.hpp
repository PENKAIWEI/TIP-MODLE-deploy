// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from rokoko_omnihand_msgs:msg/RawHandFrame.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/raw_hand_frame.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__TRAITS_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "rokoko_omnihand_msgs/msg/detail/raw_hand_frame__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'positions'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'orientations'
#include "geometry_msgs/msg/detail/quaternion__traits.hpp"

namespace rokoko_omnihand_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const RawHandFrame & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: actor_index
  {
    out << "actor_index: ";
    rosidl_generator_traits::value_to_yaml(msg.actor_index, out);
    out << ", ";
  }

  // member: actor_name
  {
    out << "actor_name: ";
    rosidl_generator_traits::value_to_yaml(msg.actor_name, out);
    out << ", ";
  }

  // member: source_timestamp
  {
    out << "source_timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.source_timestamp, out);
    out << ", ";
  }

  // member: node_names
  {
    if (msg.node_names.size() == 0) {
      out << "node_names: []";
    } else {
      out << "node_names: [";
      size_t pending_items = msg.node_names.size();
      for (auto item : msg.node_names) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: positions
  {
    if (msg.positions.size() == 0) {
      out << "positions: []";
    } else {
      out << "positions: [";
      size_t pending_items = msg.positions.size();
      for (auto item : msg.positions) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: orientations
  {
    if (msg.orientations.size() == 0) {
      out << "orientations: []";
    } else {
      out << "orientations: [";
      size_t pending_items = msg.orientations.size();
      for (auto item : msg.orientations) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RawHandFrame & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: actor_index
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "actor_index: ";
    rosidl_generator_traits::value_to_yaml(msg.actor_index, out);
    out << "\n";
  }

  // member: actor_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "actor_name: ";
    rosidl_generator_traits::value_to_yaml(msg.actor_name, out);
    out << "\n";
  }

  // member: source_timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "source_timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.source_timestamp, out);
    out << "\n";
  }

  // member: node_names
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.node_names.size() == 0) {
      out << "node_names: []\n";
    } else {
      out << "node_names:\n";
      for (auto item : msg.node_names) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.positions.size() == 0) {
      out << "positions: []\n";
    } else {
      out << "positions:\n";
      for (auto item : msg.positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: orientations
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.orientations.size() == 0) {
      out << "orientations: []\n";
    } else {
      out << "orientations:\n";
      for (auto item : msg.orientations) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RawHandFrame & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace rokoko_omnihand_msgs

namespace rosidl_generator_traits
{

[[deprecated("use rokoko_omnihand_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const rokoko_omnihand_msgs::msg::RawHandFrame & msg,
  std::ostream & out, size_t indentation = 0)
{
  rokoko_omnihand_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rokoko_omnihand_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const rokoko_omnihand_msgs::msg::RawHandFrame & msg)
{
  return rokoko_omnihand_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<rokoko_omnihand_msgs::msg::RawHandFrame>()
{
  return "rokoko_omnihand_msgs::msg::RawHandFrame";
}

template<>
inline const char * name<rokoko_omnihand_msgs::msg::RawHandFrame>()
{
  return "rokoko_omnihand_msgs/msg/RawHandFrame";
}

template<>
struct has_fixed_size<rokoko_omnihand_msgs::msg::RawHandFrame>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rokoko_omnihand_msgs::msg::RawHandFrame>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<rokoko_omnihand_msgs::msg::RawHandFrame>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__TRAITS_HPP_
