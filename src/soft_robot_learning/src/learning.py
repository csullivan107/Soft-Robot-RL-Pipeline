#!/usr/bin/env python3
#you need this above to get ROS to execute the script - points to the python executable
#use python 3 here due to the RL libraries being written in python 3
from gym import spaces
import gym
import numpy as np
import time
import random
from math import sqrt

# from stable_baselines.td3.policies import MlpPolicy as Td3MlpPolicy
# # from stable_baselines import TD3
# from stable_baselines.ddpg.noise import OrnsteinUhlenbeckActionNoise
# from stable_baselines.common.vec_env import DummyVecEnv 


#import necessary stable baselines TD3 libraries for learning purposes
from stable_baselines import TD3
from stable_baselines.td3.policies import MlpPolicy as Td3MlpPolicy
from stable_baselines.ddpg.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines.common.vec_env import DummyVecEnv
#import ROS specific libraries and custom message types
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Empty
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

xZero = 0. #zero values for each episode
yZero = 0.

action_done = False



#define constants
NUM_STEPS = 10
TIME_PER_STEP = 1 #this could be variable depending on hardware

# define ROS publisher nodes
cmd_pub = rospy.Publisher('/actuator_commands', gcode_packager, queue_size = 30)
direct_cmd_publisher = rospy.Publisher('/grbl_commands', String, queue_size = 30)
grbl_reset_pub = rospy.Publisher('/system_cmd', Empty, queue_size=1)
#test pub to update the subscribed node. for testing
testpub = rospy.Publisher('/testData', String, queue_size = 20)

#define ROS subscriber callback methods
def robot_state_callback(data):
	#print("Updating State")
	global xState
	global yState
	xState = data.xSensor
	yState = data.ySensor
	#print("x sensor: {}", format(xState))
	#print("y sensor: {}", format(yState))	

def gnd_truth_callback(data):
	#print("updating Ground Truth Data")
	global xPosition, yPosition
	xPosition = data.x_pos_gnd
	yPosition = data.y_pos_gnd
	#print("x position: {}", format(xPosition))
	#print("y position: {}", format(yPosition))

def action_done_callback(data):
	global action_done
	action_done = data.data

def testData_callback(data):
	#print("test data recieved")
	global testString
	testString = data.data + '\n'
	


#Define ROS subscriber nodes
def RL_subscribers():
    rospy.init_node('soft_robot_learning', anonymous=True)
    rospy.Subscriber("/robot_state", sensor_processing, robot_state_callback)
    rospy.Subscriber("/gnd_pos_truth", apriltag_data, gnd_truth_callback)
    rospy.Subscriber("/action_done", Bool, action_done_callback)
    rospy.Subscriber("/testData", String, testData_callback)

    # skipping spin to see if the subscriber works without spinnign whle the thin is running
    #rospy.spin()	

def distanceFromOrigin(x,y,xZero,yZero):
	xDist = x - xZero
	yDist = y - yZero
	total_distance = sqrt(xDist*xDist+yDist*yDist)
	return total_distance, xDist, yDist

def wait_for_action():
	global action_done
	count = 0
	while not action_done:
		count = count + 1
		#print(action_done)
		
	print("Action Complete...")
	time.sleep(1)



def homeGrblController():
	print("Homing System....")
	direct_cmd_publisher.publish('$H')
	wait_for_action()
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
	


class soft_learner():
	def __init__(self):
		#init position variables
		self.testS = "" #test string for testing data passing
		self.x = 0
		self.y = 0
		#init steps and dt (time per step)
		self.n_steps = 0
		self.dt = TIME_PER_STEP #1=1second - play with this variable
		#initialize proper spaces and metadata 
		#both the action and state space are bounded by 0-100 for %of actuation
		#mapping these to real world actiona dnnand sensors are handeled in another script
		self.observation_space = spaces.Box(low=np.array([0.,0.]), high=np.array([100.,100.])) #obs space = continuous, 
		self.action_space = spaces.Box(low=np.array([0.,0.]), high=np.array([100.,100.]))
