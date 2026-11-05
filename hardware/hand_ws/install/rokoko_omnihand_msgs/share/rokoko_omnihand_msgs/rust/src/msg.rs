#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to rokoko_omnihand_msgs__msg__RawHandFrame
/// RawHandFrame — per-side Rokoko raw hand frame published by the Rokoko receiver
/// node on /rokoko/{left,right}/raw_hand. Read-only source data for retargeting.
///
/// Hand side is expressed by the Topic name, NOT by a field here (Spec decision 5).
/// The canonical 21 Rokoko node spellings are NOT owned by this package; they are
/// fixed by the versioned official JSON v3 fixture in rokoko_hand_receiver. This
/// message only carries the 21 names/positions/quaternions as data arrays, already
/// reordered into the project canonical order (Spec decision 6):
///   Hand, then Thumb/Index/Middle/Ring/Little, each Proximal/Medial/Distal/Tip.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RawHandFrame {
    /// stamp = local ROS time at which the UDP datagram was received on this host
    /// (Spec decisions 4, 50). frame_id is set by the publisher and is not used to
    /// encode the hand side.
    pub header: std_msgs::msg::Header,

    /// The single Rokoko Actor selected for this run (Spec decision 3). One run
    /// selects exactly one Actor (configurable index, default 0).
    pub actor_index: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub actor_name: std::string::String,

    /// Scene-level source timestamp carried VERBATIM from the Rokoko source (Spec
    /// decisions 4, 50). Its epoch/unit is UNCONFIRMED: it MUST NOT be converted to
    /// ROS time, subtracted from ROS time or used for control timing.
    pub source_timestamp: f64,

    /// Canonical-ordered 21 node data arrays (Spec decisions 5, 6, 49).
    /// Positions are Rokoko world coordinates, unmodified: no re-relativization,
    /// mirroring, filtering or normalization (Spec decision 7).
    /// Orientations are x, y, z, w quaternions, unmodified (Spec decision 7).
    pub node_names: [std::string::String; 21],


    // This member is not documented.
    #[allow(missing_docs)]
    pub positions: [geometry_msgs::msg::Point; 21],


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientations: [geometry_msgs::msg::Quaternion; 21],

}



impl Default for RawHandFrame {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RawHandFrame::default())
  }
}

impl rosidl_runtime_rs::Message for RawHandFrame {
  type RmwMsg = super::msg::rmw::RawHandFrame;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        actor_index: msg.actor_index,
        actor_name: msg.actor_name.as_str().into(),
        source_timestamp: msg.source_timestamp,
        node_names: msg.node_names
          .map(|elem| elem.as_str().into()),
        positions: msg.positions
          .map(|elem| geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned()),
        orientations: msg.orientations
          .map(|elem| geometry_msgs::msg::Quaternion::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned()),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      actor_index: msg.actor_index,
        actor_name: msg.actor_name.as_str().into(),
      source_timestamp: msg.source_timestamp,
        node_names: msg.node_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect::<Vec<_>>()
          .try_into()
          .unwrap(),
        positions: msg.positions
          .iter()
          .map(|elem| geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect::<Vec<_>>()
          .try_into()
          .unwrap(),
        orientations: msg.orientations
          .iter()
          .map(|elem| geometry_msgs::msg::Quaternion::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect::<Vec<_>>()
          .try_into()
          .unwrap(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      actor_index: msg.actor_index,
      actor_name: msg.actor_name.to_string(),
      source_timestamp: msg.source_timestamp,
      node_names: msg.node_names
        .map(|elem| elem.to_string()),
      positions: msg.positions
        .map(geometry_msgs::msg::Point::from_rmw_message),
      orientations: msg.orientations
        .map(geometry_msgs::msg::Quaternion::from_rmw_message),
    }
  }
}


// Corresponds to rokoko_omnihand_msgs__msg__RetargetingState
/// RetargetingState — per-side retargeting diagnostics.
/// Wire contract: DOCS/01_知识/05_手部重定向状态ROS接口契约.md.
/// This is a read-only diagnostic interface; it does not participate in O10
/// control decisions.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RetargetingState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub side: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub input_stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub solve_executed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub solve_finished_stamp: builtin_interfaces::msg::Time,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RetargetingState::default())
  }
}

