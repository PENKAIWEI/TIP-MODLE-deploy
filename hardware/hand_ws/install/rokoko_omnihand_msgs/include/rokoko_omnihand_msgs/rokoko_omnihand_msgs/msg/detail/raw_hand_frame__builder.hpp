// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from rokoko_omnihand_msgs:msg/RawHandFrame.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/raw_hand_frame.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__BUILDER_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "rokoko_omnihand_msgs/msg/detail/raw_hand_frame__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace rokoko_omnihand_msgs
{

namespace msg
{

namespace builder
{

class Init_RawHandFrame_orientations
{
public:
  explicit Init_RawHandFrame_orientations(::rokoko_omnihand_msgs::msg::RawHandFrame & msg)
  : msg_(msg)
  {}
  ::rokoko_omnihand_msgs::msg::RawHandFrame orientations(::rokoko_omnihand_msgs::msg::RawHandFrame::_orientations_type arg)
  {
    msg_.orientations = std::move(arg);
    return std::move(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RawHandFrame msg_;
};

class Init_RawHandFrame_positions
{
public:
  explicit Init_RawHandFrame_positions(::rokoko_omnihand_msgs::msg::RawHandFrame & msg)
  : msg_(msg)
  {}
  Init_RawHandFrame_orientations positions(::rokoko_omnihand_msgs::msg::RawHandFrame::_positions_type arg)
  {
    msg_.positions = std::move(arg);
    return Init_RawHandFrame_orientations(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RawHandFrame msg_;
};

class Init_RawHandFrame_node_names
{
public:
  explicit Init_RawHandFrame_node_names(::rokoko_omnihand_msgs::msg::RawHandFrame & msg)
  : msg_(msg)
  {}
  Init_RawHandFrame_positions node_names(::rokoko_omnihand_msgs::msg::RawHandFrame::_node_names_type arg)
  {
    msg_.node_names = std::move(arg);
    return Init_RawHandFrame_positions(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RawHandFrame msg_;
};

class Init_RawHandFrame_source_timestamp
{
public:
  explicit Init_RawHandFrame_source_timestamp(::rokoko_omnihand_msgs::msg::RawHandFrame & msg)
  : msg_(msg)
  {}
  Init_RawHandFrame_node_names source_timestamp(::rokoko_omnihand_msgs::msg::RawHandFrame::_source_timestamp_type arg)
  {
    msg_.source_timestamp = std::move(arg);
    return Init_RawHandFrame_node_names(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RawHandFrame msg_;
};

class Init_RawHandFrame_actor_name
{
public:
  explicit Init_RawHandFrame_actor_name(::rokoko_omnihand_msgs::msg::RawHandFrame & msg)
  : msg_(msg)
  {}
  Init_RawHandFrame_source_timestamp actor_name(::rokoko_omnihand_msgs::msg::RawHandFrame::_actor_name_type arg)
  {
    msg_.actor_name = std::move(arg);
    return Init_RawHandFrame_source_timestamp(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RawHandFrame msg_;
};

class Init_RawHandFrame_actor_index
{
public:
  explicit Init_RawHandFrame_actor_index(::rokoko_omnihand_msgs::msg::RawHandFrame & msg)
  : msg_(msg)
  {}
  Init_RawHandFrame_actor_name actor_index(::rokoko_omnihand_msgs::msg::RawHandFrame::_actor_index_type arg)
  {
    msg_.actor_index = std::move(arg);
    return Init_RawHandFrame_actor_name(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RawHandFrame msg_;
};

class Init_RawHandFrame_header
{
public:
  Init_RawHandFrame_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RawHandFrame_actor_index header(::rokoko_omnihand_msgs::msg::RawHandFrame::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_RawHandFrame_actor_index(msg_);
  }

private:
  ::rokoko_omnihand_msgs::msg::RawHandFrame msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::rokoko_omnihand_msgs::msg::RawHandFrame>()
{
  return rokoko_omnihand_msgs::msg::builder::Init_RawHandFrame_header();
}

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__BUILDER_HPP_
