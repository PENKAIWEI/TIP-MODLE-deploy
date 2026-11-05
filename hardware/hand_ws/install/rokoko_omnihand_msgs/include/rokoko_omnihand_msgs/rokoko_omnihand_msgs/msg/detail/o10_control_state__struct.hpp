// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from rokoko_omnihand_msgs:msg/O10ControlState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/o10_control_state.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__STRUCT_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__STRUCT_HPP_

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
// Member 'last_target_input_stamp'
// Member 'last_target_received_stamp'
// Member 'last_command_sent_stamp'
// Member 'last_feedback_received_stamp'
// Member 'last_error_status_received_stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__rokoko_omnihand_msgs__msg__O10ControlState __attribute__((deprecated))
#else
# define DEPRECATED__rokoko_omnihand_msgs__msg__O10ControlState __declspec(deprecated)
#endif

namespace rokoko_omnihand_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct O10ControlState_
{
  using Type = O10ControlState_<ContainerAllocator>;

  explicit O10ControlState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    last_target_input_stamp(_init),
    last_target_received_stamp(_init),
    last_command_sent_stamp(_init),
    last_feedback_received_stamp(_init),
    last_error_status_received_stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->side = "";
      this->event = 0;
      this->phase = 0;
      this->feedback_ready = false;
      this->error_monitor_ready = false;
      this->target_ready = false;
      this->target_fresh = false;
      this->fault_latched = false;
      this->motion_enabled = false;
      this->target_result = 0;
      this->command_published = false;
      std::fill<typename std::array<bool, 10>::iterator, bool>(this->slew_limited.begin(), this->slew_limited.end(), false);
      this->fault_reason_mask = 0ul;
      std::fill<typename std::array<uint16_t, 10>::iterator, uint16_t>(this->hardware_error_bits.begin(), this->hardware_error_bits.end(), 0);
      this->target_time_available = false;
      this->command_time_available = false;
      this->feedback_time_available = false;
      this->error_status_time_available = false;
    }
  }

  explicit O10ControlState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    side(_alloc),
    slew_limited(_alloc),
    hardware_error_bits(_alloc),
    last_target_input_stamp(_alloc, _init),
    last_target_received_stamp(_alloc, _init),
    last_command_sent_stamp(_alloc, _init),
    last_feedback_received_stamp(_alloc, _init),
    last_error_status_received_stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->side = "";
      this->event = 0;
      this->phase = 0;
      this->feedback_ready = false;
      this->error_monitor_ready = false;
      this->target_ready = false;
      this->target_fresh = false;
      this->fault_latched = false;
      this->motion_enabled = false;
      this->target_result = 0;
      this->command_published = false;
      std::fill<typename std::array<bool, 10>::iterator, bool>(this->slew_limited.begin(), this->slew_limited.end(), false);
      this->fault_reason_mask = 0ul;
      std::fill<typename std::array<uint16_t, 10>::iterator, uint16_t>(this->hardware_error_bits.begin(), this->hardware_error_bits.end(), 0);
      this->target_time_available = false;
      this->command_time_available = false;
      this->feedback_time_available = false;
      this->error_status_time_available = false;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _side_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _side_type side;
  using _event_type =
    uint8_t;
  _event_type event;
  using _phase_type =
    uint8_t;
  _phase_type phase;
  using _feedback_ready_type =
    bool;
  _feedback_ready_type feedback_ready;
  using _error_monitor_ready_type =
    bool;
  _error_monitor_ready_type error_monitor_ready;
  using _target_ready_type =
    bool;
  _target_ready_type target_ready;
  using _target_fresh_type =
    bool;
  _target_fresh_type target_fresh;
  using _fault_latched_type =
    bool;
  _fault_latched_type fault_latched;
  using _motion_enabled_type =
    bool;
  _motion_enabled_type motion_enabled;
  using _target_result_type =
    uint8_t;
  _target_result_type target_result;
  using _command_published_type =
    bool;
  _command_published_type command_published;
  using _slew_limited_type =
    std::array<bool, 10>;
  _slew_limited_type slew_limited;
  using _fault_reason_mask_type =
    uint32_t;
  _fault_reason_mask_type fault_reason_mask;
  using _hardware_error_bits_type =
    std::array<uint16_t, 10>;
  _hardware_error_bits_type hardware_error_bits;
  using _target_time_available_type =
    bool;
  _target_time_available_type target_time_available;
  using _last_target_input_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _last_target_input_stamp_type last_target_input_stamp;
  using _last_target_received_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _last_target_received_stamp_type last_target_received_stamp;
  using _command_time_available_type =
    bool;
  _command_time_available_type command_time_available;
  using _last_command_sent_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _last_command_sent_stamp_type last_command_sent_stamp;
  using _feedback_time_available_type =
    bool;
  _feedback_time_available_type feedback_time_available;
  using _last_feedback_received_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _last_feedback_received_stamp_type last_feedback_received_stamp;
  using _error_status_time_available_type =
    bool;
  _error_status_time_available_type error_status_time_available;
  using _last_error_status_received_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _last_error_status_received_stamp_type last_error_status_received_stamp;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__side(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->side = _arg;
    return *this;
  }
  Type & set__event(
    const uint8_t & _arg)
  {
    this->event = _arg;
    return *this;
  }
  Type & set__phase(
    const uint8_t & _arg)
  {
    this->phase = _arg;
    return *this;
  }
  Type & set__feedback_ready(
    const bool & _arg)
  {
    this->feedback_ready = _arg;
    return *this;
  }
  Type & set__error_monitor_ready(
    const bool & _arg)
  {
    this->error_monitor_ready = _arg;
    return *this;
  }
  Type & set__target_ready(
    const bool & _arg)
  {
    this->target_ready = _arg;
    return *this;
  }
  Type & set__target_fresh(
    const bool & _arg)
  {
    this->target_fresh = _arg;
    return *this;
  }
  Type & set__fault_latched(
    const bool & _arg)
  {
    this->fault_latched = _arg;
    return *this;
  }
  Type & set__motion_enabled(
    const bool & _arg)
  {
    this->motion_enabled = _arg;
    return *this;
  }
  Type & set__target_result(
    const uint8_t & _arg)
  {
    this->target_result = _arg;
    return *this;
  }
  Type & set__command_published(
    const bool & _arg)
  {
    this->command_published = _arg;
    return *this;
  }
  Type & set__slew_limited(
    const std::array<bool, 10> & _arg)
  {
    this->slew_limited = _arg;
    return *this;
  }
  Type & set__fault_reason_mask(
    const uint32_t & _arg)
  {
    this->fault_reason_mask = _arg;
    return *this;
  }
  Type & set__hardware_error_bits(
    const std::array<uint16_t, 10> & _arg)
  {
    this->hardware_error_bits = _arg;
    return *this;
  }
  Type & set__target_time_available(
    const bool & _arg)
  {
    this->target_time_available = _arg;
    return *this;
  }
  Type & set__last_target_input_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->last_target_input_stamp = _arg;
    return *this;
  }
  Type & set__last_target_received_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->last_target_received_stamp = _arg;
    return *this;
  }
  Type & set__command_time_available(
    const bool & _arg)
  {
    this->command_time_available = _arg;
    return *this;
  }
  Type & set__last_command_sent_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->last_command_sent_stamp = _arg;
    return *this;
  }
  Type & set__feedback_time_available(
    const bool & _arg)
  {
    this->feedback_time_available = _arg;
    return *this;
  }
  Type & set__last_feedback_received_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->last_feedback_received_stamp = _arg;
    return *this;
  }
  Type & set__error_status_time_available(
    const bool & _arg)
  {
    this->error_status_time_available = _arg;
    return *this;
  }
  Type & set__last_error_status_received_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->last_error_status_received_stamp = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t EVENT_STARTUP =
    0u;
  static constexpr uint8_t EVENT_TARGET_PROCESSED =
    1u;
  static constexpr uint8_t EVENT_TARGET_TIMEOUT =
    2u;
  static constexpr uint8_t EVENT_FEEDBACK_RECEIVED =
    3u;
  static constexpr uint8_t EVENT_ERROR_STATUS_RECEIVED =
    4u;
  static constexpr uint8_t EVENT_OPERATOR_REQUEST =
    5u;
  static constexpr uint8_t EVENT_FAULT_CHANGED =
    6u;
  static constexpr uint8_t EVENT_COMPONENT_STATE_CHANGED =
    7u;
  static constexpr uint8_t PHASE_INITIALIZING =
    0u;
  static constexpr uint8_t PHASE_IDLE_NOT_READY =
    1u;
  static constexpr uint8_t PHASE_IDLE_READY =
    2u;
  static constexpr uint8_t PHASE_ACTIVE =
    3u;
  static constexpr uint8_t PHASE_PAUSED_TARGET_STALE =
    4u;
  static constexpr uint8_t PHASE_FAULT_LATCHED =
    5u;
  static constexpr uint8_t TARGET_NOT_EVALUATED =
    0u;
  static constexpr uint8_t TARGET_SENT =
    1u;
  static constexpr uint8_t TARGET_VALID_MOTION_DISABLED =
    2u;
  static constexpr uint8_t TARGET_REJECTED_SCHEMA =
    3u;
  static constexpr uint8_t TARGET_REJECTED_NAME_ORDER =
    4u;
  static constexpr uint8_t TARGET_REJECTED_NONFINITE =
    5u;
  static constexpr uint8_t TARGET_REJECTED_LIMIT =
    6u;
  static constexpr uint8_t TARGET_REJECTED_AUX_FIELDS =
    7u;
  static constexpr uint8_t TARGET_REJECTED_TIMESTAMP =
    8u;
  static constexpr uint8_t TARGET_REJECTED_CONTROL_STATE =
    9u;
  static constexpr uint32_t FAULT_HARDWARE_ERROR =
    1u;
  static constexpr uint32_t FAULT_COMMAND_READBACK_TIMEOUT =
    2u;
  static constexpr uint32_t FAULT_INVALID_FEEDBACK =
    4u;
  static constexpr uint32_t FAULT_SAFETY_INVARIANT =
    8u;
  static constexpr uint32_t FAULT_COMPONENT_RESTART_OR_DISCONNECT =
    16u;
  static constexpr uint32_t FAULT_ERROR_MONITOR_TIMEOUT =
    32u;

  // pointer types
  using RawPtr =
    rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator> *;
  using ConstRawPtr =
    const rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rokoko_omnihand_msgs__msg__O10ControlState
    std::shared_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rokoko_omnihand_msgs__msg__O10ControlState
    std::shared_ptr<rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const O10ControlState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->side != other.side) {
      return false;
    }
    if (this->event != other.event) {
      return false;
    }
    if (this->phase != other.phase) {
      return false;
    }
    if (this->feedback_ready != other.feedback_ready) {
      return false;
    }
    if (this->error_monitor_ready != other.error_monitor_ready) {
      return false;
    }
    if (this->target_ready != other.target_ready) {
      return false;
    }
    if (this->target_fresh != other.target_fresh) {
      return false;
    }
    if (this->fault_latched != other.fault_latched) {
      return false;
    }
    if (this->motion_enabled != other.motion_enabled) {
      return false;
    }
    if (this->target_result != other.target_result) {
      return false;
    }
    if (this->command_published != other.command_published) {
      return false;
    }
    if (this->slew_limited != other.slew_limited) {
      return false;
    }
    if (this->fault_reason_mask != other.fault_reason_mask) {
      return false;
    }
    if (this->hardware_error_bits != other.hardware_error_bits) {
      return false;
    }
    if (this->target_time_available != other.target_time_available) {
      return false;
    }
    if (this->last_target_input_stamp != other.last_target_input_stamp) {
      return false;
    }
    if (this->last_target_received_stamp != other.last_target_received_stamp) {
      return false;
    }
    if (this->command_time_available != other.command_time_available) {
      return false;
    }
    if (this->last_command_sent_stamp != other.last_command_sent_stamp) {
      return false;
    }
    if (this->feedback_time_available != other.feedback_time_available) {
      return false;
    }
    if (this->last_feedback_received_stamp != other.last_feedback_received_stamp) {
      return false;
    }
    if (this->error_status_time_available != other.error_status_time_available) {
      return false;
    }
    if (this->last_error_status_received_stamp != other.last_error_status_received_stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const O10ControlState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct O10ControlState_

// alias to use template instance with default allocator
using O10ControlState =
  rokoko_omnihand_msgs::msg::O10ControlState_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_STARTUP;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_TARGET_PROCESSED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_TARGET_TIMEOUT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_FEEDBACK_RECEIVED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_ERROR_STATUS_RECEIVED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_OPERATOR_REQUEST;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_FAULT_CHANGED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::EVENT_COMPONENT_STATE_CHANGED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::PHASE_INITIALIZING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::PHASE_IDLE_NOT_READY;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::PHASE_IDLE_READY;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::PHASE_ACTIVE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::PHASE_PAUSED_TARGET_STALE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::PHASE_FAULT_LATCHED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_NOT_EVALUATED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_SENT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_VALID_MOTION_DISABLED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_REJECTED_SCHEMA;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_REJECTED_NAME_ORDER;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_REJECTED_NONFINITE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_REJECTED_LIMIT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_REJECTED_AUX_FIELDS;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_REJECTED_TIMESTAMP;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t O10ControlState_<ContainerAllocator>::TARGET_REJECTED_CONTROL_STATE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint32_t O10ControlState_<ContainerAllocator>::FAULT_HARDWARE_ERROR;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint32_t O10ControlState_<ContainerAllocator>::FAULT_COMMAND_READBACK_TIMEOUT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint32_t O10ControlState_<ContainerAllocator>::FAULT_INVALID_FEEDBACK;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint32_t O10ControlState_<ContainerAllocator>::FAULT_SAFETY_INVARIANT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint32_t O10ControlState_<ContainerAllocator>::FAULT_COMPONENT_RESTART_OR_DISCONNECT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint32_t O10ControlState_<ContainerAllocator>::FAULT_ERROR_MONITOR_TIMEOUT;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__O10_CONTROL_STATE__STRUCT_HPP_
