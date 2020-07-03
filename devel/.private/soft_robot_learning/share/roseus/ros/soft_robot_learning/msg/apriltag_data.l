;; Auto-generated. Do not edit!


(when (boundp 'soft_robot_learning::apriltag_data)
  (if (not (find-package "SOFT_ROBOT_LEARNING"))
    (make-package "SOFT_ROBOT_LEARNING"))
  (shadow 'apriltag_data (find-package "SOFT_ROBOT_LEARNING")))
(unless (find-package "SOFT_ROBOT_LEARNING::APRILTAG_DATA")
  (make-package "SOFT_ROBOT_LEARNING::APRILTAG_DATA"))

(in-package "ROS")
;;//! \htmlinclude apriltag_data.msg.html


(defclass soft_robot_learning::apriltag_data
  :super ros::object
  :slots (_x_pos_gnd _y_pos_gnd ))

(defmethod soft_robot_learning::apriltag_data
  (:init
   (&key
    ((:x_pos_gnd __x_pos_gnd) 0.0)
    ((:y_pos_gnd __y_pos_gnd) 0.0)
    )
   (send-super :init)
   (setq _x_pos_gnd (float __x_pos_gnd))
   (setq _y_pos_gnd (float __y_pos_gnd))
   self)
  (:x_pos_gnd
   (&optional __x_pos_gnd)
   (if __x_pos_gnd (setq _x_pos_gnd __x_pos_gnd)) _x_pos_gnd)
  (:y_pos_gnd
   (&optional __y_pos_gnd)
   (if __y_pos_gnd (setq _y_pos_gnd __y_pos_gnd)) _y_pos_gnd)
  (:serialization-length
   ()
   (+
    ;; float32 _x_pos_gnd
    4
    ;; float32 _y_pos_gnd
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _x_pos_gnd
       (sys::poke _x_pos_gnd (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y_pos_gnd
       (sys::poke _y_pos_gnd (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _x_pos_gnd
     (setq _x_pos_gnd (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y_pos_gnd
     (setq _y_pos_gnd (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get soft_robot_learning::apriltag_data :md5sum-) "7eb6b532fc62c3db52dc0849aeb59aea")
(setf (get soft_robot_learning::apriltag_data :datatype-) "soft_robot_learning/apriltag_data")
(setf (get soft_robot_learning::apriltag_data :definition-)
      "float32 x_pos_gnd
float32 y_pos_gnd
")



(provide :soft_robot_learning/apriltag_data "7eb6b532fc62c3db52dc0849aeb59aea")


