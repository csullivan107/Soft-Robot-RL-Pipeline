#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from rosserial_arduino.msg import Adc
from sensor_processing.msg import sensor_processing

#these vvalues are ready for setting parameters in ROS
#ADC values taht are the limits of actuation
X_HIGH_RAW = 800
X_LOW_RAW = 400
Y_HIGH_RAW = 800
Y_LOW_RAW = 400

#define publisher
#message format - "x: num y: num"
pub = rospy.Publisher('robot_state', sensor_processing, queue_size = 30)

#this function maps the raw data from 0-1024  values to 0 - 100% actuation
#input is raw reading, what reading corresopnds to 0, and 100% actuation respectively
#adapted from arduino map function
def raw2rl_mapping(raw,zero_value,hundred_value):
    raw_mapped = (raw-0)*(hundred_value - zero_value)/(1024 - 0) + zero_value
    #now that that the value is mapped between the sensor values change that to a percent
    zero_hund_range = hundred_value-zero_value
    raw_adjusted = raw_mapped - zero_value
    percentage = (float(raw_adjusted) / zero_hund_range) * 100
    print ("input: {}\tmapped+adj: {}\tpercentage: {}",format(raw),format(raw_adjusted) ,format(percentage))
    
    return percentage


def callback0(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", str(data.adc0))
    global X_LOW_RAW, X_HIGH_RAW, Y_HIGH_RAW, Y_LOW_RAW
    #Read in sensor data from Arduino
    x_sensor_reading = data.adc0
    y_sensor_reading = data.adc1
    #map readings from 0-1024 to percentages (see: calibration)
    x_mapped = raw2rl_mapping(x_sensor_reading,X_LOW_RAW,X_HIGH_RAW)
    y_mapped = raw2rl_mapping(y_sensor_reading,Y_LOW_RAW,Y_HIGH_RAW)
    #package message and publish
    message = sensor_processing()
    message.xSensor = x_mapped
    message.ySensor = y_mapped
    pub.publish(message)
    
    
def sensorProcessingNode():

    rospy.init_node('sensor_data_processing', anonymous=True)

    rospy.Subscriber("sensor_data", Adc, callback0)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    sensorProcessingNode()