#!/usr/bin/env python
#you need this above to get ROS to execute the script
from gym import spaces
import numpy as np
import time
#import necessary stable baselines TD3 libraries for learning purposes

#import ROS specific libraries and custom message types
import rospy
from std_msgs.msg import String
from soft_robot_learning.msg import sensor_processing
from soft_robot_learning.msg import gcode_packager
from soft_robot_learning.msg import apriltag_data


#global variables
testString = ""

xCommand = 0.
yCommand = 0.

xState = 0.
yState = 0.

xPosition = 0.
yPosition = 0.

#define constants
NUM_STEPS = 1000
TIME_PER_STEP = 1 #this could be variable depending on hardware

# define ROS publisher nodes
cmd_pub = rospy.Publisher('/actuator_commands', gcode_packager, queue_size = 30)
#test pub to update the subscribed node. for testing
testpub = rospy.Publisher('/testData', String, queue_size = 20)

#define ROS subscriber callback methods
def robot_state_callback(data):
	print("Updating State")
	global xState
	global yState
	xState = data.xSensor
	yState = data.ySensor
	print("x sensor: {}", format(xState))
	print("y sensor: {}", format(yState))
	
	

def gnd_truth_callback(data):
	print("updating Ground Truth Data")

def testData_callback(data):
	#print("test data recieved")
	global testString
	testString = data.data + '\n'
	


#Define ROS subscriber nodes
def RL_subscribers():
    rospy.init_node('soft_robot_learning', anonymous=True)
    rospy.Subscriber("/robot_state", sensor_processing, robot_state_callback)
    rospy.Subscriber("/gnd_pos_truth", apriltag_data, gnd_truth_callback)
    rospy.Subscriber("/testData", String, testData_callback)

    # skipping spin to see if the subscriber works without spinnign whle the thin is running
    #rospy.spin()	

class soft_learner():
	def __init__(self):
		#init position variables
		self.testS = "" #test string for testing data passing
		self.x = 0
		self.y = 0
		#init steps and dt (time per step)
		self.n_steps = 0
		self.dt = TIME_PER_STEP #1=1second - play with this variable
		#initialize proper spaces and metadata (this is not used for now)
		self.opservation_space = spaces.Box(low=np.array([0]), high=np.array([100])) #obs space = continuous, 
		self.action_space = spaces.Box(low=np.array([0.]), high=np.array([100]))
		self.metadata = 0

	def reset(self):
		self.x = 0
		self.y = 0
		self.n_steps = 0
		return self.x, self.y

	def step(self, testnum):
		#original testing code
		
		#generate an action

		#publish action
		
		testpub.publish("testpub: " + str(testnum))

		#wait for hardware to complete action

		#subscribe/read state
		global testString
		self.testS = testString
		print("Step -- subscribed info: {}", format(self.testS))

		#compute reward

		#increment and finish step
		self.n_steps += 1
		done = self.n_steps > NUM_STEPS

		#return state, reward, done, {}



if __name__ == '__main__':
	#run suscriber nodes
	RL_subscribers()
	print "out of subscriber init"

	#init environmnet
	env = soft_learner()
	env.reset()
	rospy.spin()
	# for i in range(20):
	# 	print(testString)
	# 	#testpub.publish("i = " + str(i))
	# 	time.sleep(1)
	# 	env.step(i)


