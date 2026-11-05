// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from rokoko_omnihand_msgs:msg/RetargetingState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "rokoko_omnihand_msgs/msg/retargeting_state.hpp"


#ifndef ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__STRUCT_HPP_
#define ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__STRUCT_HPP_

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
// Member 'input_stamp'
// Member 'solve_finished_stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__rokoko_omnihand_msgs__msg__RetargetingState __attribute__((deprecated))
#else
# define DEPRECATED__rokoko_omnihand_msgs__msg__RetargetingState __declspec(deprecated)
#endif

namespace rokoko_omnihand_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RetargetingState_
{
  using Type = RetargetingState_<ContainerAllocator>;

  explicit RetargetingState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    input_stamp(_init),
    solve_finished_stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->side = "";
      this->solve_executed = false;
      this->solve_duration_sec = 0.0;
      this->phase = 0;
      this->ready = false;
      this->stale = false;
      this->command_published = false;
      std::fill<typename std::array<uint8_t, 5>::iterator, uint8_t>(this->length_state.begin(), this->length_state.end(), 0);
      std::fill<typename std::array<uint8_t, 5>::iterator, uint8_t>(this->ik_state.begin(), this->ik_state.end(), 0);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->has_valid_ik.begin(), this->has_valid_ik.end(), false);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->used_previous_valid_target.begin(), this->used_previous_valid_target.end(), false);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->residual_available.begin(), this->residual_available.end(), false);
      std::fill<typename std::array<double, 5>::iterator, double>(this->normalized_residual.begin(), this->normalized_residual.end(), 0.0);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->target_projection_applied.begin(), this->target_projection_applied.end(), false);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->target_projection_distance_available.begin(), this->target_projection_distance_available.end(), false);
      std::fill<typename std::array<double, 5>::iterator, double>(this->normalized_target_projection_distance.begin(), this->normalized_target_projection_distance.end(), 0.0);
      std::fill<typename std::array<int32_t, 5>::iterator, int32_t>(this->solver_result_code.begin(), this->solver_result_code.end(), 0l);
      std::fill<typename std::array<uint32_t, 5>::iterator, uint32_t>(this->solver_evaluations.begin(), this->solver_evaluations.end(), 0ul);
      this->recovery_valid_count = 0ul;
      this->recovery_valid_duration_sec = 0.0;
    }
  }

  explicit RetargetingState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    side(_alloc),
    input_stamp(_alloc, _init),
    solve_finished_stamp(_alloc, _init),
    length_state(_alloc),
    ik_state(_alloc),
    has_valid_ik(_alloc),
    used_previous_valid_target(_alloc),
    residual_available(_alloc),
    normalized_residual(_alloc),
    target_projection_applied(_alloc),
    target_projection_distance_available(_alloc),
    normalized_target_projection_distance(_alloc),
    solver_result_code(_alloc),
    solver_evaluations(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->side = "";
      this->solve_executed = false;
      this->solve_duration_sec = 0.0;
      this->phase = 0;
      this->ready = false;
      this->stale = false;
      this->command_published = false;
      std::fill<typename std::array<uint8_t, 5>::iterator, uint8_t>(this->length_state.begin(), this->length_state.end(), 0);
      std::fill<typename std::array<uint8_t, 5>::iterator, uint8_t>(this->ik_state.begin(), this->ik_state.end(), 0);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->has_valid_ik.begin(), this->has_valid_ik.end(), false);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->used_previous_valid_target.begin(), this->used_previous_valid_target.end(), false);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->residual_available.begin(), this->residual_available.end(), false);
      std::fill<typename std::array<double, 5>::iterator, double>(this->normalized_residual.begin(), this->normalized_residual.end(), 0.0);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->target_projection_applied.begin(), this->target_projection_applied.end(), false);
      std::fill<typename std::array<bool, 5>::iterator, bool>(this->target_projection_distance_available.begin(), this->target_projection_distance_available.end(), false);
      std::fill<typename std::array<double, 5>::iterator, double>(this->normalized_target_projection_distance.begin(), this->normalized_target_projection_distance.end(), 0.0);
      std::fill<typename std::array<int32_t, 5>::iterator, int32_t>(this->solver_result_code.begin(), this->solver_result_code.end(), 0l);
      std::fill<typename std::array<uint32_t, 5>::iterator, uint32_t>(this->solver_evaluations.begin(), this->solver_evaluations.end(), 0ul);
      this->recovery_valid_count = 0ul;
      this->recovery_valid_duration_sec = 0.0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _side_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _side_type side;
  using _input_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _input_stamp_type input_stamp;
  using _solve_executed_type =
    bool;
  _solve_executed_type solve_executed;
  using _solve_finished_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _solve_finished_stamp_type solve_finished_stamp;
  using _solve_duration_sec_type =
    double;
  _solve_duration_sec_type solve_duration_sec;
  using _phase_type =
    uint8_t;
  _phase_type phase;
  using _ready_type =
    bool;
  _ready_type ready;
  using _stale_type =
    bool;
  _stale_type stale;
  using _command_published_type =
    bool;
  _command_published_type command_published;
  using _length_state_type =
    std::array<uint8_t, 5>;
  _length_state_type length_state;
  using _ik_state_type =
    std::array<uint8_t, 5>;
  _ik_state_type ik_state;
  using _has_valid_ik_type =
    std::array<bool, 5>;
  _has_valid_ik_type has_valid_ik;
  using _used_previous_valid_target_type =
    std::array<bool, 5>;
  _used_previous_valid_target_type used_previous_valid_target;
  using _residual_available_type =
    std::array<bool, 5>;
  _residual_available_type residual_available;
  using _normalized_residual_type =
    std::array<double, 5>;
  _normalized_residual_type normalized_residual;
  using _target_projection_applied_type =
    std::array<bool, 5>;
  _target_projection_applied_type target_projection_applied;
  using _target_projection_distance_available_type =
    std::array<bool, 5>;
  _target_projection_distance_available_type target_projection_distance_available;
  using _normalized_target_projection_distance_type =
    std::array<double, 5>;
  _normalized_target_projection_distance_type normalized_target_projection_distance;
  using _solver_result_code_type =
    std::array<int32_t, 5>;
  _solver_result_code_type solver_result_code;
  using _solver_evaluations_type =
    std::array<uint32_t, 5>;
  _solver_evaluations_type solver_evaluations;
  using _recovery_valid_count_type =
    uint32_t;
  _recovery_valid_count_type recovery_valid_count;
  using _recovery_valid_duration_sec_type =
    double;
  _recovery_valid_duration_sec_type recovery_valid_duration_sec;

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
  Type & set__input_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->input_stamp = _arg;
    return *this;
  }
  Type & set__solve_executed(
    const bool & _arg)
  {
    this->solve_executed = _arg;
    return *this;
  }
  Type & set__solve_finished_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->solve_finished_stamp = _arg;
    return *this;
  }
  Type & set__solve_duration_sec(
    const double & _arg)
  {
    this->solve_duration_sec = _arg;
    return *this;
  }
  Type & set__phase(
    const uint8_t & _arg)
  {
    this->phase = _arg;
    return *this;
  }
  Type & set__ready(
    const bool & _arg)
  {
    this->ready = _arg;
    return *this;
  }
  Type & set__stale(
    const bool & _arg)
  {
    this->stale = _arg;
    return *this;
  }
  Type & set__command_published(
    const bool & _arg)
  {
    this->command_published = _arg;
    return *this;
  }
  Type & set__length_state(
    const std::array<uint8_t, 5> & _arg)
  {
    this->length_state = _arg;
    return *this;
  }
  Type & set__ik_state(
    const std::array<uint8_t, 5> & _arg)
  {
    this->ik_state = _arg;
    return *this;
  }
  Type & set__has_valid_ik(
    const std::array<bool, 5> & _arg)
  {
    this->has_valid_ik = _arg;
    return *this;
  }
  Type & set__used_previous_valid_target(
    const std::array<bool, 5> & _arg)
  {
    this->used_previous_valid_target = _arg;
    return *this;
  }
  Type & set__residual_available(
    const std::array<bool, 5> & _arg)
  {
    this->residual_available = _arg;
    return *this;
  }
  Type & set__normalized_residual(
    const std::array<double, 5> & _arg)
  {
    this->normalized_residual = _arg;
    return *this;
  }
  Type & set__target_projection_applied(
    const std::array<bool, 5> & _arg)
  {
    this->target_projection_applied = _arg;
    return *this;
  }
  Type & set__target_projection_distance_available(
    const std::array<bool, 5> & _arg)
  {
    this->target_projection_distance_available = _arg;
    return *this;
  }
  Type & set__normalized_target_projection_distance(
    const std::array<double, 5> & _arg)
  {
    this->normalized_target_projection_distance = _arg;
    return *this;
  }
  Type & set__solver_result_code(
    const std::array<int32_t, 5> & _arg)
  {
    this->solver_result_code = _arg;
    return *this;
  }
  Type & set__solver_evaluations(
    const std::array<uint32_t, 5> & _arg)
  {
    this->solver_evaluations = _arg;
    return *this;
  }
  Type & set__recovery_valid_count(
    const uint32_t & _arg)
  {
    this->recovery_valid_count = _arg;
    return *this;
  }
  Type & set__recovery_valid_duration_sec(
    const double & _arg)
  {
    this->recovery_valid_duration_sec = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t PHASE_INITIALIZING =
    0u;
  static constexpr uint8_t PHASE_COLLECTING_LENGTHS =
    1u;
  static constexpr uint8_t PHASE_WAITING_FIRST_VALID_IK =
    2u;
  static constexpr uint8_t PHASE_TRACKING =
    3u;
  static constexpr uint8_t PHASE_STALE =
    4u;
  static constexpr uint8_t PHASE_RECOVERY_CONFIRMING =
    5u;
  static constexpr uint8_t PHASE_RECOVERY_RESUMING =
    6u;
  static constexpr uint8_t PHASE_MODEL_ERROR =
    7u;
  static constexpr uint8_t LENGTH_COLLECTING =
    0u;
  static constexpr uint8_t LENGTH_FROZEN =
    1u;
  static constexpr uint8_t LENGTH_CURRENT_INVALID =
    2u;
  static constexpr uint8_t IK_UNINITIALIZED =
    0u;
  static constexpr uint8_t IK_VALID =
    1u;
  static constexpr uint8_t IK_INPUT_INVALID =
    2u;
  static constexpr uint8_t IK_SIDE_INVALID =
    3u;
  static constexpr uint8_t IK_RESIDUAL_EXCEEDED =
    4u;
  static constexpr uint8_t IK_SOLVER_ERROR =
    5u;
  static constexpr uint8_t IK_NOT_RUN_LENGTH_COLLECTING =
    6u;
  static constexpr uint8_t IK_NOT_RUN_STALE =
    7u;
  static constexpr uint8_t IK_MAPPING_VALID =
    8u;
  static constexpr uint8_t IK_MAPPING_REJECTED =
    9u;
  static constexpr uint8_t SOLVER_NOT_RUN =
    0u;

  // pointer types
  using RawPtr =
    rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator> *;
  using ConstRawPtr =
    const rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__rokoko_omnihand_msgs__msg__RetargetingState
    std::shared_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__rokoko_omnihand_msgs__msg__RetargetingState
    std::shared_ptr<rokoko_omnihand_msgs::msg::RetargetingState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RetargetingState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->side != other.side) {
      return false;
    }
    if (this->input_stamp != other.input_stamp) {
      return false;
    }
    if (this->solve_executed != other.solve_executed) {
      return false;
    }
    if (this->solve_finished_stamp != other.solve_finished_stamp) {
      return false;
    }
    if (this->solve_duration_sec != other.solve_duration_sec) {
      return false;
    }
    if (this->phase != other.phase) {
      return false;
    }
    if (this->ready != other.ready) {
      return false;
    }
    if (this->stale != other.stale) {
      return false;
    }
    if (this->command_published != other.command_published) {
      return false;
    }
    if (this->length_state != other.length_state) {
      return false;
    }
    if (this->ik_state != other.ik_state) {
      return false;
    }
    if (this->has_valid_ik != other.has_valid_ik) {
      return false;
    }
    if (this->used_previous_valid_target != other.used_previous_valid_target) {
      return false;
    }
    if (this->residual_available != other.residual_available) {
      return false;
    }
    if (this->normalized_residual != other.normalized_residual) {
      return false;
    }
    if (this->target_projection_applied != other.target_projection_applied) {
      return false;
    }
    if (this->target_projection_distance_available != other.target_projection_distance_available) {
      return false;
    }
    if (this->normalized_target_projection_distance != other.normalized_target_projection_distance) {
      return false;
    }
    if (this->solver_result_code != other.solver_result_code) {
      return false;
    }
    if (this->solver_evaluations != other.solver_evaluations) {
      return false;
    }
    if (this->recovery_valid_count != other.recovery_valid_count) {
      return false;
    }
    if (this->recovery_valid_duration_sec != other.recovery_valid_duration_sec) {
      return false;
    }
    return true;
  }
  bool operator!=(const RetargetingState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RetargetingState_

// alias to use template instance with default allocator
using RetargetingState =
  rokoko_omnihand_msgs::msg::RetargetingState_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_INITIALIZING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_COLLECTING_LENGTHS;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_WAITING_FIRST_VALID_IK;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_TRACKING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_STALE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_RECOVERY_CONFIRMING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_RECOVERY_RESUMING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::PHASE_MODEL_ERROR;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::LENGTH_COLLECTING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::LENGTH_FROZEN;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::LENGTH_CURRENT_INVALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_UNINITIALIZED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_VALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_INPUT_INVALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_SIDE_INVALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_RESIDUAL_EXCEEDED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_SOLVER_ERROR;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_NOT_RUN_LENGTH_COLLECTING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_NOT_RUN_STALE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_MAPPING_VALID;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::IK_MAPPING_REJECTED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RetargetingState_<ContainerAllocator>::SOLVER_NOT_RUN;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace rokoko_omnihand_msgs

#endif  // ROKOKO_OMNIHAND_MSGS__MSG__DETAIL__RETARGETING_STATE__STRUCT_HPP_
