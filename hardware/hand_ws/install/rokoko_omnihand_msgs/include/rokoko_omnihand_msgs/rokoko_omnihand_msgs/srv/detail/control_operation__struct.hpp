// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from rokoko_omnihand_msgs:srv/ControlOperation.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/srv/control_operation.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__STRUCT_HPP_
#define ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Request __attribute__((deprecated))
#else
# define DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Request __declspec(deprecated)
#endif

namespace rokoko_omnihand_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ControlOperation_Request_
{
  using Type = ControlOperation_Request_<ContainerAllocator>;

  explicit ControlOperation_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit ControlOperation_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Request
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Request
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControlOperation_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControlOperation_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControlOperation_Request_

// alias to use template instance with default allocator
using ControlOperation_Request =
  rokoko_omnihand_msgs::srv::ControlOperation_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace rokoko_omnihand_msgs


// Include directives for member types
// Member 'state'
#include "rokoko_omnihand_msgs/msg/detail/o10_control_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Response __attribute__((deprecated))
#else
# define DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Response __declspec(deprecated)
#endif

namespace rokoko_omnihand_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ControlOperation_Response_
{
  using Type = ControlOperation_Response_<ContainerAllocator>;

  explicit ControlOperation_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : state(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->result_code = 0;
      this->message = "";
    }
  }

  explicit ControlOperation_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc),
    state(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->result_code = 0;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _result_code_type =
    uint8_t;
  _result_code_type result_code;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _state_type =
    rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator>;
  _state_type state;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__result_code(
    const uint8_t & _arg)
  {
    this->result_code = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__state(
    const rokoko_omnihand_msgs::msg::O10ControlState_<ContainerAllocator> & _arg)
  {
    this->state = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t CLEAR_FAULT_SUCCESS =
    30u;
  static constexpr uint8_t CLEAR_FAULT_ALREADY_CLEAR =
    31u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_CONTROL_STATE =
    40u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_COMMUNICATION_UNHEALTHY =
    41u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_ERROR_QUERY_TIMEOUT =
    42u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_ERROR_STATUS_INVALID =
    43u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_HARDWARE_ERROR_PRESENT =
    44u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_FEEDBACK_READ_TIMEOUT =
    45u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_FEEDBACK_INVALID =
    46u;
  static constexpr uint8_t CLEAR_FAULT_REJECTED_LIMITER_INIT_FAILED =
    47u;

  // pointer types
  using RawPtr =
    rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Response
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Response
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControlOperation_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->result_code != other.result_code) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->state != other.state) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControlOperation_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControlOperation_Response_

// alias to use template instance with default allocator
using ControlOperation_Response =
  rokoko_omnihand_msgs::srv::ControlOperation_Response_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_SUCCESS;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_ALREADY_CLEAR;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_CONTROL_STATE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_COMMUNICATION_UNHEALTHY;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_ERROR_QUERY_TIMEOUT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_ERROR_STATUS_INVALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_HARDWARE_ERROR_PRESENT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_FEEDBACK_READ_TIMEOUT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_FEEDBACK_INVALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ControlOperation_Response_<ContainerAllocator>::CLEAR_FAULT_REJECTED_LIMITER_INIT_FAILED;
#endif  // __cplusplus < 201703L

}  // namespace srv

}  // namespace rokoko_omnihand_msgs


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Event __attribute__((deprecated))
#else
# define DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Event __declspec(deprecated)
#endif

namespace rokoko_omnihand_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ControlOperation_Event_
{
  using Type = ControlOperation_Event_<ContainerAllocator>;

  explicit ControlOperation_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit ControlOperation_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<rokoko_omnihand_msgs::srv::ControlOperation_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<rokoko_omnihand_msgs::srv::ControlOperation_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Event
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rokoko_omnihand_msgs__srv__ControlOperation_Event
    std::shared_ptr<rokoko_omnihand_msgs::srv::ControlOperation_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControlOperation_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControlOperation_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControlOperation_Event_

// alias to use template instance with default allocator
using ControlOperation_Event =
  rokoko_omnihand_msgs::srv::ControlOperation_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace rokoko_omnihand_msgs

namespace rokoko_omnihand_msgs
{

namespace srv
{

struct ControlOperation
{
  using Request = rokoko_omnihand_msgs::srv::ControlOperation_Request;
  using Response = rokoko_omnihand_msgs::srv::ControlOperation_Response;
  using Event = rokoko_omnihand_msgs::srv::ControlOperation_Event;
};

}  // namespace srv

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__SRV__DETAIL__CONTROL_OPERATION__STRUCT_HPP_
