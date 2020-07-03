;; Auto-generated. Do not edit!


(when (boundp 'soft_robot_learning::gcode_packager)
  (if (not (find-package "SOFT_ROBOT_LEARNING"))
    (make-package "SOFT_ROBOT_LEARNING"))
  (shadow 'gcode_packager (find-package "SOFT_ROBOT_LEARNING")))
(unless (find-package "SOFT_ROBOT_LEARNING::GCODE_PACKAGER")
  (make-package "SOFT_ROBOT_LEARNING::GCODE_PACKAGER"))

(in-package "ROS")
;;//! \htmlinclude gcode_packager.msg.html


(defclass soft_robot_learning::gcode_packager
  :super ros::object
  :slots (_x_percentage _y_percentage ))

(defmethod soft_robot_learning::gcode_packager
  (:init
   (&key
    ((:x_percentage __x_percentage) 0.0)
    ((:y_percentage __y_percentage) 0.0)
    )
   (send-super :init)
   (setq _x_percentage (float __x_percentage))
   (setq _y_percentage (float __y_percentage))
   self)
  (:x_percentage
   (&optional __x_percentage)
   (if __x_percentage (setq _x_percentage __x_percentage)) _x_percentage)
  (:y_percentage
   (&optional __y_percentage)
   (if __y_percentage (setq _y_percentage __y_percentage)) _y_percentage)
  (:serialization-length
   ()
   (+
    ;; float32 _x_percentage
    4
    ;; float32 _y_percentage
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _x_percentage
       (sys::poke _x_percentage (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y_percentage
       (sys::poke _y_percentage (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _x_percentage
     (setq _x_percentage (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y_percentage
     (setq _y_percentage (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get soft_robot_learning::gcode_packager :md5sum-) "04ac0e9112339add0ccbc4911b02d6de")
(setf (get soft_robot_learning::gcode_packager :datatype-) "soft_robot_learning/gcode_packager")
(setf (get soft_robot_learning::gcode_packager :definition-)
      "float32 x_percentage
float32 y_percentage
")



(provide :soft_robot_learning/gcode_packager "04ac0e9112339add0ccbc4911b02d6de")


