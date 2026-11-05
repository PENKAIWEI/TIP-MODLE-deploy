// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rokoko_omnihand_msgs:srv/ControlOperation.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/srv/control_operation.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__BUILDER_HPP_
#define ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rokoko_omnihand_msgs/srv/detail/control_operation__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rokoko_omnihand_msgs
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::rokoko_omnihand_msgs::srv::ControlOperation_Request>()
{
  return ::rokoko_omnihand_msgs::srv::ControlOperation_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace rokoko_omnihand_msgs


namespace rokoko_omnihand_msgs
{

namespace srv
{

namespace builder
{

class Init_ControlOperation_Response_state
{
public:
  explicit Init_ControlOperation_Response_state(::rokoko_omnihand_msgs::srv::ControlOperation_Response & msg)
  : msg_(msg)
  {}
  ::rokoko_omnihand_msgs::srv::ControlOperation_Response state(::rokoko_omnihand_msgs::srv::ControlOperation_Response::_state_type arg)
  {
    msg_.state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rokoko_omnihand_msgs::srv::ControlOperation_Response msg_;
};

class Init_ControlOperation_Response_message
{
public:
  explicit Init_ControlOperation_Response_message(::rokoko_omnihand_msgs::srv::ControlOperation_Response & msg)
  : msg_(msg)
  {}
  Init_ControlOperation_Response_state message(::rokoko_omnihand_msgs::srv::ControlOperation_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_ControlOperation_Response_state(msg_);
  }

private:
  ::rokoko_omnihand_msgs::srv::ControlOperation_Response msg_;
};

class Init_ControlOperation_Response_result_code
{
public:
  explicit Init_ControlOperation_Response_result_code(::rokoko_omnihand_msgs::srv::ControlOperation_Response & msg)
  : msg_(msg)
  {}
  Init_ControlOperation_Response_message result_code(::rokoko_omnihand_msgs::srv::ControlOperation_Response::_result_code_type arg)
  {
    msg_.result_code = std::move(arg);
    return Init_ControlOperation_Response_message(msg_);
  }

private:
  ::rokoko_omnihand_msgs::srv::ControlOperation_Response msg_;
};

class Init_ControlOperation_Response_success
{
public:
  Init_ControlOperation_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlOperation_Response_result_code success(::rokoko_omnihand_msgs::srv::ControlOperation_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ControlOperation_Response_result_code(msg_);
  }

private:
  ::rokoko_omnihand_msgs::srv::ControlOperation_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::rokoko_omnihand_msgs::srv::ControlOperation_Response>()
{
  return rokoko_omnihand_msgs::srv::builder::Init_ControlOperation_Response_success();
}

}  // namespace rokoko_omnihand_msgs


namespace rokoko_omnihand_msgs
{

namespace srv
{

namespace builder
{

class Init_ControlOperation_Event_response
{
public:
  explicit Init_ControlOperation_Event_response(::rokoko_omnihand_msgs::srv::ControlOperation_Event & msg)
  : msg_(msg)
  {}
  ::rokoko_omnihand_msgs::srv::ControlOperation_Event response(::rokoko_omnihand_msgs::srv::ControlOperation_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rokoko_omnihand_msgs::srv::ControlOperation_Event msg_;
};

class Init_ControlOperation_Event_request
{
public:
  explicit Init_ControlOperation_Event_request(::rokoko_omnihand_msgs::srv::ControlOperation_Event & msg)
  : msg_(msg)
  {}
  Init_ControlOperation_Event_response request(::rokoko_omnihand_msgs::srv::ControlOperation_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_ControlOperation_Event_response(msg_);
  }

private:
  ::rokoko_omnihand_msgs::srv::ControlOperation_Event msg_;
};

class Init_ControlOperation_Event_info
{
public:
  Init_ControlOperation_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControlOperation_Event_request info(::rokoko_omnihand_msgs::srv::ControlOperation_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_ControlOperation_Event_request(msg_);
  }

private:
  ::rokoko_omnihand_msgs::srv::ControlOperation_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::rokoko_omnihand_msgs::srv::ControlOperation_Event>()
{
  return rokoko_omnihand_msgs::srv::builder::Init_ControlOperation_Event_info();
}

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__BUILDER_HPP_