#since each action is broken out here i am going to say the action space is only one


		self.metadata = 0

		#send initial commands to grbl (home, set 0 all that)

	def reset(self):
		global xZero, yZero, xPosition, yPosition
		self.x = 0
		self.y = 0
		self.n_steps = 0
		
		
		#re calibrate and set x and y zero values for each new run for april tags data
		xZero = xPosition
		yZero = yPosition

		#reset grbl controller
		resetGrblController()

		#run calibration function here
		return self.x, self.y

	def step(self, generated_cmd_array):
		global xCommand, yCommand, xPosition, yPosition, xZero, yZero, xState, yState
		
		# print(generated_cmd_array)
		# xCommand = generated_cmd_array[0]
		# yCommand = generated_cmd_array[1]
		# xCommand = np.clip(xCommand, self.action_space.low, self.action_space.high)
		# yCommand = np.clip(yCommand, self.action_space.low, self.action_space.high)
		generated_cmd_array = np.clip(generated_cmd_array, self.action_space.low, self.action_space.high)

		#generate an action
		# xCommand = random.randint(0,100)
		# yCommand = random.randint(0,100)
		print("command generated x {} y {}", format(generated_cmd_array[0]), format(generated_cmd_array[1]))
		#v = np.clip(v, self.action_space.low, self.action_space.high)
		#above line in example not sure why it is used

		#publish action
		cmd_message = gcode_packager()
		# cmd_message.x_percentage = xCommand
		# cmd_message.y_percentage = yCommand
		cmd_message.x_percentage = generated_cmd_array[0]
		cmd_message.y_percentage = generated_cmd_array[1]
		cmd_pub.publish(cmd_message)

		#wait for hardware to complete action
		wait_for_action()

		#subscribe/read state
		# state = {'x': xState, 'y': yState}
		state = [xState, yState]
		print("xState: {}", format(state[0]))
		print("yState: {}", format(state[1]))

		#compute reward
		reward, x_calibrated, y_calibrated = distanceFromOrigin(xPosition,yPosition, xZero,yZero)
		#print("x position: {}", format(xPosition))
		#print("y position: {}", format(yPosition))
		print("x calibrated: {}", format(x_calibrated))
		print("y calibrated: {}", format(y_calibrated))
		print("reward: {}", format(reward))

		#increment and finish step
		self.n_steps += 1
		done = self.n_steps > NUM_STEPS

		return state, reward, done, {}


if __name__ == '__main__':
	
	#run suscriber nodes
	RL_subscribers()
	print("Starting...")

	time.sleep(3) #give ros time to set up

	#init environmnet
	env = soft_learner()
	env.reset()

	#run and testing

	a_dim = env.action_space.shape[0]
	td3_noise = OrnsteinUhlenbeckActionNoise(np.zeros(a_dim), 0.003*np.ones(a_dim)) 
	td3_env = DummyVecEnv([lambda: env])
	td3_model = TD3(Td3MlpPolicy, td3_env, verbose=0, action_noise=td3_noise, tensorboard_log='tensorboard')
	td3_model.learn(total_timesteps=100)
	td3_model.save("td3_model")
	print('Complete training TD3')
	# x = td3_env.reset()
#     for i in range(100): 
#         x, r, _, _ = td3_env.step(td3_model.predict(x)) 
#     print(x) 
#     print(r) 
	




	
	# #rospy.spin()
	# print("running sensor mount testing")
	# count = 1
	# cmd_message = gcode_packager()
	# while True:
	# 	cmd_message.x_percentage = 95
	# 	cmd_message.y_percentage = 0
	# 	cmd_pub.publish(cmd_message)
	# 	wait_for_action()
	# 	print("fully inflated...")
	# 	cmd_message.x_percentage = 0
	# 	cmd_message.y_percentage = 0
	# 	cmd_pub.publish(cmd_message)
	# 	wait_for_action()
	# 	print("Not inflated...")
	# 	count =count+1
	# 	print (count)
	# 	if (count%10 == 0):
	# 		resetGrblController()

	# #for i in range(10):
	# #	time.sleep(1)
	# #	env.step()



