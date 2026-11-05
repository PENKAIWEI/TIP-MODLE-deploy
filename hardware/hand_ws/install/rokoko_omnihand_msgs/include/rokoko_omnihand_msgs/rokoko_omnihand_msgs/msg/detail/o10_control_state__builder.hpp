// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rokoko_omnihand_msgs:msg/O10ControlState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/o10_control_state.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__BUILDER_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rokoko_omnihand_msgs/msg/detail/o10_control_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rokoko_omnihand_msgs
{

namespace msg
{

namespace builder
{

class Init_O10ControlState_last_error_status_received_stamp
{
public:
  explicit Init_O10ControlState_last_error_status_received_stamp(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  ::rokoko_omnihand_msgs::msg::O10ControlState last_error_status_received_stamp(::rokoko_omnihand_msgs::msg::O10ControlState::_last_error_status_received_stamp_type arg)
  {
    msg_.last_error_status_received_stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_error_status_time_available
{
public:
  explicit Init_O10ControlState_error_status_time_available(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_last_error_status_received_stamp error_status_time_available(::rokoko_omnihand_msgs::msg::O10ControlState::_error_status_time_available_type arg)
  {
    msg_.error_status_time_available = std::move(arg);
    return Init_O10ControlState_last_error_status_received_stamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_last_feedback_received_stamp
{
public:
  explicit Init_O10ControlState_last_feedback_received_stamp(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_error_status_time_available last_feedback_received_stamp(::rokoko_omnihand_msgs::msg::O10ControlState::_last_feedback_received_stamp_type arg)
  {
    msg_.last_feedback_received_stamp = std::move(arg);
    return Init_O10ControlState_error_status_time_available(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_feedback_time_available
{
public:
  explicit Init_O10ControlState_feedback_time_available(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_last_feedback_received_stamp feedback_time_available(::rokoko_omnihand_msgs::msg::O10ControlState::_feedback_time_available_type arg)
  {
    msg_.feedback_time_available = std::move(arg);
    return Init_O10ControlState_last_feedback_received_stamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_last_command_sent_stamp
{
public:
  explicit Init_O10ControlState_last_command_sent_stamp(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_feedback_time_available last_command_sent_stamp(::rokoko_omnihand_msgs::msg::O10ControlState::_last_command_sent_stamp_type arg)
  {
    msg_.last_command_sent_stamp = std::move(arg);
    return Init_O10ControlState_feedback_time_available(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_command_time_available
{
public:
  explicit Init_O10ControlState_command_time_available(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_last_command_sent_stamp command_time_available(::rokoko_omnihand_msgs::msg::O10ControlState::_command_time_available_type arg)
  {
    msg_.command_time_available = std::move(arg);
    return Init_O10ControlState_last_command_sent_stamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_last_target_received_stamp
{
public:
  explicit Init_O10ControlState_last_target_received_stamp(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_command_time_available last_target_received_stamp(::rokoko_omnihand_msgs::msg::O10ControlState::_last_target_received_stamp_type arg)
  {
    msg_.last_target_received_stamp = std::move(arg);
    return Init_O10ControlState_command_time_available(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_last_target_input_stamp
{
public:
  explicit Init_O10ControlState_last_target_input_stamp(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_last_target_received_stamp last_target_input_stamp(::rokoko_omnihand_msgs::msg::O10ControlState::_last_target_input_stamp_type arg)
  {
    msg_.last_target_input_stamp = std::move(arg);
    return Init_O10ControlState_last_target_received_stamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_target_time_available
{
public:
  explicit Init_O10ControlState_target_time_available(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_last_target_input_stamp target_time_available(::rokoko_omnihand_msgs::msg::O10ControlState::_target_time_available_type arg)
  {
    msg_.target_time_available = std::move(arg);
    return Init_O10ControlState_last_target_input_stamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_hardware_error_bits
{
public:
  explicit Init_O10ControlState_hardware_error_bits(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_target_time_available hardware_error_bits(::rokoko_omnihand_msgs::msg::O10ControlState::_hardware_error_bits_type arg)
  {
    msg_.hardware_error_bits = std::move(arg);
    return Init_O10ControlState_target_time_available(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_fault_reason_mask
{
public:
  explicit Init_O10ControlState_fault_reason_mask(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_hardware_error_bits fault_reason_mask(::rokoko_omnihand_msgs::msg::O10ControlState::_fault_reason_mask_type arg)
  {
    msg_.fault_reason_mask = std::move(arg);
    return Init_O10ControlState_hardware_error_bits(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_slew_limited
{
public:
  explicit Init_O10ControlState_slew_limited(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_fault_reason_mask slew_limited(::rokoko_omnihand_msgs::msg::O10ControlState::_slew_limited_type arg)
  {
    msg_.slew_limited = std::move(arg);
    return Init_O10ControlState_fault_reason_mask(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_command_published
{
public:
  explicit Init_O10ControlState_command_published(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_slew_limited command_published(::rokoko_omnihand_msgs::msg::O10ControlState::_command_published_type arg)
  {
    msg_.command_published = std::move(arg);
    return Init_O10ControlState_slew_limited(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_target_result
{
public:
  explicit Init_O10ControlState_target_result(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_command_published target_result(::rokoko_omnihand_msgs::msg::O10ControlState::_target_result_type arg)
  {
    msg_.target_result = std::move(arg);
    return Init_O10ControlState_command_published(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_motion_enabled
{
public:
  explicit Init_O10ControlState_motion_enabled(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_target_result motion_enabled(::rokoko_omnihand_msgs::msg::O10ControlState::_motion_enabled_type arg)
  {
    msg_.motion_enabled = std::move(arg);
    return Init_O10ControlState_target_result(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_fault_latched
{
public:
  explicit Init_O10ControlState_fault_latched(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_motion_enabled fault_latched(::rokoko_omnihand_msgs::msg::O10ControlState::_fault_latched_type arg)
  {
    msg_.fault_latched = std::move(arg);
    return Init_O10ControlState_motion_enabled(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_target_fresh
{
public:
  explicit Init_O10ControlState_target_fresh(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_fault_latched target_fresh(::rokoko_omnihand_msgs::msg::O10ControlState::_target_fresh_type arg)
  {
    msg_.target_fresh = std::move(arg);
    return Init_O10ControlState_fault_latched(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_target_ready
{
public:
  explicit Init_O10ControlState_target_ready(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_target_fresh target_ready(::rokoko_omnihand_msgs::msg::O10ControlState::_target_ready_type arg)
  {
    msg_.target_ready = std::move(arg);
    return Init_O10ControlState_target_fresh(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_error_monitor_ready
{
public:
  explicit Init_O10ControlState_error_monitor_ready(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_target_ready error_monitor_ready(::rokoko_omnihand_msgs::msg::O10ControlState::_error_monitor_ready_type arg)
  {
    msg_.error_monitor_ready = std::move(arg);
    return Init_O10ControlState_target_ready(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_feedback_ready
{
public:
  explicit Init_O10ControlState_feedback_ready(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_error_monitor_ready feedback_ready(::rokoko_omnihand_msgs::msg::O10ControlState::_feedback_ready_type arg)
  {
    msg_.feedback_ready = std::move(arg);
    return Init_O10ControlState_error_monitor_ready(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_phase
{
public:
  explicit Init_O10ControlState_phase(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_feedback_ready phase(::rokoko_omnihand_msgs::msg::O10ControlState::_phase_type arg)
  {
    msg_.phase = std::move(arg);
    return Init_O10ControlState_feedback_ready(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_event
{
public:
  explicit Init_O10ControlState_event(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_phase event(::rokoko_omnihand_msgs::msg::O10ControlState::_event_type arg)
  {
    msg_.event = std::move(arg);
    return Init_O10ControlState_phase(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_side
{
public:
  explicit Init_O10ControlState_side(::rokoko_omnihand_msgs::msg::O10ControlState & msg)
  : msg_(msg)
  {}
  Init_O10ControlState_event side(::rokoko_omnihand_msgs::msg::O10ControlState::_side_type arg)
  {
    msg_.side = std::move(arg);
    return Init_O10ControlState_event(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

class Init_O10ControlState_header
{
public:
  Init_O10ControlState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_O10ControlState_side header(::rokoko_omnihand_msgs::msg::O10ControlState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_O10ControlState_side(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::O10ControlState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::rokoko_omnihand_msgs::msg::O10ControlState>()
{
  return rokoko_omnihand_msgs::msg::builder::Init_O10ControlState_header();
}

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__BUILDER_HPP_