impl rosidl_runtime_rs::Message for RetargetingState {
  type RmwMsg = super::msg::rmw::RetargetingState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        side: msg.side.as_str().into(),
        input_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.input_stamp)).into_owned(),
        solve_executed: msg.solve_executed,
        solve_finished_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.solve_finished_stamp)).into_owned(),
        solve_duration_sec: msg.solve_duration_sec,
        phase: msg.phase,
        ready: msg.ready,
        stale: msg.stale,
        command_published: msg.command_published,
        length_state: msg.length_state,
        ik_state: msg.ik_state,
        has_valid_ik: msg.has_valid_ik,
        used_previous_valid_target: msg.used_previous_valid_target,
        residual_available: msg.residual_available,
        normalized_residual: msg.normalized_residual,
        target_projection_applied: msg.target_projection_applied,
        target_projection_distance_available: msg.target_projection_distance_available,
        normalized_target_projection_distance: msg.normalized_target_projection_distance,
        solver_result_code: msg.solver_result_code,
        solver_evaluations: msg.solver_evaluations,
        recovery_valid_count: msg.recovery_valid_count,
        recovery_valid_duration_sec: msg.recovery_valid_duration_sec,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        side: msg.side.as_str().into(),
        input_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.input_stamp)).into_owned(),
      solve_executed: msg.solve_executed,
        solve_finished_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.solve_finished_stamp)).into_owned(),
      solve_duration_sec: msg.solve_duration_sec,
      phase: msg.phase,
      ready: msg.ready,
      stale: msg.stale,
      command_published: msg.command_published,
        length_state: msg.length_state,
        ik_state: msg.ik_state,
        has_valid_ik: msg.has_valid_ik,
        used_previous_valid_target: msg.used_previous_valid_target,
        residual_available: msg.residual_available,
        normalized_residual: msg.normalized_residual,
        target_projection_applied: msg.target_projection_applied,
        target_projection_distance_available: msg.target_projection_distance_available,
        normalized_target_projection_distance: msg.normalized_target_projection_distance,
        solver_result_code: msg.solver_result_code,
        solver_evaluations: msg.solver_evaluations,
      recovery_valid_count: msg.recovery_valid_count,
      recovery_valid_duration_sec: msg.recovery_valid_duration_sec,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      side: msg.side.to_string(),
      input_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.input_stamp),
      solve_executed: msg.solve_executed,
      solve_finished_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.solve_finished_stamp),
      solve_duration_sec: msg.solve_duration_sec,
      phase: msg.phase,
      ready: msg.ready,
      stale: msg.stale,
      command_published: msg.command_published,
      length_state: msg.length_state,
      ik_state: msg.ik_state,
      has_valid_ik: msg.has_valid_ik,
      used_previous_valid_target: msg.used_previous_valid_target,
      residual_available: msg.residual_available,
      normalized_residual: msg.normalized_residual,
      target_projection_applied: msg.target_projection_applied,
      target_projection_distance_available: msg.target_projection_distance_available,
      normalized_target_projection_distance: msg.normalized_target_projection_distance,
      solver_result_code: msg.solver_result_code,
      solver_evaluations: msg.solver_evaluations,
      recovery_valid_count: msg.recovery_valid_count,
      recovery_valid_duration_sec: msg.recovery_valid_duration_sec,
    }
  }
}


