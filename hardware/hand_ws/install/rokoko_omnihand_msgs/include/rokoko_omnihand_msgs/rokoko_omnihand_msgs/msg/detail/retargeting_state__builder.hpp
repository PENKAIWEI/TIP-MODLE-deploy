// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rokoko_omnihand_msgs:msg/RetargetingState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/retargeting_state.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__BUILDER_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rokoko_omnihand_msgs/msg/detail/retargeting_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rokoko_omnihand_msgs
{

namespace msg
{

namespace builder
{

class Init_RetargetingState_recovery_valid_duration_sec
{
public:
  explicit Init_RetargetingState_recovery_valid_duration_sec(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  ::rokoko_omnihand_msgs::msg::RetargetingState recovery_valid_duration_sec(::rokoko_omnihand_msgs::msg::RetargetingState::_recovery_valid_duration_sec_type arg)
  {
    msg_.recovery_valid_duration_sec = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_recovery_valid_count
{
public:
  explicit Init_RetargetingState_recovery_valid_count(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_recovery_valid_duration_sec recovery_valid_count(::rokoko_omnihand_msgs::msg::RetargetingState::_recovery_valid_count_type arg)
  {
    msg_.recovery_valid_count = std::move(arg);
    return Init_RetargetingState_recovery_valid_duration_sec(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_solver_evaluations
{
public:
  explicit Init_RetargetingState_solver_evaluations(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_recovery_valid_count solver_evaluations(::rokoko_omnihand_msgs::msg::RetargetingState::_solver_evaluations_type arg)
  {
    msg_.solver_evaluations = std::move(arg);
    return Init_RetargetingState_recovery_valid_count(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_solver_result_code
{
public:
  explicit Init_RetargetingState_solver_result_code(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_solver_evaluations solver_result_code(::rokoko_omnihand_msgs::msg::RetargetingState::_solver_result_code_type arg)
  {
    msg_.solver_result_code = std::move(arg);
    return Init_RetargetingState_solver_evaluations(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_normalized_target_projection_distance
{
public:
  explicit Init_RetargetingState_normalized_target_projection_distance(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_solver_result_code normalized_target_projection_distance(::rokoko_omnihand_msgs::msg::RetargetingState::_normalized_target_projection_distance_type arg)
  {
    msg_.normalized_target_projection_distance = std::move(arg);
    return Init_RetargetingState_solver_result_code(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_target_projection_distance_available
{
public:
  explicit Init_RetargetingState_target_projection_distance_available(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_normalized_target_projection_distance target_projection_distance_available(::rokoko_omnihand_msgs::msg::RetargetingState::_target_projection_distance_available_type arg)
  {
    msg_.target_projection_distance_available = std::move(arg);
    return Init_RetargetingState_normalized_target_projection_distance(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_target_projection_applied
{
public:
  explicit Init_RetargetingState_target_projection_applied(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_target_projection_distance_available target_projection_applied(::rokoko_omnihand_msgs::msg::RetargetingState::_target_projection_applied_type arg)
  {
    msg_.target_projection_applied = std::move(arg);
    return Init_RetargetingState_target_projection_distance_available(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_normalized_residual
{
public:
  explicit Init_RetargetingState_normalized_residual(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_target_projection_applied normalized_residual(::rokoko_omnihand_msgs::msg::RetargetingState::_normalized_residual_type arg)
  {
    msg_.normalized_residual = std::move(arg);
    return Init_RetargetingState_target_projection_applied(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_residual_available
{
public:
  explicit Init_RetargetingState_residual_available(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_normalized_residual residual_available(::rokoko_omnihand_msgs::msg::RetargetingState::_residual_available_type arg)
  {
    msg_.residual_available = std::move(arg);
    return Init_RetargetingState_normalized_residual(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_used_previous_valid_target
{
public:
  explicit Init_RetargetingState_used_previous_valid_target(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_residual_available used_previous_valid_target(::rokoko_omnihand_msgs::msg::RetargetingState::_used_previous_valid_target_type arg)
  {
    msg_.used_previous_valid_target = std::move(arg);
    return Init_RetargetingState_residual_available(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_has_valid_ik
{
public:
  explicit Init_RetargetingState_has_valid_ik(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_used_previous_valid_target has_valid_ik(::rokoko_omnihand_msgs::msg::RetargetingState::_has_valid_ik_type arg)
  {
    msg_.has_valid_ik = std::move(arg);
    return Init_RetargetingState_used_previous_valid_target(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_ik_state
{
public:
  explicit Init_RetargetingState_ik_state(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_has_valid_ik ik_state(::rokoko_omnihand_msgs::msg::RetargetingState::_ik_state_type arg)
  {
    msg_.ik_state = std::move(arg);
    return Init_RetargetingState_has_valid_ik(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_length_state
{
public:
  explicit Init_RetargetingState_length_state(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_ik_state length_state(::rokoko_omnihand_msgs::msg::RetargetingState::_length_state_type arg)
  {
    msg_.length_state = std::move(arg);
    return Init_RetargetingState_ik_state(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_command_published
{
public:
  explicit Init_RetargetingState_command_published(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_length_state command_published(::rokoko_omnihand_msgs::msg::RetargetingState::_command_published_type arg)
  {
    msg_.command_published = std::move(arg);
    return Init_RetargetingState_length_state(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_stale
{
public:
  explicit Init_RetargetingState_stale(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_command_published stale(::rokoko_omnihand_msgs::msg::RetargetingState::_stale_type arg)
  {
    msg_.stale = std::move(arg);
    return Init_RetargetingState_command_published(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_ready
{
public:
  explicit Init_RetargetingState_ready(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_stale ready(::rokoko_omnihand_msgs::msg::RetargetingState::_ready_type arg)
  {
    msg_.ready = std::move(arg);
    return Init_RetargetingState_stale(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_phase
{
public:
  explicit Init_RetargetingState_phase(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_ready phase(::rokoko_omnihand_msgs::msg::RetargetingState::_phase_type arg)
  {
    msg_.phase = std::move(arg);
    return Init_RetargetingState_ready(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_solve_duration_sec
{
public:
  explicit Init_RetargetingState_solve_duration_sec(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_phase solve_duration_sec(::rokoko_omnihand_msgs::msg::RetargetingState::_solve_duration_sec_type arg)
  {
    msg_.solve_duration_sec = std::move(arg);
    return Init_RetargetingState_phase(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_solve_finished_stamp
{
public:
  explicit Init_RetargetingState_solve_finished_stamp(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_solve_duration_sec solve_finished_stamp(::rokoko_omnihand_msgs::msg::RetargetingState::_solve_finished_stamp_type arg)
  {
    msg_.solve_finished_stamp = std::move(arg);
    return Init_RetargetingState_solve_duration_sec(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_solve_executed
{
public:
  explicit Init_RetargetingState_solve_executed(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_solve_finished_stamp solve_executed(::rokoko_omnihand_msgs::msg::RetargetingState::_solve_executed_type arg)
  {
    msg_.solve_executed = std::move(arg);
    return Init_RetargetingState_solve_finished_stamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_input_stamp
{
public:
  explicit Init_RetargetingState_input_stamp(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_solve_executed input_stamp(::rokoko_omnihand_msgs::msg::RetargetingState::_input_stamp_type arg)
  {
    msg_.input_stamp = std::move(arg);
    return Init_RetargetingState_solve_executed(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_side
{
public:
  explicit Init_RetargetingState_side(::rokoko_omnihand_msgs::msg::RetargetingState & msg)
  : msg_(msg)
  {}
  Init_RetargetingState_input_stamp side(::rokoko_omnihand_msgs::msg::RetargetingState::_side_type arg)
  {
    msg_.side = std::move(arg);
    return Init_RetargetingState_input_stamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

class Init_RetargetingState_header
{
public:
  Init_RetargetingState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RetargetingState_side header(::rokoko_omnihand_msgs::msg::RetargetingState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_RetargetingState_side(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RetargetingState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::rokoko_omnihand_msgs::msg::RetargetingState>()
{
  return rokoko_omnihand_msgs::msg::builder::Init_RetargetingState_header();
}

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__BUILDER_HPP_
