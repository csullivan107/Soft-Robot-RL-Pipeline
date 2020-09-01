#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from soft_robot_learning.msg import gcode_packager


#constants from calibration
X_RANGE_MAX = rospy.get_param('/xTravelMax')
X_RANGE_MIN = rospy.get_param('/xTravelMin')
Y_RANGE_MAX = rospy.get_param('/yTravelMax')
Y_RANGE_MIN = rospy.get_param('/yTravelMin')


#define publisher
#message format - "x: num y: num"
pub = rospy.Publisher('/grbl_commands', String, queue_size = 30)

#function to map percentage actuator commands to range of actuators
def actuator2gcode_mapping(percent_cmd,act_low,act_high):
    mapped = (percent_cmd-0)*(act_high - act_low)/(100 - 0) + act_low
    return mapped


def gcode(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", str(data.adc0))
    #Read in sensor data from Arduino
    x_perc = data.x_percentage
    y_perc = data.y_percentage
    x_act_dist = actuator2gcode_mapping(x_perc,X_RANGE_MIN,X_RANGE_MAX)
    y_act_dist = actuator2gcode_mapping(y_perc,Y_RANGE_MIN,Y_RANGE_MAX)
    x_act_dist = int(x_act_dist)
    y_act_dist = int(y_act_dist)
    

    #map readings from 0-1024 to percentages (see: calibration)
    #package message and publish it

    message = "G00 X" + str(x_act_dist) + " Y" + str(y_act_dist) + "\n"
    print(message)
    pub.publish(message)
    
    
def g_code_packager_node():

    rospy.init_node('gcode_packager', anonymous=True)

    rospy.Subscriber("/actuator_commands", gcode_packager, gcode)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    g_code_packager_node()