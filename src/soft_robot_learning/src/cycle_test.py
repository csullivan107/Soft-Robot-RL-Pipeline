#!/usr/bin/env python
#this file must be run inside the catkin base worksapce for the directories to work properly

import numpy as np
import time
import pprint

import json
import os
import datetime



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

numReadings = 5
robotName = 'robot_3'

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
	
def calibrateAxis(axis2Calibrate, otherAxisValue):
	global numReadings
	readings = {}
	readings['xAxis'] = {} #predefine the value to key runKey as a dictionary
	readings['yAxis'] = {}

	print('------------------ ' + axis2Calibrate + ' AXIS CALIBRATION ------------------')
	for run in range(numReadings):
		#x axis calibration
		xCmd = 0.
		yCmd = 0.
		if axis2Calibrate == 'x':
			yCmd = otherAxisValue
		elif axis2Calibrate == 'y':
			xCmd = otherAxisValue
		elif axis2Calibrate == 'both':
			xCmd = 0.
			yCmd = 0.

	
		runKey = 'run '+ str(run)
		
		readings['xAxis'][runKey] = {}
		readings['yAxis'][runKey] = {}

		#this is required to not sent teh same command twice... this messes things up for some reason
		direct_cmd_publisher.publish('g0 x2 y2')
		wait_for_action()
		cmdIndex = 0
		print('------------------------------Starting Calibration run' + str(run) + '--------------------------')
		for i in range(51):
			msg = 'g0 x' + str(xCmd) + ' y' + str(yCmd)
			print("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f | %s" %(xCmd, yCmd, msg))
			direct_cmd_publisher.publish(msg)
			wait_for_action()
			time.sleep(.5)
	
			readings['xAxis'][runKey][cmdIndex] = xState_global
			readings['yAxis'][runKey][cmdIndex] = yState_global

			if axis2Calibrate == 'x':
				xCmd = xCmd + 2
			elif axis2Calibrate == 'y':
				yCmd = yCmd + 2
			elif axis2Calibrate == 'both':
				xCmd = xCmd + 2
				yCmd = yCmd + 2
			else:
				print('splease specify a corrent axis')
				return 0
			cmdIndex += 2
			print("\tState Information\t| \t  xState: %6.3f \t  yState: %6.3f" %(xState_global, yState_global))
			print('\t------------------------------------------------------------------------------------------')

		pp.pprint(readings)
		

	return readings



def averageReadings(readings):
	#this function means the readings from a single axis during a single run
	global numReadings
	average = {}
	stdDev = {}
	
	Cmd = 0
	for command in range(51):
		tempAvg = []
		for i in range(numReadings):
			runKey = 'run '+ str(i)
			tempAvg.append(readings[runKey][Cmd])
			print('TempAvg: ' + str(tempAvg))
		#the averate for a give command 
		average[Cmd] = np.mean(tempAvg)
		stdDev[Cmd] = np.std(tempAvg)
		Cmd += 2

		# pp.pprint(average)

	return average, stdDev

def cycleTest(n_cycles):
	for i in range(n_cycles):
		print("-----Cycle " + str(i+1) + " Start----")
		direct_cmd_publisher.publish('g0 x100 y100')
		wait_for_action()
		print("\tNetworks inflated")
		direct_cmd_publisher.publish('g0 x0 y0')
		wait_for_action()
		print("\tNetworks deflated")
		print("\tCycle Completed ("+str(i+1)+" out of "+str(n_cycles)+")")


if __name__ == '__main__':
	
	#run suscriber nodes
	RL_subscribers()
	print("Starting...")

	time.sleep(3) #give ros time to set up

	resetGrblController()

	cycleTest(1000)




	
	