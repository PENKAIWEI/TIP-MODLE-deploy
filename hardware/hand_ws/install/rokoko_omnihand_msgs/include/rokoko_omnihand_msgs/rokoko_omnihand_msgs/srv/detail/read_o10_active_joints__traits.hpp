// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from rokoko_omnihand_msgs:srv/ReadO10ActiveJoints.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/srv/read_o10_active_joints.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__TRAITS_HPP_
#define ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "rokoko_omnihand_msgs/srv/detail/read_o10_active_joints__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace rokoko_omnihand_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ReadO10ActiveJoints_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ReadO10ActiveJoints_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ReadO10ActiveJoints_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace rokoko_omnihand_msgs

namespace rosidl_generator_traits
{

[[deprecated("use rokoko_omnihand_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  rokoko_omnihand_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rokoko_omnihand_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request & msg)
{
  return rokoko_omnihand_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>()
{
  return "rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request";
}

template<>
inline const char * name<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>()
{
  return "rokoko_omnihand_msgs/srv/ReadO10ActiveJoints_Request";
}

template<>
struct has_fixed_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'sample_stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace rokoko_omnihand_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ReadO10ActiveJoints_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: result_code
  {
    out << "result_code: ";
    rosidl_generator_traits::value_to_yaml(msg.result_code, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: sample_stamp
  {
    out << "sample_stamp: ";
    to_flow_style_yaml(msg.sample_stamp, out);
    out << ", ";
  }

  // member: position
  {
    if (msg.position.size() == 0) {
      out << "position: []";
    } else {
      out << "position: [";
      size_t pending_items = msg.position.size();
      for (auto item : msg.position) {
        rosidl_generator_traits::value_to_yaml(item, out);
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
  const ReadO10ActiveJoints_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: result_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result_code: ";
    rosidl_generator_traits::value_to_yaml(msg.result_code, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }

  // member: sample_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sample_stamp:\n";
    to_block_style_yaml(msg.sample_stamp, out, indentation + 2);
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.position.size() == 0) {
      out << "position: []\n";
    } else {
      out << "position:\n";
      for (auto item : msg.position) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ReadO10ActiveJoints_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace rokoko_omnihand_msgs

namespace rosidl_generator_traits
{

[[deprecated("use rokoko_omnihand_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  rokoko_omnihand_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rokoko_omnihand_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response & msg)
{
  return rokoko_omnihand_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>()
{
  return "rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response";
}

template<>
inline const char * name<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>()
{
  return "rokoko_omnihand_msgs/srv/ReadO10ActiveJoints_Response";
}

template<>
struct has_fixed_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace rokoko_omnihand_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ReadO10ActiveJoints_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
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
  const ReadO10ActiveJoints_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ReadO10ActiveJoints_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace rokoko_omnihand_msgs

namespace rosidl_generator_traits
{

[[deprecated("use rokoko_omnihand_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  rokoko_omnihand_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use rokoko_omnihand_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event & msg)
{
  return rokoko_omnihand_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event>()
{
  return "rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event";
}

template<>
inline const char * name<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event>()
{
  return "rokoko_omnihand_msgs/srv/ReadO10ActiveJoints_Event";
}

template<>
struct has_fixed_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event>
  : std::integral_constant<bool, has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>::value && has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints>()
{
  return "rokoko_omnihand_msgs::srv::ReadO10ActiveJoints";
}

template<>
inline const char * name<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints>()
{
  return "rokoko_omnihand_msgs/srv/ReadO10ActiveJoints";
}

template<>
struct has_fixed_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints>
  : std::integral_constant<
    bool,
    has_fixed_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>::value &&
    has_fixed_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>::value
  >
{
};

template<>
struct has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints>
  : std::integral_constant<
    bool,
    has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>::value &&
    has_bounded_size<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>::value
  >
{
};

template<>
struct is_service<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints>
  : std::true_type
{
};

template<>
struct is_service_request<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Request>
  : std::true_type
{
};

template<>
struct is_service_response<rokoko_omnihand_msgs::srv::ReadO10ActiveJoints_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__READ_O10_ACTIVE_JOINTS__TRAITS_HPP_
