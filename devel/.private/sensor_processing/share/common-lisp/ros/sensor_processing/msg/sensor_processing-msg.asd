
(cl:in-package :asdf)

(defsystem "sensor_processing-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "sensor_processing" :depends-on ("_package_sensor_processing"))
    (:file "_package_sensor_processing" :depends-on ("_package"))
  ))