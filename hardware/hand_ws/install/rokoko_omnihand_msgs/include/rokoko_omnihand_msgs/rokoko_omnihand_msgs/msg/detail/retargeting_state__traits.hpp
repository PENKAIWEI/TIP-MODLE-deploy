// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from rokoko_omnihand_msgs:msg/RetargetingState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/retargeting_state.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__TRAITS_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "rokoko_omnihand_msgs/msg/detail/retargeting_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'input_stamp'
// Member 'solve_finished_stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace rokoko_omnihand_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const RetargetingState & msg,
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

  // member: input_stamp
  {
    out << "input_stamp: ";
    to_flow_style_yaml(msg.input_stamp, out);
    out << ", ";
  }

  // member: solve_executed
  {
    out << "solve_executed: ";
    rosidl_generator_traits::value_to_yaml(msg.solve_executed, out);
    out << ", ";
  }

  // member: solve_finished_stamp
  {
    out << "solve_finished_stamp: ";
    to_flow_style_yaml(msg.solve_finished_stamp, out);
    out << ", ";
  }

  // member: solve_duration_sec
  {
    out << "solve_duration_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.solve_duration_sec, out);
    out << ", ";
  }

  // member: phase
  {
    out << "phase: ";
    rosidl_generator_traits::value_to_yaml(msg.phase, out);
    out << ", ";
  }

  // member: ready
  {
    out << "ready: ";
    rosidl_generator_traits::value_to_yaml(msg.ready, out);
    out << ", ";
  }

  // member: stale
  {
    out << "stale: ";
    rosidl_generator_traits::value_to_yaml(msg.stale, out);
    out << ", ";
  }

  // member: command_published
  {
    out << "command_published: ";
    rosidl_generator_traits::value_to_yaml(msg.command_published, out);
    out << ", ";
  }

  // member: length_state
  {
    if (msg.length_state.size() == 0) {
      out << "length_state: []";
    } else {
      out << "length_state: [";
      size_t pending_items = msg.length_state.size();
      for (auto item : msg.length_state) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: ik_state
  {
    if (msg.ik_state.size() == 0) {
      out << "ik_state: []";
    } else {
      out << "ik_state: [";
      size_t pending_items = msg.ik_state.size();
      for (auto item : msg.ik_state) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: has_valid_ik
  {
    if (msg.has_valid_ik.size() == 0) {
      out << "has_valid_ik: []";
    } else {
      out << "has_valid_ik: [";
      size_t pending_items = msg.has_valid_ik.size();
      for (auto item : msg.has_valid_ik) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: used_previous_valid_target
  {
    if (msg.used_previous_valid_target.size() == 0) {
      out << "used_previous_valid_target: []";
    } else {
      out << "used_previous_valid_target: [";
      size_t pending_items = msg.used_previous_valid_target.size();
      for (auto item : msg.used_previous_valid_target) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: residual_available
  {
    if (msg.residual_available.size() == 0) {
      out << "residual_available: []";
    } else {
      out << "residual_available: [";
      size_t pending_items = msg.residual_available.size();
      for (auto item : msg.residual_available) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: normalized_residual
  {
    if (msg.normalized_residual.size() == 0) {
      out << "normalized_residual: []";
    } else {
      out << "normalized_residual: [";
      size_t pending_items = msg.normalized_residual.size();
      for (auto item : msg.normalized_residual) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: target_projection_applied
  {
    if (msg.target_projection_applied.size() == 0) {
      out << "target_projection_applied: []";
    } else {
      out << "target_projection_applied: [";
      size_t pending_items = msg.target_projection_applied.size();
      for (auto item : msg.target_projection_applied) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: target_projection_distance_available
  {
    if (msg.target_projection_distance_available.size() == 0) {
      out << "target_projection_distance_available: []";
    } else {
      out << "target_projection_distance_available: [";
      size_t pending_items = msg.target_projection_distance_available.size();
      for (auto item : msg.target_projection_distance_available) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: normalized_target_projection_distance
  {
    if (msg.normalized_target_projection_distance.size() == 0) {
      out << "normalized_target_projection_distance: []";
    } else {
      out << "normalized_target_projection_distance: [";
      size_t pending_items = msg.normalized_target_projection_distance.size();
      for (auto item : msg.normalized_target_projection_distance) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: solver_result_code
  {
    if (msg.solver_result_code.size() == 0) {
      out << "solver_result_code: []";
    } else {
      out << "solver_result_code: [";
      size_t pending_items = msg.solver_result_code.size();
      for (auto item : msg.solver_result_code) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: solver_evaluations
  {
    if (msg.solver_evaluations.size() == 0) {
      out << "solver_evaluations: []";
    } else {
      out << "solver_evaluations: [";
      size_t pending_items = msg.solver_evaluations.size();
      for (auto item : msg.solver_evaluations) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: recovery_valid_count
  {
    out << "recovery_valid_count: ";
    rosidl_generator_traits::value_to_yaml(msg.recovery_valid_count, out);
    out << ", ";
  }

  // member: recovery_valid_duration_sec
  {
    out << "recovery_valid_duration_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.recovery_valid_duration_sec, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RetargetingState & msg,
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

  // member: input_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "input_stamp:\n";
    to_block_style_yaml(msg.input_stamp, out, indentation + 2);
  }

  // member: solve_executed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "solve_executed: ";
    rosidl_generator_traits::value_to_yaml(msg.solve_executed, out);
    out << "\n";
  }

  // member: solve_finished_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "solve_finished_stamp:\n";
    to_block_style_yaml(msg.solve_finished_stamp, out, indentation + 2);
  }

  // member: solve_duration_sec
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "solve_duration_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.solve_duration_sec, out);
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

  // member: ready
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "ready: ";
    rosidl_generator_traits::value_to_yaml(msg.ready, out);
    out << "\n";
  }

  // member: stale
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stale: ";
    rosidl_generator_traits::value_to_yaml(msg.stale, out);
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

  // member: length_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.length_state.size() == 0) {
      out << "length_state: []\n";
    } else {
      out << "length_state:\n";
      for (auto item : msg.length_state) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: ik_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.ik_state.size() == 0) {
      out << "ik_state: []\n";
    } else {
      out << "ik_state:\n";
      for (auto item : msg.ik_state) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: has_valid_ik
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.has_valid_ik.size() == 0) {
      out << "has_valid_ik: []\n";
    } else {
      out << "has_valid_ik:\n";
      for (auto item : msg.has_valid_ik) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: used_previous_valid_target
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.used_previous_valid_target.size() == 0) {
      out << "used_previous_valid_target: []\n";
    } else {
      out << "used_previous_valid_target:\n";
      for (auto item : msg.used_previous_valid_target) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: residual_available
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.residual_available.size() == 0) {
      out << "residual_available: []\n";
    } else {
      out << "residual_available:\n";
      for (auto item : msg.residual_available) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: normalized_residual
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.normalized_residual.size() == 0) {
      out << "normalized_residual: []\n";
    } else {
      out << "normalized_residual:\n";
      for (auto item : msg.normalized_residual) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: target_projection_applied
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_projection_applied.size() == 0) {
      out << "target_projection_applied: []\n";
    } else {
      out << "target_projection_applied:\n";
      for (auto item : msg.target_projection_applied) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: target_projection_distance_available
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_projection_distance_available.size() == 0) {
      out << "target_projection_distance_available: []\n";
    } else {
      out << "target_projection_distance_available:\n";
      for (auto item : msg.target_projection_distance_available) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: normalized_target_projection_distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.normalized_target_projection_distance.size() == 0) {
      out << "normalized_target_projection_distance: []\n";
    } else {
      out << "normalized_target_projection_distance:\n";
      for (auto item : msg.normalized_target_projection_distance) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: solver_result_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.solver_result_code.size() == 0) {
      out << "solver_result_code: []\n";
    } else {
      out << "solver_result_code:\n";
      for (auto item : msg.solver_result_code) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: solver_evaluations
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.solver_evaluations.size() == 0) {
      out << "solver_evaluations: []\n";
    } else {
      out << "solver_evaluations:\n";
      for (auto item : msg.solver_evaluations) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: recovery_valid_count
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "recovery_valid_count: ";
    rosidl_generator_traits::value_to_yaml(msg.recovery_valid_count, out);
    out << "\n";
  }

  // member: recovery_valid_duration_sec
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "recovery_valid_duration_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.recovery_valid_duration_sec, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RetargetingState & msg, bool use_flow_style = false)
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
  const rokoko_omnihand_msgs::msg::RetargetingState & msg,
  std::ostream & out, size_t indentation = 0)
{
  rokoko_omnihand_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rokoko_omnihand_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const rokoko_omnihand_msgs::msg::RetargetingState & msg)
{
  return rokoko_omnihand_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<rokoko_omnihand_msgs::msg::RetargetingState>()
{
  return "rokoko_omnihand_msgs::msg::RetargetingState";
}

template<>
inline const char * name<rokoko_omnihand_msgs::msg::RetargetingState>()
{
  return "rokoko_omnihand_msgs/msg/RetargetingState";
}

template<>
struct has_fixed_size<rokoko_omnihand_msgs::msg::RetargetingState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rokoko_omnihand_msgs::msg::RetargetingState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<rokoko_omnihand_msgs::msg::RetargetingState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__TRAITS_HPP_
