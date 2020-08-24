#!/usr/bin/env python
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

	#set to 100
	direct_cmd_publisher.publish('G0 X100 Y100')
	wait_for_action()

	x_readings = {}
	y_readings = {}
	minutes = 0
	#read sensors overnight every 5 minutes for.... 12 hours (144 readings)
	print("Starting leak test...")
	for i in range(144):
		x_readings[minutes]=xState_global
		y_readings[minutes]=yState_global
		
		
		print('----------------- ' + str(minutes) + ' Minutes Passed -------------------')
		print('\t\tX Sensor Reading: ' + str(x_readings[minutes]))
		print('\t\tY Sensor Reading: ' + str(y_readings[minutes]))

		minutes += 5
		time.sleep(300) #wat 2 minutes 600 total

	#save to files... json
	run = 0
	baseDir = 'sensor_calibration_files/leak_test_'


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
		
	pp.pprint(x_readings)
	pp.pprint(y_readings)

	print("Saving Data")

	#store values from leak test
	x_readings_json = json.dumps(x_readings)
	f = open(os.path.join(dirName, "x_readings.json"), "w")
	f.write(x_readings_json)
	f.close()

	y_readings_json = json.dumps(y_readings)
	f = open(os.path.join(dirName, "y_readings.json"), "w")
	f.write(y_readings_json)
	f.close()

	# #calibrate the x axis sensor at various y values
	# xCalibrateReadings_y0 = calibrateAxis('x',0)
	# xCalibrateReadings_y50 = calibrateAxis('x',50)
	# xCalibrateReadings_y100 = calibrateAxis('x',100)

	# #collect and average the readings for both axes during the calibration cycle
	# xCalibrate_x_avg_y0 = averageReadings(xCalibrateReadings_y0['xAxis'])
	# xCalibrate_x_avg_y50 = averageReadings(xCalibrateReadings_y50['xAxis'])
	# xCalibrate_x_avg_y100 = averageReadings(xCalibrateReadings_y100['xAxis'])
	# xCalibrate_y_avg_y0 = averageReadings(xCalibrateReadings_y0['yAxis'])
	# xCalibrate_y_avg_y50 = averageReadings(xCalibrateReadings_y50['yAxis'])
	# xCalibrate_y_avg_y100 = averageReadings(xCalibrateReadings_y100['yAxis'])

	# #calibrate y axis at various x axis values
	# yCalibrateReadings_x0 = calibrateAxis('y',0)
	# yCalibrateReadings_x50 = calibrateAxis('y',50)
	# yCalibrateReadings_x100 = calibrateAxis('y',100)

	# #collect acerages for bothe axes
	# yCalibrate_x_avg_x0 = averageReadings(yCalibrateReadings_x0['xAxis'])
	# yCalibrate_x_avg_x50 = averageReadings(yCalibrateReadings_x50['xAxis'])
	# yCalibrate_x_avg_x100 = averageReadings(yCalibrateReadings_x100['xAxis'])
	# yCalibrate_y_avg_x0 = averageReadings(yCalibrateReadings_x0['yAxis'])
	# yCalibrate_y_avg_x50 = averageReadings(yCalibrateReadings_x50['yAxis'])
	# yCalibrate_y_avg_x100 = averageReadings(yCalibrateReadings_x100['yAxis'])

	# #run both axes at the same time and colelct readings
	# bothCalibrateReadings = calibrateAxis('both',0)

	# #average readings for running both axes at once
	# bothCalibrate_x_avg = averageReadings(bothCalibrateReadings['xAxis'])
	# bothCalibrate_y_avg = averageReadings(bothCalibrateReadings['yAxis'])
	
	# #save to files... json
	# run = 0
	# baseDir = 'sensor_calibration_files/Calibration_run_'


	# t = datetime.datetime.now()
	# t = t.strftime("%m_%d_%y_%X/")
	# dirName = baseDir + t 
	# if not os.path.exists(dirName):
	# 	os.makedirs(dirName)
	# 	print(dirName + " created successfully")
	# 	done = True
	# else:
	# 	print(dirName + " exists")
	# 	run += 1
		
	# print("Saving Data")


	# #store values from x calibration runs
	# xCal_x_avg_json_y0 = json.dumps(xCalibrate_x_avg_y0)
	# f = open(os.path.join(dirName, "xCal_x_avg_y0.json"), "w")
	# f.write(xCal_x_avg_json_y0)
	# f.close()

	# xCal_x_avg_json_y50 = json.dumps(xCalibrate_x_avg_y50)
	# f = open(os.path.join(dirName, "xCal_x_avg_y50.json"), "w")
	# f.write(xCal_x_avg_json_y50)
	# f.close()

	# xCal_x_avg_json_y100 = json.dumps(xCalibrate_x_avg_y100)
	# f = open(os.path.join(dirName, "xCal_x_avg_y100.json"), "w")
	# f.write(xCal_x_avg_json_y100)
	# f.close()

	# xCal_y_avg_json_y0 = json.dumps(xCalibrate_y_avg_y0)
	# f = open(os.path.join(dirName, "xCal_y_avg_y0.json"), "w")
	# f.write(xCal_y_avg_json_y0)
	# f.close()

	# xCal_y_avg_json_y50 = json.dumps(xCalibrate_y_avg_y50)
	# f = open(os.path.join(dirName, "xCal_y_avg_y50.json"), "w")
	# f.write(xCal_y_avg_json_y50)
	# f.close()

	# xCal_y_avg_json_y100 = json.dumps(xCalibrate_y_avg_y100)
	# f = open(os.path.join(dirName, "xCal_y_avg_y100.json"), "w")
	# f.write(xCal_y_avg_json_y100)
	# f.close()

	# #store values from the y calibration

	# yCal_x_avg_json_x0 = json.dumps(yCalibrate_x_avg_x0)
	# f = open(os.path.join(dirName, "yCal_x_avg_x0.json"), "w")
	# f.write(yCal_x_avg_json_x0)
	# f.close()

	# yCal_x_avg_json_x50 = json.dumps(yCalibrate_x_avg_x50)
	# f = open(os.path.join(dirName, "yCal_x_avg_x50.json"), "w")
	# f.write(yCal_x_avg_json_x50)
	# f.close()

	# yCal_x_avg_json_x100 = json.dumps(yCalibrate_x_avg_x100)
	# f = open(os.path.join(dirName, "yCal_x_avg_x100.json"), "w")
	# f.write(yCal_x_avg_json_x100)
	# f.close()

	# yCal_y_avg_json_x0 = json.dumps(yCalibrate_y_avg_x0)
	# f = open(os.path.join(dirName, "yCal_y_avg_x0.json"), "w")
	# f.write(yCal_y_avg_json_x0)
	# f.close()
	
	# yCal_y_avg_json_x50 = json.dumps(yCalibrate_y_avg_x50)
	# f = open(os.path.join(dirName, "yCal_y_avg_x50.json"), "w")
	# f.write(yCal_y_avg_json_x50)
	# f.close()

	# yCal_y_avg_json_x100 = json.dumps(yCalibrate_y_avg_x100)
	# f = open(os.path.join(dirName, "yCal_y_avg_x100.json"), "w")
	# f.write(yCal_y_avg_json_x100)
	# f.close()
	# #---------------

	# bothCal_x_avg_json = json.dumps(bothCalibrate_x_avg)
	# f= open(os.path.join(dirName, "bothCal_x_avg.json"), "w")
	# f.write(bothCal_x_avg_json)
	# f.close()

	# bothCal_y_avg_json = json.dumps(bothCalibrate_y_avg)
	# f= open(os.path.join(dirName, "bothCal_y_avg.json"), "w")
	# f.write(bothCal_y_avg_json)
	# f.close()

	# print("data successfully saved to " + dirName)


