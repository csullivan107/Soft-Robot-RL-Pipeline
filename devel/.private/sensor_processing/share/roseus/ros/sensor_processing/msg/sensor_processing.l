;; Auto-generated. Do not edit!


(when (boundp 'sensor_processing::sensor_processing)
  (if (not (find-package "SENSOR_PROCESSING"))
    (make-package "SENSOR_PROCESSING"))
  (shadow 'sensor_processing (find-package "SENSOR_PROCESSING")))
(unless (find-package "SENSOR_PROCESSING::SENSOR_PROCESSING")
  (make-package "SENSOR_PROCESSING::SENSOR_PROCESSING"))

(in-package "ROS")
;;//! \htmlinclude sensor_processing.msg.html


(defclass sensor_processing::sensor_processing
  :super ros::object
  :slots (_xSensor _ySensor ))

(defmethod sensor_processing::sensor_processing
  (:init
   (&key
    ((:xSensor __xSensor) 0.0)
    ((:ySensor __ySensor) 0.0)
    )
   (send-super :init)
   (setq _xSensor (float __xSensor))
   (setq _ySensor (float __ySensor))
   self)
  (:xSensor
   (&optional __xSensor)
   (if __xSensor (setq _xSensor __xSensor)) _xSensor)
  (:ySensor
   (&optional __ySensor)
   (if __ySensor (setq _ySensor __ySensor)) _ySensor)
  (:serialization-length
   ()
   (+
    ;; float32 _xSensor
    4
    ;; float32 _ySensor
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _xSensor
       (sys::poke _xSensor (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _ySensor
       (sys::poke _ySensor (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _xSensor
     (setq _xSensor (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _ySensor
     (setq _ySensor (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get sensor_processing::sensor_processing :md5sum-) "85a7f1f6ce3d01e7b0a20f37a29b8607")
(setf (get sensor_processing::sensor_processing :datatype-) "sensor_processing/sensor_processing")
(setf (get sensor_processing::sensor_processing :definition-)
      "#This is a custom message template for the state of the robot
#Modify it with the amount of sensors you have to put into your RL 
#algorithm

float32 xSensor
float32 ySensor
")



(provide :sensor_processing/sensor_processing "85a7f1f6ce3d01e7b0a20f37a29b8607")


