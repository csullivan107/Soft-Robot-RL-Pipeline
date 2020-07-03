; Auto-generated. Do not edit!


(cl:in-package soft_robot_learning-msg)


;//! \htmlinclude gcode_packager.msg.html

(cl:defclass <gcode_packager> (roslisp-msg-protocol:ros-message)
  ((x_percentage
    :reader x_percentage
    :initarg :x_percentage
    :type cl:float
    :initform 0.0)
   (y_percentage
    :reader y_percentage
    :initarg :y_percentage
    :type cl:float
    :initform 0.0))
)

(cl:defclass gcode_packager (<gcode_packager>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <gcode_packager>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'gcode_packager)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name soft_robot_learning-msg:<gcode_packager> is deprecated: use soft_robot_learning-msg:gcode_packager instead.")))

(cl:ensure-generic-function 'x_percentage-val :lambda-list '(m))
(cl:defmethod x_percentage-val ((m <gcode_packager>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader soft_robot_learning-msg:x_percentage-val is deprecated.  Use soft_robot_learning-msg:x_percentage instead.")
  (x_percentage m))

(cl:ensure-generic-function 'y_percentage-val :lambda-list '(m))
(cl:defmethod y_percentage-val ((m <gcode_packager>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader soft_robot_learning-msg:y_percentage-val is deprecated.  Use soft_robot_learning-msg:y_percentage instead.")
  (y_percentage m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <gcode_packager>) ostream)
  "Serializes a message object of type '<gcode_packager>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x_percentage))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y_percentage))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <gcode_packager>) istream)
  "Deserializes a message object of type '<gcode_packager>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x_percentage) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y_percentage) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<gcode_packager>)))
  "Returns string type for a message object of type '<gcode_packager>"
  "soft_robot_learning/gcode_packager")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'gcode_packager)))
  "Returns string type for a message object of type 'gcode_packager"
  "soft_robot_learning/gcode_packager")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<gcode_packager>)))
  "Returns md5sum for a message object of type '<gcode_packager>"
  "04ac0e9112339add0ccbc4911b02d6de")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'gcode_packager)))
  "Returns md5sum for a message object of type 'gcode_packager"
  "04ac0e9112339add0ccbc4911b02d6de")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<gcode_packager>)))
  "Returns full string definition for message of type '<gcode_packager>"
  (cl:format cl:nil "float32 x_percentage~%float32 y_percentage~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'gcode_packager)))
  "Returns full string definition for message of type 'gcode_packager"
  (cl:format cl:nil "float32 x_percentage~%float32 y_percentage~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <gcode_packager>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <gcode_packager>))
  "Converts a ROS message object to a list"
  (cl:list 'gcode_packager
    (cl:cons ':x_percentage (x_percentage msg))
    (cl:cons ':y_percentage (y_percentage msg))
))
