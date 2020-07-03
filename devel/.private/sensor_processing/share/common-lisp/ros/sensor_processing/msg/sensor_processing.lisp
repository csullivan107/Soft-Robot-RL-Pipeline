; Auto-generated. Do not edit!


(cl:in-package sensor_processing-msg)


;//! \htmlinclude sensor_processing.msg.html

(cl:defclass <sensor_processing> (roslisp-msg-protocol:ros-message)
  ((xSensor
    :reader xSensor
    :initarg :xSensor
    :type cl:float
    :initform 0.0)
   (ySensor
    :reader ySensor
    :initarg :ySensor
    :type cl:float
    :initform 0.0))
)

(cl:defclass sensor_processing (<sensor_processing>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <sensor_processing>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'sensor_processing)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensor_processing-msg:<sensor_processing> is deprecated: use sensor_processing-msg:sensor_processing instead.")))

(cl:ensure-generic-function 'xSensor-val :lambda-list '(m))
(cl:defmethod xSensor-val ((m <sensor_processing>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_processing-msg:xSensor-val is deprecated.  Use sensor_processing-msg:xSensor instead.")
  (xSensor m))

(cl:ensure-generic-function 'ySensor-val :lambda-list '(m))
(cl:defmethod ySensor-val ((m <sensor_processing>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor_processing-msg:ySensor-val is deprecated.  Use sensor_processing-msg:ySensor instead.")
  (ySensor m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <sensor_processing>) ostream)
  "Serializes a message object of type '<sensor_processing>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'xSensor))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'ySensor))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <sensor_processing>) istream)
  "Deserializes a message object of type '<sensor_processing>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'xSensor) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'ySensor) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<sensor_processing>)))
  "Returns string type for a message object of type '<sensor_processing>"
  "sensor_processing/sensor_processing")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'sensor_processing)))
  "Returns string type for a message object of type 'sensor_processing"
  "sensor_processing/sensor_processing")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<sensor_processing>)))
  "Returns md5sum for a message object of type '<sensor_processing>"
  "85a7f1f6ce3d01e7b0a20f37a29b8607")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'sensor_processing)))
  "Returns md5sum for a message object of type 'sensor_processing"
  "85a7f1f6ce3d01e7b0a20f37a29b8607")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<sensor_processing>)))
  "Returns full string definition for message of type '<sensor_processing>"
  (cl:format cl:nil "#This is a custom message template for the state of the robot~%#Modify it with the amount of sensors you have to put into your RL ~%#algorithm~%~%float32 xSensor~%float32 ySensor~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'sensor_processing)))
  "Returns full string definition for message of type 'sensor_processing"
  (cl:format cl:nil "#This is a custom message template for the state of the robot~%#Modify it with the amount of sensors you have to put into your RL ~%#algorithm~%~%float32 xSensor~%float32 ySensor~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <sensor_processing>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <sensor_processing>))
  "Converts a ROS message object to a list"
  (cl:list 'sensor_processing
    (cl:cons ':xSensor (xSensor msg))
    (cl:cons ':ySensor (ySensor msg))
))
