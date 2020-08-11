#!/usr/bin/env python3
#you need this above to get ROS to execute the script - points to the python executable
#use python 3 here due to the RL libraries being written in python 3

import numpy as np
import matplotlib.pyplot as plt
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)


def loadData():
	files = []
	files.append(open('bothCal_x_avg.json'))
	files.append(open('bothCal_y_avg.json'))
	files.append(open('xCal_x_avg_y0.json'))
	files.append(open('xCal_x_avg_y50.json'))
	files.append(open('xCal_x_avg_y100.json'))
	files.append(open('xCal_y_avg_y0.json'))
	files.append(open('xCal_y_avg_y50.json'))
	files.append(open('xCal_y_avg_y100.json'))
	files.append(open('yCal_x_avg_x0.json'))
	files.append(open('yCal_x_avg_x50.json'))
	files.append(open('yCal_x_avg_x100.json'))
	files.append(open('yCal_y_avg_x0.json'))
	files.append(open('yCal_y_avg_x50.json'))
	files.append(open('yCal_y_avg_x100.json'))

	
	xAxis_data = []
	yAxis_data = []
	for f in files:
		# dictionaries.append(json.load(f))
		dictData = json.load(f)
		x = list(map(int,(list(dictData.keys())))) 
		y = list(dictData.values())
		xAxis_data.append(x)
		yAxis_data.append(y)

		# print (xAxis_data)
		# print ('-------------------------------------------------')
		# print (yAxis_data)
	
	return xAxis_data, yAxis_data
	

def plotData(x_data,y_data):

	plt.title('SENSOR READINGS')
	plt.xlabel('% ACTUATOR (0-100)')
	plt.ylabel('Sensor Reading (0-1024)')

	for (x,y) in zip(x_data,y_data):
		print(x)
		print(y)
		# plt.plot(x,y)

	both_x_sd = np.std(y_data[0])
	print (both_x_sd)

	both_x = plt.plot(x_data[0],y_data[0], '-g', label='Both Actuators used - Right Actuator')	#both x
	both_y = plt.plot(x_data[1],y_data[1], '-b', label='Both Actuators used - Left Actuator')	#both y
	x_x = plt.plot(x_data[2],y_data[2], '--g', label='Right Actuator used - Right Actuator')	#x x
	x_y = plt.plot(x_data[3],y_data[3], '--b', label='Right Actuators used - Left Actuator')	#x y	
	y_x = plt.plot(x_data[4],y_data[4], ':g', label='Left Actuators used - Right Actuator')	#y x
	y_y = plt.plot(x_data[5],y_data[5], ':b', label='Left Actuators used - Left Actuator')	#y y

	plt.legend()

	plt.show()
	return plt
	
def plotXcal(x_data,y_data, robotName):


	fig1 = plt.figure('X_cal_x_Actuator' + robotName)
	plt.title('Right Actuator Calibration - Right Actuator Readings\n'+robotName)
	plt.xlabel('Actuation (0-100)% - Right Actuator')
	plt.ylabel('Sensor Reading (0-1024) - Right Actuator')

	x_y0 = plt.plot(x_data[2],y_data[2], 'r', label='Left Actuator held at 0%')
	x_y50 = plt.plot(x_data[3],y_data[3], 'y', label='Left Actuator held at 50%')
	x_y100 = plt.plot(x_data[4],y_data[4], 'b', label='Left Actuator held at 0%')
	both_x = plt.plot(x_data[0],y_data[0], '-.c', label='Both Actuators Used Simultaneously')
	plt.grid()
	plt.subplots_adjust(bottom=.25)
	plt.legend(bbox_to_anchor=(.5,0), loc="lower center", bbox_transform=fig1.transFigure, ncol=2)

	fig2 = plt.figure('X_cal_y_Actuator')
	plt.title('Right Actuator Calibration - Left Actuator Readings\n'+robotName)
	plt.xlabel('Actuation (0-100)% - Right Actuator')
	plt.ylabel('Sensor Reading (0-1024) Left Actuator')

	y_y0 = plt.plot(x_data[5],y_data[5], '--r', label='Left Actuator held at 0%')	
	y_y50 = plt.plot(x_data[6],y_data[6], '--y', label='Left Actuator held at 50%')
	y_y100 = plt.plot(x_data[7],y_data[7], '--b', label='Left Actuator held at 100%')
	plt.grid()
	plt.subplots_adjust(bottom=.25)
	plt.legend(bbox_to_anchor=(.5,0), loc="lower center", bbox_transform=fig2.transFigure, ncol=2)

	
	
	return 0

def plotYcal(x_data,y_data, robotName):
	fig1 = plt.figure('Y_cal_x_Actuator')
	plt.title('Left Actuator Calibration - Right Actuator Readings\n'+robotName)
	plt.xlabel('Actuation (0-100)% - Left Actuator')
	plt.ylabel('Sensor Reading (0-1024) Right Actuator')

	x_x0 = plt.plot(x_data[8],y_data[8], '--r', label='Right Actuator Held at 0%')
	x_x50 = plt.plot(x_data[9],y_data[9], '--y', label='Right Actuator Held at 50%')
	x_x100 = plt.plot(x_data[10],y_data[10], '--b', label='Right Actuator Held at 100%')
	plt.grid()
	plt.subplots_adjust(bottom=.25)
	plt.legend(bbox_to_anchor=(.5,0), loc="lower center", bbox_transform=fig1.transFigure, ncol=2)
	

	fig2 = plt.figure('Y_cal_y_Actuator')
	plt.title('Left Actuator Calibration - Left Actuator Readings\n'+robotName)
	plt.xlabel('Actuation (0-100)%  - Left Actuator')
	plt.ylabel('Sensor Reading (0-1024) Left Actuator')

	y_y0 = plt.plot(x_data[11],y_data[11], 'r', label='Right Actuator Held at 0%')	
	y_y50 = plt.plot(x_data[12],y_data[12], 'y', label='Right Actuator Held at 50%')
	y_y100 = plt.plot(x_data[13],y_data[13], 'b', label='Right Actuator Held at 100%')
	both_y = plt.plot(x_data[1],y_data[1], '-.c', label='Both Actuators Used Simultaneously')
	plt.grid()
	plt.subplots_adjust(bottom=.25)
	plt.legend(bbox_to_anchor=(.5,0), loc="lower center", bbox_transform=fig2.transFigure, ncol=2)
	
	

# this function is not used	
def plotBothcal(x_data,y_data):
	plt.figure('both_cal_x_Actuator')
	plt.title(' Actuator Calibration - X Actuator Readings')
	plt.xlabel('% ACTUATION (0-100)')
	plt.ylabel('Sensor Reading (0-1024)')

	both_x = plt.plot(x_data[0],y_data[0], '--r', label='Right Actuator Readings - R(0))')
	both_y = plt.plot(x_data[1],y_data[1], '--r', label='Right Actuator Readings - R(0))')
	
	plt.grid()
	plt.legend()
	
	
	return 0

def formatPlotData(plt):
	print("fart")

if __name__ == '__main__':

	robotName = "Robot 1"

	x_data, y_data = loadData()
	_ = plotXcal(x_data, y_data,robotName)
	_ = plotYcal(x_data, y_data,robotName)
	# formatPlotData(plt)
	
	plt.show()
	exit()

	


	