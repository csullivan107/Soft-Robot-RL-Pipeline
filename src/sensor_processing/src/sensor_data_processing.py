#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from rosserial_arduino.msg import Adc

#define publisher
#message format - "x: num y: num"
pub = rospy.Publisher('robot_state', String, queue_size = 30)

def callback0(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", str(data.adc0))
    x_sensor_reading = data.adc0
    y_sensor_reading = data.adc1

    str2pub = "x: " + str(x_sensor_reading) + " y: " + str(y_sensor_reading)
    pub.publish(str2pub)
    
    
def sensorProcessing():

    rospy.init_node('sensor_data_processing', anonymous=True)

    rospy.Subscriber("sensor_data", Adc, callback0)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    sensorProcessing()