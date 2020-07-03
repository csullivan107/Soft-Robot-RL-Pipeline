; Auto-generated. Do not edit!


(cl:in-package soft_robot_learning-msg)


;//! \htmlinclude apriltag_data.msg.html

(cl:defclass <apriltag_data> (roslisp-msg-protocol:ros-message)
  ((x_pos_gnd
    :reader x_pos_gnd
    :initarg :x_pos_gnd
    :type cl:float
    :initform 0.0)
   (y_pos_gnd
    :reader y_pos_gnd
    :initarg :y_pos_gnd
    :type cl:float
    :initform 0.0))
)

(cl:defclass apriltag_data (<apriltag_data>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <apriltag_data>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'apriltag_data)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name soft_robot_learning-msg:<apriltag_data> is deprecated: use soft_robot_learning-msg:apriltag_data instead.")))

(cl:ensure-generic-function 'x_pos_gnd-val :lambda-list '(m))
(cl:defmethod x_pos_gnd-val ((m <apriltag_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader soft_robot_learning-msg:x_pos_gnd-val is deprecated.  Use soft_robot_learning-msg:x_pos_gnd instead.")
  (x_pos_gnd m))

(cl:ensure-generic-function 'y_pos_gnd-val :lambda-list '(m))
(cl:defmethod y_pos_gnd-val ((m <apriltag_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader soft_robot_learning-msg:y_pos_gnd-val is deprecated.  Use soft_robot_learning-msg:y_pos_gnd instead.")
  (y_pos_gnd m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <apriltag_data>) ostream)
  "Serializes a message object of type '<apriltag_data>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x_pos_gnd))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y_pos_gnd))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <apriltag_data>) istream)
  "Deserializes a message object of type '<apriltag_data>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x_pos_gnd) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y_pos_gnd) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<apriltag_data>)))
  "Returns string type for a message object of type '<apriltag_data>"
  "soft_robot_learning/apriltag_data")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'apriltag_data)))
  "Returns string type for a message object of type 'apriltag_data"
  "soft_robot_learning/apriltag_data")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<apriltag_data>)))
  "Returns md5sum for a message object of type '<apriltag_data>"
  "7eb6b532fc62c3db52dc0849aeb59aea")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'apriltag_data)))
  "Returns md5sum for a message object of type 'apriltag_data"
  "7eb6b532fc62c3db52dc0849aeb59aea")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<apriltag_data>)))
  "Returns full string definition for message of type '<apriltag_data>"
  (cl:format cl:nil "float32 x_pos_gnd~%float32 y_pos_gnd~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'apriltag_data)))
  "Returns full string definition for message of type 'apriltag_data"
  (cl:format cl:nil "float32 x_pos_gnd~%float32 y_pos_gnd~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <apriltag_data>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <apriltag_data>))
  "Converts a ROS message object to a list"
  (cl:list 'apriltag_data
    (cl:cons ':x_pos_gnd (x_pos_gnd msg))
    (cl:cons ':y_pos_gnd (y_pos_gnd msg))
))
