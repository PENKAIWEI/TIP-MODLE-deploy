#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request() -> *const std::ffi::c_void;
}

#[link(name = "rokoko_omnihand_msgs__rosidl_generator_c")]
extern "C" {
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__init(msg: *mut ReadO10ActiveJoints_Request) -> bool;
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Request>, size: usize) -> bool;
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Request>);
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Request>) -> bool;
}

// Corresponds to rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadO10ActiveJoints_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ReadO10ActiveJoints_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__init(&mut msg as *mut _) {
        panic!("Call to rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadO10ActiveJoints_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadO10ActiveJoints_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadO10ActiveJoints_Request where Self: Sized {
  const TYPE_NAME: &'static str = "rokoko_omnihand_msgs/srv/ReadO10ActiveJoints_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Request() }
  }
}


#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response() -> *const std::ffi::c_void;
}

#[link(name = "rokoko_omnihand_msgs__rosidl_generator_c")]
extern "C" {
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__init(msg: *mut ReadO10ActiveJoints_Response) -> bool;
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Response>, size: usize) -> bool;
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Response>);
    fn rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadO10ActiveJoints_Response>) -> bool;
}

// Corresponds to rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sample_stamp: builtin_interfaces::msg::rmw::Time,


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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__init(&mut msg as *mut _) {
        panic!("Call to rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadO10ActiveJoints_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadO10ActiveJoints_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadO10ActiveJoints_Response where Self: Sized {
  const TYPE_NAME: &'static str = "rokoko_omnihand_msgs/srv/ReadO10ActiveJoints_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ReadO10ActiveJoints_Response() }
  }
}


#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ControlOperation_Request() -> *const std::ffi::c_void;
}

#[link(name = "rokoko_omnihand_msgs__rosidl_generator_c")]
extern "C" {
    fn rokoko_omnihand_msgs__srv__ControlOperation_Request__init(msg: *mut ControlOperation_Request) -> bool;
    fn rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ControlOperation_Request>, size: usize) -> bool;
    fn rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ControlOperation_Request>);
    fn rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ControlOperation_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ControlOperation_Request>) -> bool;
}

// Corresponds to rokoko_omnihand_msgs__srv__ControlOperation_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ControlOperation_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ControlOperation_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rokoko_omnihand_msgs__srv__ControlOperation_Request__init(&mut msg as *mut _) {
        panic!("Call to rokoko_omnihand_msgs__srv__ControlOperation_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ControlOperation_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ControlOperation_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ControlOperation_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ControlOperation_Request where Self: Sized {
  const TYPE_NAME: &'static str = "rokoko_omnihand_msgs/srv/ControlOperation_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ControlOperation_Request() }
  }
}


#[link(name = "rokoko_omnihand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ControlOperation_Response() -> *const std::ffi::c_void;
}

#[link(name = "rokoko_omnihand_msgs__rosidl_generator_c")]
extern "C" {
    fn rokoko_omnihand_msgs__srv__ControlOperation_Response__init(msg: *mut ControlOperation_Response) -> bool;
    fn rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ControlOperation_Response>, size: usize) -> bool;
    fn rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ControlOperation_Response>);
    fn rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ControlOperation_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ControlOperation_Response>) -> bool;
}

// Corresponds to rokoko_omnihand_msgs__srv__ControlOperation_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub state: super::super::msg::rmw::O10ControlState,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !rokoko_omnihand_msgs__srv__ControlOperation_Response__init(&mut msg as *mut _) {
        panic!("Call to rokoko_omnihand_msgs__srv__ControlOperation_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ControlOperation_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { rokoko_omnihand_msgs__srv__ControlOperation_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ControlOperation_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ControlOperation_Response where Self: Sized {
  const TYPE_NAME: &'static str = "rokoko_omnihand_msgs/srv/ControlOperation_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__rokoko_omnihand_msgs__srv__ControlOperation_Response() }
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


