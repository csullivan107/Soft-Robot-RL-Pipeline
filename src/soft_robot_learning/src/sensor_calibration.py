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
robotName = 'robot_1'

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




if __name__ == '__main__':
	
	#run suscriber nodes
	RL_subscribers()
	print("Starting...")

	time.sleep(3) #give ros time to set up

	resetGrblController()

	#calibrate the x axis sensor at various y values
	xCalibrateReadings_y0 = calibrateAxis('x',0)
	xCalibrateReadings_y50 = calibrateAxis('x',50)
	xCalibrateReadings_y100 = calibrateAxis('x',100)

	#collect and average the readings for both axes during the calibration cycle
	xCalibrate_x_avg_y0, xCalibrate_x_avg_y0_sdev  = averageReadings(xCalibrateReadings_y0['xAxis'])
	xCalibrate_x_avg_y50, xCalibrate_x_avg_y50_sdev = averageReadings(xCalibrateReadings_y50['xAxis'])
	xCalibrate_x_avg_y100, xCalibrate_x_avg_y100_sdev  = averageReadings(xCalibrateReadings_y100['xAxis'])
	xCalibrate_y_avg_y0, xCalibrate_y_avg_y0_sdev = averageReadings(xCalibrateReadings_y0['yAxis'])
	xCalibrate_y_avg_y50, xCalibrate_y_avg_y50_sdev = averageReadings(xCalibrateReadings_y50['yAxis'])
	xCalibrate_y_avg_y100, xCalibrate_y_avg_y100_sdev = averageReadings(xCalibrateReadings_y100['yAxis'])

	#calibrate y axis at various x axis values
	yCalibrateReadings_x0 = calibrateAxis('y',0)
	yCalibrateReadings_x50 = calibrateAxis('y',50)
	yCalibrateReadings_x100 = calibrateAxis('y',100)

	#collect acerages for bothe axes
	yCalibrate_x_avg_x0, yCalibrate_x_avg_x0_sdev = averageReadings(yCalibrateReadings_x0['xAxis'])
	yCalibrate_x_avg_x50, yCalibrate_x_avg_x50_sdev = averageReadings(yCalibrateReadings_x50['xAxis'])
	yCalibrate_x_avg_x100, yCalibrate_x_avg_x100_sdev = averageReadings(yCalibrateReadings_x100['xAxis'])
	yCalibrate_y_avg_x0, yCalibrate_y_avg_x0_sdev = averageReadings(yCalibrateReadings_x0['yAxis'])
	yCalibrate_y_avg_x50, yCalibrate_y_avg_x50_sdev = averageReadings(yCalibrateReadings_x50['yAxis'])
	yCalibrate_y_avg_x100, yCalibrate_y_avg_x100_sdev = averageReadings(yCalibrateReadings_x100['yAxis'])

	#run both axes at the same time and colelct readings
	bothCalibrateReadings = calibrateAxis('both',0)

	#average readings for running both axes at once
	bothCalibrate_x_avg, bothCalibrate_x_avg_sdev = averageReadings(bothCalibrateReadings['xAxis'])
	bothCalibrate_y_avg, bothCalibrate_y_avg_sdev = averageReadings(bothCalibrateReadings['yAxis'])
	
	#save to files... json
	run = 0
	baseDir = 'src/soft_robot_learning/src/sensor_calibration_files/' + robotName + '/Calibration_run_'


	t = datetime.datetime.now()
	t = t.strftime("%m_%d_%y_%X/")
	dirName = baseDir + t 
	if not os.path.exists(dirName):
		os.makedirs(dirName)
		print(dirName + " created successfully")
		done = True
	else:
		print(dirName + " exists")
		run += 1
		
	print("Saving Data")


	#store values from x calibration runs
	xCal_x_avg_json_y0 = json.dumps(xCalibrate_x_avg_y0)
	f = open(os.path.join(dirName, "xCal_x_avg_y0.json"), "w")
	f.write(xCal_x_avg_json_y0)
	f.close()

	xCal_x_avg_json_y0_sdev = json.dumps(xCalibrate_x_avg_y0_sdev)
	f = open(os.path.join(dirName, "xCal_x_avg_y0_sdev.json"), "w")
	f.write(xCal_x_avg_json_y0_sdev)
	f.close()

	xCal_x_avg_json_y50 = json.dumps(xCalibrate_x_avg_y50)
	f = open(os.path.join(dirName, "xCal_x_avg_y50.json"), "w")
	f.write(xCal_x_avg_json_y50)
	f.close()

	xCal_x_avg_json_y50_sdev = json.dumps(xCalibrate_x_avg_y50_sdev)
	f = open(os.path.join(dirName, "xCal_x_avg_y50_sdev.json"), "w")
	f.write(xCal_x_avg_json_y50_sdev)
	f.close()

	xCal_x_avg_json_y100 = json.dumps(xCalibrate_x_avg_y100)
	f = open(os.path.join(dirName, "xCal_x_avg_y100.json"), "w")
	f.write(xCal_x_avg_json_y100)
	f.close()

	xCal_x_avg_json_y100_sdev = json.dumps(xCalibrate_x_avg_y100_sdev)
	f = open(os.path.join(dirName, "xCal_x_avg_y100_sdev.json"), "w")
	f.write(xCal_x_avg_json_y100_sdev)
	f.close()

	xCal_y_avg_json_y0 = json.dumps(xCalibrate_y_avg_y0)
	f = open(os.path.join(dirName, "xCal_y_avg_y0.json"), "w")
	f.write(xCal_y_avg_json_y0)
	f.close()

	xCal_y_avg_json_y0_sdev = json.dumps(xCalibrate_y_avg_y0_sdev)
	f = open(os.path.join(dirName, "xCal_y_avg_y0_sdev.json"), "w")
	f.write(xCal_y_avg_json_y0_sdev)
	f.close()

	xCal_y_avg_json_y50 = json.dumps(xCalibrate_y_avg_y50)
	f = open(os.path.join(dirName, "xCal_y_avg_y50.json"), "w")
	f.write(xCal_y_avg_json_y50)
	f.close()

	xCal_y_avg_json_y50_sdev = json.dumps(xCalibrate_y_avg_y50_sdev)
	f = open(os.path.join(dirName, "xCal_y_avg_y50_sdev.json"), "w")
	f.write(xCal_y_avg_json_y50_sdev)
	f.close()

	xCal_y_avg_json_y100 = json.dumps(xCalibrate_y_avg_y100)
	f = open(os.path.join(dirName, "xCal_y_avg_y100.json"), "w")
	f.write(xCal_y_avg_json_y100)
	f.close()

	xCal_y_avg_json_y100_sdev = json.dumps(xCalibrate_y_avg_y100_sdev)
	f = open(os.path.join(dirName, "xCal_y_avg_y100_sdev.json"), "w")
	f.write(xCal_y_avg_json_y100_sdev)
	f.close()

	

	#store values from the y calibration

	yCal_x_avg_json_x0 = json.dumps(yCalibrate_x_avg_x0)
	f = open(os.path.join(dirName, "yCal_x_avg_x0.json"), "w")
	f.write(yCal_x_avg_json_x0)
	f.close()

	yCal_x_avg_json_x0_sdev = json.dumps(yCalibrate_x_avg_x0_sdev)
	f = open(os.path.join(dirName, "yCal_x_avg_x0_sdev.json"), "w")
	f.write(yCal_x_avg_json_x0_sdev)
	f.close()

	yCal_x_avg_json_x50 = json.dumps(yCalibrate_x_avg_x50)
	f = open(os.path.join(dirName, "yCal_x_avg_x50.json"), "w")
	f.write(yCal_x_avg_json_x50)
	f.close()

	yCal_x_avg_json_x50_sdev = json.dumps(yCalibrate_x_avg_x50_sdev)
	f = open(os.path.join(dirName, "yCal_x_avg_x50_sdev.json"), "w")
	f.write(yCal_x_avg_json_x50_sdev)
	f.close()

	yCal_x_avg_json_x100 = json.dumps(yCalibrate_x_avg_x100)
	f = open(os.path.join(dirName, "yCal_x_avg_x100.json"), "w")
	f.write(yCal_x_avg_json_x100)
	f.close()

	yCal_x_avg_json_x100_sdev = json.dumps(yCalibrate_x_avg_x100_sdev)
	f = open(os.path.join(dirName, "yCal_x_avg_x100_sdev.json"), "w")
	f.write(yCal_x_avg_json_x100_sdev)
	f.close()

	yCal_y_avg_json_x0 = json.dumps(yCalibrate_y_avg_x0)
	f = open(os.path.join(dirName, "yCal_y_avg_x0.json"), "w")
	f.write(yCal_y_avg_json_x0)
	f.close()

	yCal_y_avg_json_x0_sdev = json.dumps(yCalibrate_y_avg_x0_sdev)
	f = open(os.path.join(dirName, "yCal_y_avg_x0_sdev.json"), "w")
	f.write(yCal_y_avg_json_x0_sdev)
	f.close()
	
	yCal_y_avg_json_x50 = json.dumps(yCalibrate_y_avg_x50)
	f = open(os.path.join(dirName, "yCal_y_avg_x50.json"), "w")
	f.write(yCal_y_avg_json_x50)
	f.close()

	yCal_y_avg_json_x50_sdev = json.dumps(yCalibrate_y_avg_x50_sdev)
	f = open(os.path.join(dirName, "yCal_y_avg_x50_sdev.json"), "w")
	f.write(yCal_y_avg_json_x50_sdev)
	f.close()

	yCal_y_avg_json_x100 = json.dumps(yCalibrate_y_avg_x100)
	f = open(os.path.join(dirName, "yCal_y_avg_x100.json"), "w")
	f.write(yCal_y_avg_json_x100)
	f.close()

	yCal_y_avg_json_x100_sdev = json.dumps(yCalibrate_y_avg_x100_sdev)
	f = open(os.path.join(dirName, "yCal_y_avg_x100_sdev.json"), "w")
	f.write(yCal_y_avg_json_x100_sdev)
	f.close()
	
	#Store values from both calibration

	bothCal_x_avg_json = json.dumps(bothCalibrate_x_avg)
	f= open(os.path.join(dirName, "bothCal_x_avg.json"), "w")
	f.write(bothCal_x_avg_json)
	f.close()

	bothCal_x_avg_json_sdev = json.dumps(bothCalibrate_x_avg_sdev)
	f= open(os.path.join(dirName, "bothCal_x_avg_sdev.json"), "w")
	f.write(bothCal_x_avg_json_sdev)
	f.close()

	bothCal_y_avg_json = json.dumps(bothCalibrate_y_avg)
	f= open(os.path.join(dirName, "bothCal_y_avg.json"), "w")
	f.write(bothCal_y_avg_json)
	f.close()
	
	bothCal_y_avg_json_sdev = json.dumps(bothCalibrate_y_avg_sdev)
	f= open(os.path.join(dirName, "bothCal_y_avg_sdev.json"), "w")
	f.write(bothCal_y_avg_json_sdev)
	f.close()

	
	
	#save the raw data because why not

	xCalibrateReadings_y0_raw = json.dumps(xCalibrateReadings_y0)
	f= open(os.path.join(dirName, "xCalibrateReadings_y0_raw.json"), "w")
	f.write(xCalibrateReadings_y0_raw)
	f.close()

	xCalibrateReadings_y50_raw = json.dumps(xCalibrateReadings_y50)
	f= open(os.path.join(dirName, "xCalibrateReadings_y50_raw.json"), "w")
	f.write(xCalibrateReadings_y50_raw)
	f.close()

	xCalibrateReadings_y100_raw = json.dumps(xCalibrateReadings_y100)
	f= open(os.path.join(dirName, "xCalibrateReadings_y100_raw.json"), "w")
	f.write(xCalibrateReadings_y100_raw)
	f.close()

	yCalibrateReadings_x0_raw = json.dumps(yCalibrateReadings_x0)
	f= open(os.path.join(dirName, "yCalibrateReadings_x0_raw.json"), "w")
	f.write(yCalibrateReadings_x0_raw)
	f.close()

	yCalibrateReadings_x50_raw = json.dumps(yCalibrateReadings_x50)
	f= open(os.path.join(dirName, "yCalibrateReadings_x50_raw.json"), "w")
	f.write(yCalibrateReadings_x50_raw)
	f.close()

	yCalibrateReadings_x100_raw = json.dumps(yCalibrateReadings_x100)
	f= open(os.path.join(dirName, "yCalibrateReadings_x0_raw.json"), "w")
	f.write(yCalibrateReadings_x100_raw)
	f.close()


	bothCalibrateReadings_raw = json.dumps(bothCalibrateReadings)
	f= open(os.path.join(dirName, "bothCalibrateReadings_raw.json"), "w")
	f.write(bothCalibrateReadings_raw)
	f.close()

	

	print("data successfully saved to " + dirName)


	
	