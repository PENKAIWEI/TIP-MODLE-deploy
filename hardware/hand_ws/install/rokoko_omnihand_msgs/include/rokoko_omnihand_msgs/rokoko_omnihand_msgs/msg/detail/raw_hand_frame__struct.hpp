// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from rokoko_omnihand_msgs:msg/RawHandFrame.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/raw_hand_frame.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__STRUCT_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'positions'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'orientations'
#include "geometry_msgs/msg/detail/quaternion__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__rokoko_omnihand_msgs__msg__RawHandFrame __attribute__((deprecated))
#else
# define DEPRECATED__rokoko_omnihand_msgs__msg__RawHandFrame __declspec(deprecated)
#endif

namespace rokoko_omnihand_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RawHandFrame_
{
  using Type = RawHandFrame_<ContainerAllocator>;

  explicit RawHandFrame_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->actor_index = 0ul;
      this->actor_name = "";
      this->source_timestamp = 0.0;
      std::fill<typename std::array<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, 21>::iterator, std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>(this->node_names.begin(), this->node_names.end(), "");
      this->positions.fill(geometry_msgs::msg::Point_<ContainerAllocator>{_init});
      this->orientations.fill(geometry_msgs::msg::Quaternion_<ContainerAllocator>{_init});
    }
  }

  explicit RawHandFrame_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    actor_name(_alloc),
    node_names(_alloc),
    positions(_alloc),
    orientations(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->actor_index = 0ul;
      this->actor_name = "";
      this->source_timestamp = 0.0;
      std::fill<typename std::array<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, 21>::iterator, std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>(this->node_names.begin(), this->node_names.end(), "");
      this->positions.fill(geometry_msgs::msg::Point_<ContainerAllocator>{_alloc, _init});
      this->orientations.fill(geometry_msgs::msg::Quaternion_<ContainerAllocator>{_alloc, _init});
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _actor_index_type =
    uint32_t;
  _actor_index_type actor_index;
  using _actor_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _actor_name_type actor_name;
  using _source_timestamp_type =
    double;
  _source_timestamp_type source_timestamp;
  using _node_names_type =
    std::array<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, 21>;
  _node_names_type node_names;
  using _positions_type =
    std::array<geometry_msgs::msg::Point_<ContainerAllocator>, 21>;
  _positions_type positions;
  using _orientations_type =
    std::array<geometry_msgs::msg::Quaternion_<ContainerAllocator>, 21>;
  _orientations_type orientations;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__actor_index(
    const uint32_t & _arg)
  {
    this->actor_index = _arg;
    return *this;
  }
  Type & set__actor_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->actor_name = _arg;
    return *this;
  }
  Type & set__source_timestamp(
    const double & _arg)
  {
    this->source_timestamp = _arg;
    return *this;
  }
  Type & set__node_names(
    const std::array<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, 21> & _arg)
  {
    this->node_names = _arg;
    return *this;
  }
  Type & set__positions(
    const std::array<geometry_msgs::msg::Point_<ContainerAllocator>, 21> & _arg)
  {
    this->positions = _arg;
    return *this;
  }
  Type & set__orientations(
    const std::array<geometry_msgs::msg::Quaternion_<ContainerAllocator>, 21> & _arg)
  {
    this->orientations = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator> *;
  using ConstRawPtr =
    const rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rokoko_omnihand_msgs__msg__RawHandFrame
    std::shared_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rokoko_omnihand_msgs__msg__RawHandFrame
    std::shared_ptr<rokoko_omnihand_msgs::msg::RawHandFrame_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RawHandFrame_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->actor_index != other.actor_index) {
      return false;
    }
    if (this->actor_name != other.actor_name) {
      return false;
    }
    if (this->source_timestamp != other.source_timestamp) {
      return false;
    }
    if (this->node_names != other.node_names) {
      return false;
    }
    if (this->positions != other.positions) {
      return false;
    }
    if (this->orientations != other.orientations) {
      return false;
    }
    return true;
  }
  bool operator!=(const RawHandFrame_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RawHandFrame_

// alias to use template instance with default allocator
using RawHandFrame =
  rokoko_omnihand_msgs::msg::RawHandFrame_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RAW_HAND_FRAME__STRUCT_HPP_
