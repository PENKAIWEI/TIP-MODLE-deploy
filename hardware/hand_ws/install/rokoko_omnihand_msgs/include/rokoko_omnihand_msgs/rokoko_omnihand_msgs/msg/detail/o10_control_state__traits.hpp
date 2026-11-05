// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from rokoko_omnihand_msgs:msg/O10ControlState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/o10_control_state.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__TRAITS_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "rokoko_omnihand_msgs/msg/detail/o10_control_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'last_target_input_stamp'
// Member 'last_target_received_stamp'
// Member 'last_command_sent_stamp'
// Member 'last_feedback_received_stamp'
// Member 'last_error_status_received_stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace rokoko_omnihand_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const O10ControlState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: side
  {
    out << "side: ";
    rosidl_generator_traits::value_to_yaml(msg.side, out);
    out << ", ";
  }

  // member: event
  {
    out << "event: ";
    rosidl_generator_traits::value_to_yaml(msg.event, out);
    out << ", ";
  }

  // member: phase
  {
    out << "phase: ";
    rosidl_generator_traits::value_to_yaml(msg.phase, out);
    out << ", ";
  }

  // member: feedback_ready
  {
    out << "feedback_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.feedback_ready, out);
    out << ", ";
  }

  // member: error_monitor_ready
  {
    out << "error_monitor_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.error_monitor_ready, out);
    out << ", ";
  }

  // member: target_ready
  {
    out << "target_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.target_ready, out);
    out << ", ";
  }

  // member: target_fresh
  {
    out << "target_fresh: ";
    rosidl_generator_traits::value_to_yaml(msg.target_fresh, out);
    out << ", ";
  }

  // member: fault_latched
  {
    out << "fault_latched: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_latched, out);
    out << ", ";
  }

  // member: motion_enabled
  {
    out << "motion_enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.motion_enabled, out);
    out << ", ";
  }

  // member: target_result
  {
    out << "target_result: ";
    rosidl_generator_traits::value_to_yaml(msg.target_result, out);
    out << ", ";
  }

  // member: command_published
  {
    out << "command_published: ";
    rosidl_generator_traits::value_to_yaml(msg.command_published, out);
    out << ", ";
  }

  // member: slew_limited
  {
    if (msg.slew_limited.size() == 0) {
      out << "slew_limited: []";
    } else {
      out << "slew_limited: [";
      size_t pending_items = msg.slew_limited.size();
      for (auto item : msg.slew_limited) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: fault_reason_mask
  {
    out << "fault_reason_mask: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_reason_mask, out);
    out << ", ";
  }

  // member: hardware_error_bits
  {
    if (msg.hardware_error_bits.size() == 0) {
      out << "hardware_error_bits: []";
    } else {
      out << "hardware_error_bits: [";
      size_t pending_items = msg.hardware_error_bits.size();
      for (auto item : msg.hardware_error_bits) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: target_time_available
  {
    out << "target_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.target_time_available, out);
    out << ", ";
  }

  // member: last_target_input_stamp
  {
    out << "last_target_input_stamp: ";
    to_flow_style_yaml(msg.last_target_input_stamp, out);
    out << ", ";
  }

  // member: last_target_received_stamp
  {
    out << "last_target_received_stamp: ";
    to_flow_style_yaml(msg.last_target_received_stamp, out);
    out << ", ";
  }

  // member: command_time_available
  {
    out << "command_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.command_time_available, out);
    out << ", ";
  }

  // member: last_command_sent_stamp
  {
    out << "last_command_sent_stamp: ";
    to_flow_style_yaml(msg.last_command_sent_stamp, out);
    out << ", ";
  }

  // member: feedback_time_available
  {
    out << "feedback_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.feedback_time_available, out);
    out << ", ";
  }

  // member: last_feedback_received_stamp
  {
    out << "last_feedback_received_stamp: ";
    to_flow_style_yaml(msg.last_feedback_received_stamp, out);
    out << ", ";
  }

  // member: error_status_time_available
  {
    out << "error_status_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.error_status_time_available, out);
    out << ", ";
  }

  // member: last_error_status_received_stamp
  {
    out << "last_error_status_received_stamp: ";
    to_flow_style_yaml(msg.last_error_status_received_stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const O10ControlState & msg,
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

  // member: side
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "side: ";
    rosidl_generator_traits::value_to_yaml(msg.side, out);
    out << "\n";
  }

  // member: event
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "event: ";
    rosidl_generator_traits::value_to_yaml(msg.event, out);
    out << "\n";
  }

  // member: phase
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "phase: ";
    rosidl_generator_traits::value_to_yaml(msg.phase, out);
    out << "\n";
  }

  // member: feedback_ready
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.feedback_ready, out);
    out << "\n";
  }

  // member: error_monitor_ready
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_monitor_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.error_monitor_ready, out);
    out << "\n";
  }

  // member: target_ready
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.target_ready, out);
    out << "\n";
  }

  // member: target_fresh
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_fresh: ";
    rosidl_generator_traits::value_to_yaml(msg.target_fresh, out);
    out << "\n";
  }

  // member: fault_latched
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fault_latched: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_latched, out);
    out << "\n";
  }

  // member: motion_enabled
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "motion_enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.motion_enabled, out);
    out << "\n";
  }

  // member: target_result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_result: ";
    rosidl_generator_traits::value_to_yaml(msg.target_result, out);
    out << "\n";
  }

  // member: command_published
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "command_published: ";
    rosidl_generator_traits::value_to_yaml(msg.command_published, out);
    out << "\n";
  }

  // member: slew_limited
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.slew_limited.size() == 0) {
      out << "slew_limited: []\n";
    } else {
      out << "slew_limited:\n";
      for (auto item : msg.slew_limited) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: fault_reason_mask
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fault_reason_mask: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_reason_mask, out);
    out << "\n";
  }

  // member: hardware_error_bits
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.hardware_error_bits.size() == 0) {
      out << "hardware_error_bits: []\n";
    } else {
      out << "hardware_error_bits:\n";
      for (auto item : msg.hardware_error_bits) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: target_time_available
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.target_time_available, out);
    out << "\n";
  }

  // member: last_target_input_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "last_target_input_stamp:\n";
    to_block_style_yaml(msg.last_target_input_stamp, out, indentation + 2);
  }

  // member: last_target_received_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "last_target_received_stamp:\n";
    to_block_style_yaml(msg.last_target_received_stamp, out, indentation + 2);
  }

  // member: command_time_available
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "command_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.command_time_available, out);
    out << "\n";
  }

  // member: last_command_sent_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "last_command_sent_stamp:\n";
    to_block_style_yaml(msg.last_command_sent_stamp, out, indentation + 2);
  }

  // member: feedback_time_available
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.feedback_time_available, out);
    out << "\n";
  }

  // member: last_feedback_received_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "last_feedback_received_stamp:\n";
    to_block_style_yaml(msg.last_feedback_received_stamp, out, indentation + 2);
  }

  // member: error_status_time_available
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_status_time_available: ";
    rosidl_generator_traits::value_to_yaml(msg.error_status_time_available, out);
    out << "\n";
  }

  // member: last_error_status_received_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "last_error_status_received_stamp:\n";
    to_block_style_yaml(msg.last_error_status_received_stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const O10ControlState & msg, bool use_flow_style = false)
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
  const rokoko_omnihand_msgs::msg::O10ControlState & msg,
  std::ostream & out, size_t indentation = 0)
{
  rokoko_omnihand_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rokoko_omnihand_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const rokoko_omnihand_msgs::msg::O10ControlState & msg)
{
  return rokoko_omnihand_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<rokoko_omnihand_msgs::msg::O10ControlState>()
{
  return "rokoko_omnihand_msgs::msg::O10ControlState";
}

template<>
inline const char * name<rokoko_omnihand_msgs::msg::O10ControlState>()
{
  return "rokoko_omnihand_msgs/msg/O10ControlState";
}

template<>
struct has_fixed_size<rokoko_omnihand_msgs::msg::O10ControlState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rokoko_omnihand_msgs::msg::O10ControlState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<rokoko_omnihand_msgs::msg::O10ControlState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__TRAITS_HPP_
