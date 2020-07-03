
(cl:in-package :asdf)

(defsystem "soft_robot_learning-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "apriltag_data" :depends-on ("_package_apriltag_data"))
    (:file "_package_apriltag_data" :depends-on ("_package"))
    (:file "gcode_packager" :depends-on ("_package_gcode_packager"))
    (:file "_package_gcode_packager" :depends-on ("_package"))
    (:file "sensor_processing" :depends-on ("_package_sensor_processing"))
    (:file "_package_sensor_processing" :depends-on ("_package"))
  ))