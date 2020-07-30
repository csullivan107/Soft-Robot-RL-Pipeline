#!/usr/bin/env python
#you need this above to get ROS to execute the script - points to the python executable
#use python 3 here due to the RL libraries being written in python 3
import numpy as np
import time
import pprint

#import ROS specific libraries and custom message types
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Empty
from soft_robot_learning.msg import sensor_processing
from soft_robot_learning.msg import gcode_packager
from soft_robot_learning.msg import apriltag_data
from rosserial_arduino.msg import Adc
from sensor_processing.msg import sensor_processing

pp = pprint.PrettyPrinter(indent=4)

#sensor readings
xState_global = 0.
yState_global = 0.
#apriltag readings
xPos_global = 0.
yPos_global = 0.

action_done = False

# define ROS publisher nodes
cmd_pub = rospy.Publisher('/actuator_commands', gcode_packager, queue_size = 30)
direct_cmd_publisher = rospy.Publisher('/grbl_commands', String, queue_size = 30)
grbl_reset_pub = rospy.Publisher('/system_cmd', Empty, queue_size=1)
#test pub to update the subscribed node. for testing
testpub = rospy.Publisher('/testData', String, queue_size = 20)

#define ROS subscriber callback methods
def sensor_data_callback(data):
	#print("Updating State")
	global xState_global
	global yState_global
	xState_global = float(data.adc0)
	yState_global = float(data.adc1)
	# print("x sensor: {}", format(xState_global))
	# print("y sensor: {}", format(yState_global))	


def action_done_callback(data):
	global action_done
	action_done = data.data

#Define ROS subscriber nodes
def RL_subscribers():
    rospy.init_node('sensor_calibration', anonymous=True)
    rospy.Subscriber("/sensor_data", Adc, sensor_data_callback)
    rospy.Subscriber("/action_done", Bool, action_done_callback)

def wait_for_action():
	global action_done
	count = 0
	while not action_done:
		count = count + 1
		#print(action_done)
		
	print("\t--Action Complete--\t|")
	time.sleep(1)

def homeGrblController():
	print("Homing System....")
	direct_cmd_publisher.publish('$H')
	wait_for_action()
	time.sleep(.5)
	direct_cmd_publisher.publish('G92 X0 Y0')
	print("Homing Complete")

def initGrblController():
	print("Initializing Grbl System...")
	direct_cmd_publisher.publish('$X')
	homeGrblController()

def resetGrblController():
	print("Resetting grbl controller...")
	msg = Empty()
	grbl_reset_pub.publish(msg)
	time.sleep(4) #wait for reset to take plae
	initGrblController()
	print("grbl controller reset!")

def homeRobot():
	print("Sending Robot Home")
	direct_cmd_publisher.publish('G0 X0 Y0')
	wait_for_action()
	print("Robot Home")
	

if __name__ == '__main__':
	
	#run suscriber nodes
	RL_subscribers()
	print("Starting...")

	time.sleep(3) #give ros time to set up

	resetGrblController()

	#x axis calibration
	xCmd = 0.
	yCmd = 0.
	direction  = 1
	readings = {}
	repeat = True
	skip = False

	#this is required to not sent teh same command twice... this messes things up for some reason
	direct_cmd_publisher.publish('g0 x2 y0')
	wait_for_action()

	print('------------------ X AXIS CALIBRATION ------------------')
	for i in range(51):
		msg = 'g0 x' + str(xCmd) + ' y' + str(yCmd)
		print("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f | %s" %(xCmd, yCmd, msg))
		direct_cmd_publisher.publish(msg)
		wait_for_action()
		time.sleep(.5)
		#read sensors store in a dict {cmd: reading}
		readings[xCmd] = xState_global
		print("\tState Information\t| \t  xState: %6.3f \t  yState: %6.3f" %(xState_global, yState_global))
		#update xCmd
		xCmd = xCmd + 2*direction
		# if (xCmd == 100) and repeat:
		# 	direction = 0
		# 	repeat = not repeat
		# 	#this is required to not sent teh same command twice... this messes things up for some reason
		# 	direct_cmd_publisher.publish('g0 x98 y0')
		# 	wait_for_action()
		# elif (xCmd == 100.) and not repeat:
		# 	direction = -1
		print('\t------------------------------------------------------------------------------------------')

pp.pprint(readings)

	