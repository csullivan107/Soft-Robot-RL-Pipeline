#!/usr/bin/env python3
#you need this above to get ROS to execute the script - points to the python executable
#use python 3 here due to the RL libraries being written in python 3

import numpy as np
import matplotlib.pyplot as plt
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

# with open('bothCal_x_avg.json') as bothCal_x:
# 	dictData = json.load(bothCal_x)
# 	pp.pprint(dictData)
# 	print (dictData[str(90)])

# 	plt.title('SENSOR READINGS')
# 	plt.xlabel('% ACTUATOR (0-100)')
# 	plt.ylabel('Sensor Reading (0-1024)')
# 	x = list(map(int,(list(dictData.keys())))) 
# 	y = list(dictData.values())
# 	# x = list(map(int,x))
# 	print(x)
# 	print(y)
# 	plt.plot(x,y)
# 	plt.show()

def loadData():
	files = []
	files.append(open('bothCal_x_avg.json'))
	files.append(open('bothCal_y_avg.json'))
	files.append(open('xCal_x_avg.json'))
	files.append(open('xCal_y_avg.json'))
	files.append(open('yCal_x_avg.json'))
	files.append(open('yCal_y_avg.json'))

	print (files)

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
	
	return xAxis_data,yAxis_data
	

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
	
def normalizeData(x_data y_data):
	#using zscore
	

if __name__ == '__main__':

	x_data, y_data = loadData()
	plt = plotData(x_data, y_data)
	# formatPlotData(plt)

	


	