#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__msg__RawHandFrame() -> *const std::ffi::c_void;
}

#[link(name = "rokoko_omnihand_msgs__rosidl_generator_c")]
extern "C" {
    fn rokoko_omnihand_msgs__msg__RawHandFrame__init(msg: *mut RawHandFrame) -> bool;
    fn rokoko_omnihand_msgs__msg__RawHandFrame__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RawHandFrame>, size: usize) -> bool;
    fn rokoko_omnihand_msgs__msg__RawHandFrame__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RawHandFrame>);
    fn rokoko_omnihand_msgs__msg__RawHandFrame__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RawHandFrame>, out_seq: *mut rosidl_runtime_rs::Sequence<RawHandFrame>) -> bool;
}

// Corresponds to rokoko_omnihand_msgs__msg__RawHandFrame
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// RawHandFrame — per-side Rokoko raw hand frame published by the Rokoko receiver
/// node on /rokoko/{left,right}/raw_hand. Read-only source data for retargeting.
///
/// Hand side is expressed by the Topic name, NOT by a field here (Spec decision 5).
/// The canonical 21 Rokoko node spellings are NOT owned by this package; they are
/// fixed by the versioned official JSON v3 fixture in rokoko_hand_receiver. This
/// message only carries the 21 names/positions/quaternions as data arrays, already
/// reordered into the project canonical order (Spec decision 6):
///   Hand, then Thumb/Index/Middle/Ring/Little, each Proximal/Medial/Distal/Tip.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RawHandFrame {
    /// stamp = local ROS time at which the UDP datagram was received on this host
    /// (Spec decisions 4, 50). frame_id is set by the publisher and is not used to
    /// encode the hand side.
    pub header: std_msgs::msg::rmw::Header,

    /// The single Rokoko Actor selected for this run (Spec decision 3). One run
    /// selects exactly one Actor (configurable index, default 0).
    pub actor_index: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub actor_name: rosidl_runtime_rs::String,

    /// Scene-level source timestamp carried VERBATIM from the Rokoko source (Spec
    /// decisions 4, 50). Its epoch/unit is UNCONFIRMED: it MUST NOT be converted to
    /// ROS time, subtracted from ROS time or used for control timing.
    pub source_timestamp: f64,

    /// Canonical-ordered 21 node data arrays (Spec decisions 5, 6, 49).
    /// Positions are Rokoko world coordinates, unmodified: no re-relativization,
    /// mirroring, filtering or normalization (Spec decision 7).
    /// Orientations are x, y, z, w quaternions, unmodified (Spec decision 7).
    pub node_names: [rosidl_runtime_rs::String; 21],


    // This member is not documented.
    #[allow(missing_docs)]
    pub positions: [geometry_msgs::msg::rmw::Point; 21],


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientations: [geometry_msgs::msg::rmw::Quaternion; 21],

}



impl Default for RawHandFrame {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rokoko_omnihand_msgs__msg__RawHandFrame__init(&mut msg as *mut _) {
        panic!("Call to rokoko_omnihand_msgs__msg__RawHandFrame__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RawHandFrame {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__RawHandFrame__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__RawHandFrame__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__RawHandFrame__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RawHandFrame {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RawHandFrame where Self: Sized {
  const TYPE_NAME: &'static str = "rokoko_omnihand_msgs/msg/RawHandFrame";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__msg__RawHandFrame() }
  }
}


#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__msg__RetargetingState() -> *const std::ffi::c_void;
}

#[link(name = "rokoko_omnihand_msgs__rosidl_generator_c")]
extern "C" {
    fn rokoko_omnihand_msgs__msg__RetargetingState__init(msg: *mut RetargetingState) -> bool;
    fn rokoko_omnihand_msgs__msg__RetargetingState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RetargetingState>, size: usize) -> bool;
    fn rokoko_omnihand_msgs__msg__RetargetingState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RetargetingState>);
    fn rokoko_omnihand_msgs__msg__RetargetingState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RetargetingState>, out_seq: *mut rosidl_runtime_rs::Sequence<RetargetingState>) -> bool;
}

