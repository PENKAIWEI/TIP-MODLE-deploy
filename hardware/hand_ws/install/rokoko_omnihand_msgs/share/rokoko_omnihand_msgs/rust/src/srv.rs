#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadO10ActiveJoints_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ReadO10ActiveJoints_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadO10ActiveJoints_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ReadO10ActiveJoints_Request {
  type RmwMsg = super::srv::rmw::ReadO10ActiveJoints_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadO10ActiveJoints_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sample_stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: [f64; 10],

}

impl ReadO10ActiveJoints_Response {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READ_SUCCESS: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READ_DEVICE_UNAVAILABLE: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READ_HARDWARE_ERROR: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READ_INVALID_RESULT: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READ_INTERNAL_ERROR: u8 = 4;

}


impl Default for ReadO10ActiveJoints_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadO10ActiveJoints_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ReadO10ActiveJoints_Response {
  type RmwMsg = super::srv::rmw::ReadO10ActiveJoints_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        sample_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.sample_stamp)).into_owned(),
        position: msg.position,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
        sample_stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.sample_stamp)).into_owned(),
        position: msg.position,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      result_code: msg.result_code,
      message: msg.message.to_string(),
      sample_stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.sample_stamp),
      position: msg.position,
    }
  }
}


// Corresponds to rokoko_omnihand_msgs__srv__ControlOperation_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ControlOperation_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ControlOperation_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ControlOperation_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ControlOperation_Request {
  type RmwMsg = super::srv::rmw::ControlOperation_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to rokoko_omnihand_msgs__srv__ControlOperation_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ControlOperation_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub state: super::msg::O10ControlState,

}

impl ControlOperation_Response {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_SUCCESS: u8 = 30;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_ALREADY_CLEAR: u8 = 31;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_CONTROL_STATE: u8 = 40;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_COMMUNICATION_UNHEALTHY: u8 = 41;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_ERROR_QUERY_TIMEOUT: u8 = 42;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_ERROR_STATUS_INVALID: u8 = 43;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_HARDWARE_ERROR_PRESENT: u8 = 44;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_FEEDBACK_READ_TIMEOUT: u8 = 45;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_FEEDBACK_INVALID: u8 = 46;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLEAR_FAULT_REJECTED_LIMITER_INIT_FAILED: u8 = 47;

}


impl Default for ControlOperation_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ControlOperation_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ControlOperation_Response {
  type RmwMsg = super::srv::rmw::ControlOperation_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        state: super::msg::O10ControlState::into_rmw_message(std::borrow::Cow::Owned(msg.state)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
        state: super::msg::O10ControlState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.state)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      result_code: msg.result_code,
      message: msg.message.to_string(),
      state: super::msg::O10ControlState::from_rmw_message(msg.state),
    }
  }
}






#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__rokoko_omnihand_msgs__srv__ReadO10ActiveJoints() -> *const std::ffi::c_void;
}

// Corresponds to rokoko_omnihand_msgs__srv__ReadO10ActiveJoints
#[allow(missing_docs, non_camel_case_types)]
pub struct ReadO10ActiveJoints;

impl rosidl_runtime_rs::Service for ReadO10ActiveJoints {
    type Request = ReadO10ActiveJoints_Request;
    type Response = ReadO10ActiveJoints_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__rokoko_omnihand_msgs__srv__ReadO10ActiveJoints() }
    }
}




#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__rokoko_omnihand_msgs__srv__ControlOperation() -> *const std::ffi::c_void;
}

// Corresponds to rokoko_omnihand_msgs__srv__ControlOperation
#[allow(missing_docs, non_camel_case_types)]
pub struct ControlOperation;

impl rosidl_runtime_rs::Service for ControlOperation {
    type Request = ControlOperation_Request;
    type Response = ControlOperation_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__rokoko_omnihand_msgs__srv__ControlOperation() }
    }
}