// Corresponds to rokoko_omnihand_msgs__msg__O10ControlState
/// O10ControlState — per-side control diagnostics.
/// Wire contract: DOCS/01_知识/06_O10控制状态ROS接口契约.md.
/// This is a read-only diagnostic interface; it does not participate in control
/// decisions.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct O10ControlState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub side: std::string::String,


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
    pub last_target_input_stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_target_received_stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub command_time_available: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_command_sent_stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback_time_available: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_feedback_received_stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_status_time_available: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_error_status_received_stamp: builtin_interfaces::msg::Time,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::O10ControlState::default())
  }
}

impl rosidl_runtime_rs::Message for O10ControlState {
  type RmwMsg = super::msg::rmw::O10ControlState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        side: msg.side.as_str().into(),
        event: msg.event,
        phase: msg.phase,
        feedback_ready: msg.feedback_ready,
        error_monitor_ready: msg.error_monitor_ready,
        target_ready: msg.target_ready,
        target_fresh: msg.target_fresh,
        fault_latched: msg.fault_latched,
        motion_enabled: msg.motion_enabled,
        target_result: msg.target_result,
        command_published: msg.command_published,
        slew_limited: msg.slew_limited,
        fault_reason_mask: msg.fault_reason_mask,
        hardware_error_bits: msg.hardware_error_bits,
        target_time_available: msg.target_time_available,
        last_target_input_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.last_target_input_stamp)).into_owned(),
        last_target_received_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.last_target_received_stamp)).into_owned(),
        command_time_available: msg.command_time_available,
        last_command_sent_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.last_command_sent_stamp)).into_owned(),
        feedback_time_available: msg.feedback_time_available,
        last_feedback_received_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.last_feedback_received_stamp)).into_owned(),
        error_status_time_available: msg.error_status_time_available,
        last_error_status_received_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.last_error_status_received_stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        side: msg.side.as_str().into(),
      event: msg.event,
      phase: msg.phase,
      feedback_ready: msg.feedback_ready,
      error_monitor_ready: msg.error_monitor_ready,
      target_ready: msg.target_ready,
      target_fresh: msg.target_fresh,
      fault_latched: msg.fault_latched,
      motion_enabled: msg.motion_enabled,
      target_result: msg.target_result,
      command_published: msg.command_published,
        slew_limited: msg.slew_limited,
      fault_reason_mask: msg.fault_reason_mask,
        hardware_error_bits: msg.hardware_error_bits,
      target_time_available: msg.target_time_available,
        last_target_input_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.last_target_input_stamp)).into_owned(),
        last_target_received_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.last_target_received_stamp)).into_owned(),
      command_time_available: msg.command_time_available,
        last_command_sent_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.last_command_sent_stamp)).into_owned(),
      feedback_time_available: msg.feedback_time_available,
        last_feedback_received_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.last_feedback_received_stamp)).into_owned(),
      error_status_time_available: msg.error_status_time_available,
        last_error_status_received_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.last_error_status_received_stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      side: msg.side.to_string(),
      event: msg.event,
      phase: msg.phase,
      feedback_ready: msg.feedback_ready,
      error_monitor_ready: msg.error_monitor_ready,
      target_ready: msg.target_ready,
      target_fresh: msg.target_fresh,
      fault_latched: msg.fault_latched,
      motion_enabled: msg.motion_enabled,
      target_result: msg.target_result,
      command_published: msg.command_published,
      slew_limited: msg.slew_limited,
      fault_reason_mask: msg.fault_reason_mask,
      hardware_error_bits: msg.hardware_error_bits,
      target_time_available: msg.target_time_available,
      last_target_input_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.last_target_input_stamp),
      last_target_received_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.last_target_received_stamp),
      command_time_available: msg.command_time_available,
      last_command_sent_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.last_command_sent_stamp),
      feedback_time_available: msg.feedback_time_available,
      last_feedback_received_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.last_feedback_received_stamp),
      error_status_time_available: msg.error_status_time_available,
      last_error_status_received_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.last_error_status_received_stamp),
    }
  }
}