// Corresponds to rokoko_omnihand_msgs__msg__RetargetingState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// RetargetingState — per-side retargeting diagnostics.
/// Wire contract: DOCS/01_知识/05_手部重定向状态ROS接口契约.md.
/// This is a read-only diagnostic interface; it does not participate in O10
/// control decisions.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RetargetingState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub side: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub input_stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub solve_executed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub solve_finished_stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub solve_duration_sec: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub phase: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub ready: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stale: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub command_published: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub length_state: [u8; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub ik_state: [u8; 5],

    /// Legacy field name: in mapping mode the thumb element reports mapping
    /// validity; use ik_state to distinguish mapping from an IK solve.
    pub has_valid_ik: [bool; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub used_previous_valid_target: [bool; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub residual_available: [bool; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub normalized_residual: [f64; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_projection_applied: [bool; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_projection_distance_available: [bool; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub normalized_target_projection_distance: [f64; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub solver_result_code: [i32; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub solver_evaluations: [u32; 5],


    // This member is not documented.
    #[allow(missing_docs)]
    pub recovery_valid_count: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub recovery_valid_duration_sec: f64,

}

impl RetargetingState {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_INITIALIZING: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_COLLECTING_LENGTHS: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_WAITING_FIRST_VALID_IK: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_TRACKING: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_STALE: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_RECOVERY_CONFIRMING: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_RECOVERY_RESUMING: u8 = 6;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_MODEL_ERROR: u8 = 7;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const LENGTH_COLLECTING: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const LENGTH_FROZEN: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const LENGTH_CURRENT_INVALID: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_UNINITIALIZED: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_VALID: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_INPUT_INVALID: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_SIDE_INVALID: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_RESIDUAL_EXCEEDED: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_SOLVER_ERROR: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_NOT_RUN_LENGTH_COLLECTING: u8 = 6;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_NOT_RUN_STALE: u8 = 7;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_MAPPING_VALID: u8 = 8;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IK_MAPPING_REJECTED: u8 = 9;

    /// Named wire value for a finger whose solver was not executed.
    pub const SOLVER_NOT_RUN: u8 = 0;

}


impl Default for RetargetingState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rokoko_omnihand_msgs__msg__RetargetingState__init(&mut msg as *mut _) {
        panic!("Call to rokoko_omnihand_msgs__msg__RetargetingState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RetargetingState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__RetargetingState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__RetargetingState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__RetargetingState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RetargetingState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RetargetingState where Self: Sized {
  const TYPE_NAME: &'static str = "rokoko_omnihand_msgs/msg/RetargetingState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__msg__RetargetingState() }
  }
}


#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__msg__O10ControlState() -> *const std::ffi::c_void;
}

#[link(name = "rokoko_omnihand_msgs__rosidl_generator_c")]
extern "C" {
    fn rokoko_omnihand_msgs__msg__O10ControlState__init(msg: *mut O10ControlState) -> bool;
    fn rokoko_omnihand_msgs__msg__O10ControlState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<O10ControlState>, size: usize) -> bool;
    fn rokoko_omnihand_msgs__msg__O10ControlState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<O10ControlState>);
    fn rokoko_omnihand_msgs__msg__O10ControlState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<O10ControlState>, out_seq: *mut rosidl_runtime_rs::Sequence<O10ControlState>) -> bool;
}

// Corresponds to rokoko_omnihand_msgs__msg__O10ControlState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// O10ControlState — per-side control diagnostics.
/// Wire contract: DOCS/01_知识/06_O10控制状态ROS接口契约.md.
/// This is a read-only diagnostic interface; it does not participate in control
/// decisions.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct O10ControlState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub side: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub event: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub phase: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback_ready: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_monitor_ready: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_ready: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_fresh: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fault_latched: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub motion_enabled: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_result: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub command_published: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub slew_limited: [bool; 10],


    // This member is not documented.
    #[allow(missing_docs)]
    pub fault_reason_mask: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hardware_error_bits: [u16; 10],


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_time_available: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_target_input_stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_target_received_stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub command_time_available: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_command_sent_stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback_time_available: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_feedback_received_stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_status_time_available: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_error_status_received_stamp: builtin_interfaces::msg::rmw::Time,

}

impl O10ControlState {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_STARTUP: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_TARGET_PROCESSED: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_TARGET_TIMEOUT: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_FEEDBACK_RECEIVED: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_ERROR_STATUS_RECEIVED: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_OPERATOR_REQUEST: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_FAULT_CHANGED: u8 = 6;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const EVENT_COMPONENT_STATE_CHANGED: u8 = 7;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_INITIALIZING: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_IDLE_NOT_READY: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_IDLE_READY: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_ACTIVE: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_PAUSED_TARGET_STALE: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PHASE_FAULT_LATCHED: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_NOT_EVALUATED: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_SENT: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_VALID_MOTION_DISABLED: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_REJECTED_SCHEMA: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_REJECTED_NAME_ORDER: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_REJECTED_NONFINITE: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_REJECTED_LIMIT: u8 = 6;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_REJECTED_AUX_FIELDS: u8 = 7;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_REJECTED_TIMESTAMP: u8 = 8;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const TARGET_REJECTED_CONTROL_STATE: u8 = 9;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAULT_HARDWARE_ERROR: u32 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAULT_COMMAND_READBACK_TIMEOUT: u32 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAULT_INVALID_FEEDBACK: u32 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAULT_SAFETY_INVARIANT: u32 = 8;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAULT_COMPONENT_RESTART_OR_DISCONNECT: u32 = 16;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAULT_ERROR_MONITOR_TIMEOUT: u32 = 32;

}


impl Default for O10ControlState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rokoko_omnihand_msgs__msg__O10ControlState__init(&mut msg as *mut _) {
        panic!("Call to rokoko_omnihand_msgs__msg__O10ControlState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for O10ControlState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__O10ControlState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__O10ControlState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__msg__O10ControlState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for O10ControlState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for O10ControlState where Self: Sized {
  const TYPE_NAME: &'static str = "rokoko_omnihand_msgs/msg/O10ControlState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__msg__O10ControlState() }
  }
}


