#!/usr/bin/env python3
#you need this above to get ROS to execute the script - points to the python executable
#use python 3 here due to the RL libraries being written in python 3
from gym import spaces
import gym
import numpy as np
import time
import random
from math import sqrt
import datetime
import os

# from stable_baselines.td3.policies import MlpPolicy as Td3MlpPolicy
# # from stable_baselines import TD3
# from stable_baselines.ddpg.noise import OrnsteinUhlenbeckActionNoise
# from stable_baselines.common.vec_env import DummyVecEnv 


#import necessary stable baselines TD3 libraries for learning purposes
# from stable_baselines import TD3
from stable_baselines import DDPG
from stable_baselines.ddpg.policies import MlpPolicy as DDPGMlpPolicy
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
#sensor readings
xState_global = 0.
yState_global = 0.
#apriltag readings
xPos_global = 0.
yPos_global = 0.

xZero = 0. #zero values for each episode
yZero = 0.

action_done = False

#define constants
NUM_STEPS_EPISODE = 24 #index at 0 - (desirednum - 1)
TOTAL_STEPS = 2000
TIME_PER_STEP = 1 #this could be variable depending on hardware
robotName = "robot_1"
NOISE_CONSTANT = 3.5

#here are the constants for the TD3 Model
GAMMA = 0.99
LEARNING_RATE = .0003
BUFFER_SIZE = 50000
LEARNING_STARTS = 100
TRAIN_FREQ = 100
GRADIENT_STEPS = 100
BATCH_SIZE = 128
TAU = .005
POLICY_DELAY = 2
# ACTION_NOISE = None | this is set later when you build the noise generator
TARGET_POLICY_NOISE = 0.2
TARGET_NOISE_CLIP = 0.5
RANDOM_EXPLORATION = 0.0
VERBOSE = 0
TENSORBOARD_LOG = 'tensorboard'
_INIT_SETUP_MODEL = True
POLICY_KWARGS = None
FULL_TENSORBOARD_LOG = False
SEED = None
N_CPU_TF_SESS = None



#set up a log file for the printed output
baseDir = 'src/soft_robot_learning/src/learning_logs/' + robotName + '/learining_run_DDPG_'


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
		
file = open(os.path.join(dirName, "learn.txt"), "w")
file.close()


# ACTUATOR_X_MAX = rospy.get_param('/xActMax')
# ACTUATOR_X_MIN = rospy.get_param('/xActMin')
# ACTUATOR_y_MAX = rospy.get_param('/yActMax')
# ACTUATOR_y_MIN = rospy.get_param('/yActMin')




# define ROS publisher nodes
cmd_pub = rospy.Publisher('/actuator_commands', gcode_packager, queue_size = 30)
direct_cmd_publisher = rospy.Publisher('/grbl_commands', String, queue_size = 30)
grbl_reset_pub = rospy.Publisher('/system_cmd', Empty, queue_size=1)
#test pub to update the subscribed node. for testing
testpub = rospy.Publisher('/testData', String, queue_size = 20)

#define ROS subscriber callback methods
def robot_state_callback(data):
	#print("Updating State")
	global xState_global
	global yState_global
	xState_global = data.xSensor
	yState_global = data.ySensor
	#print("x sensor: {}", format(xState))
	#print("y sensor: {}", format(yState))	

def gnd_truth_callback(data):
	#print("updating Ground Truth Data")
	global xPos_global, yPos_global
	xPos_global = data.x_pos_gnd
	yPos_global = data.y_pos_gnd
	# print("x position: {}", format(xPosition))
	# print("y position: {}", format(yPosition))

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
	# 
	# 
#Define various functions used throughout script	

def rewardCalculation(x_current, y_current, x_startstep, y_startstep):
	xDist = x_current - x_startstep
	yDist = y_current - y_startstep

	reward = yDist*1000

	# if yDist < 0:
	# 	#moved backwards
	# 	reward = yDist * 1000
	# else:
	# 	#moved forward
	# 	reward = yDist * 1000 #positions given in meters so to make reward large use mm

	#improved reward calculation

	# reward = 10
	return reward

def wait_for_action():
	global action_done
	count = 0
	while not action_done:
		count = count + 1
		#print(action_done)
		
	print("\t--Action Complete--\t|")
	time.sleep(1)

def screenCmdData(generated, xPrev, yPrev):
	global step_count
	checkRange = 1
	changeAmount = 1.5
	
	
	xGen = generated[0]
	yGen = generated[1]

	

	#find difference between generaged and previous command
	xDiff = xGen-xPrev
	yDiff = yGen-yPrev

	#a for loop would be better/more scalable here but i just want to see if it works

	if (abs(xDiff) < checkRange):
		if xGen >  (100. - changeAmount): #this would result in a greator than 100 command
			xScreened = xGen - random.uniform(2,3)
		else:
			xScreened = xGen + random.uniform(2,3)
	else:
		xScreened = xGen

	if (abs(yDiff) < checkRange):
		if yGen >  (100. - changeAmount): #this would result in a greator than 100 command
			yScreened = yGen - random.uniform(2,3)
		else:
			yScreened = yGen + random.uniform(2,3)
	else:
		yScreened = yGen

	# if xGen == 0.0: #this is to prevent getting stuck
	# 	xScreened = random.uniform(0.5,3)
	# if yGen == 0.0:
	# 	yScreened = random.uniform(0.5,3)

	# print ('\tScreening command data -- xCmd: ' +str(xScreened) + '\t yCmd: ' + str(yScreened))



	return [xScreened, yScreened]


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
	


class soft_learner():
	def __init__(self):
		#init position variables
		self.testS = "" #test string for testing data passing
		self.xCmd = 0
		self.yCmd = 0
		self.xCmdPrev = 0
		self.yCmdPrev = 0
		self.xPos = 0
		self.yPos = 0
		self.xPosPrev = 0
		self.yPosPrev = 0
		self.xZero = 0
		self.yZero = 0
		self.xState = 0
		self.yState = 0
		self.xStatePrev = 0
		self.yStatePrev = 0
		self.xZero = 0 
		self.yZero = 0


		self.log_file = None

		self.state = np.array([0,0])
		self.statePrev = np.array([0,0])

		self.FirstCommand = True

		self.TotalStepCount = 0
		self.TotalEpisodeCount = 0
		#init steps and dt (time per step)
		self.n_steps = 0
		self.dt = TIME_PER_STEP #1=1second - play with this variable
		#initialize proper spaces and metadata 
		#both the action and state space are bounded by 0-100 for %of actuation
		#mapping these to real world actiona dnnand sensors are handeled in another script
		self.observation_space = spaces.Box(low=np.array([0.,0.]), high=np.array([100.,100.])) #obs space = continuous, 
		self.action_space = spaces.Box(low=np.array([0.,0.]), high=np.array([100.,100.]))
		# self.action_space = spaces.Box(low=np.array([xActMin,yActMin]), high=np.array([xActMax,yActMax]))
		# print("Calibrating action space from ROS parameters...")
		# print("\txMin: "+xActMin+"\txMax: "+xActMax)
		# print("\tyMin: "+yActMin+"\tyMax: "+yActMax)
		#since each action is broken out here i am going to say the action space is only one


		self.metadata = 0

		#send initial commands to grbl (home, set 0 all that)

	def reset(self):
		global xZero, yZero, xPos_global, yPos_global
		self.x = 0
		self.y = 0
		self.n_steps = 0
		self.reward = 0

		self.xCmd = 0
		self.yCmd = 0
		self.xCmdPrev = 0
		self.yCmdPrev = 0
		self.xPos = 0
		self.yPos = 0
		self.xPosPrev = 0
		self.yPosPrev = 0
		self.xZero = 0
		self.yZero = 0
		self.xState = 0
		self.yState = 0
		self.xStatePrev = 0
		self.yStatePrev = 0

		self.FirstCommand = True

		
		#reset grbl controller
		resetGrblController()
		print('==== BEGINNING EPISODE ' + str(self.TotalEpisodeCount) + ' ====')

		#re calibrate and set x and y zero values for each new run for april tags data
		self.xZero = xPos_global
		self.yZero = yPos_global

		#run calibration function here
		return self.x, self.y

	def step(self, generated_cmd_array):
		global xPos_global, yPos_global, xState_global, yState_global
		f = open(os.path.join(dirName, "learn.txt"), "a")
		self.log_file = f


		xPos_startstep = xPos_global #try to take a 0 so every stpe knows where it starts and us it to find reward
		yPos_startstep = yPos_global
		
		
		print('---------------------| Total Steps: ' + str(self.TotalStepCount) + ' | Episode: ' + str(self.TotalEpisodeCount) + ' | Episode Step: '  + str(self.n_steps) + ' |-----------------------')
		self.log_file.write('---------------------| Total Steps: ' + str(self.TotalStepCount) + ' | Episode: ' + str(self.TotalEpisodeCount) + ' | Episode Step: '  + str(self.n_steps) + ' |-----------------------\n')
		# print(generated_cmd_array)
		# xCommand = generated_cmd_array[0]
		# yCommand = generated_cmd_array[1]
		# xCommand = np.clip(xCommand, self.action_space.low, self.action_space.high)
		# yCommand = np.clip(yCommand, self.action_space.low, self.action_space.high)
		generated_cmd_array = np.clip(generated_cmd_array, self.action_space.low, self.action_space.high)

		#generate an action
		# xCommand = random.randint(0,100)
		# yCommand = random.randint(0,100)
		#print("command generated x {} y {}", format(generated_cmd_array[0]), format(generated_cmd_array[1]))
		
		#v = np.clip(v, self.action_space.low, self.action_space.high)
		#above line in example not sure why it is used

		#publish action
		cmd_message = gcode_packager()
		# cmd_message.x_percentage = xCommand
		# cmd_message.y_percentage = yCommand
		
		#preprocess generated commands to make sure they are sufficiently far enough away from last command to not freeze system and within 0-100
		screened_cmd_array = screenCmdData(generated_cmd_array, self.xCmdPrev, self.yCmdPrev)
		self.xCmd = screened_cmd_array[0]
		self.yCmd = screened_cmd_array[1]
		# print('\tCommand Generated: \t\txCmd:\t' +  str(self.xCmd) + '\tyCmd:\t' + str(self.yCmd))
		print("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f" %(self.xCmd, self.yCmd))
		self.log_file.write("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f\n" %(self.xCmd, self.yCmd))
		cmd_message.x_percentage = screened_cmd_array[0]
		cmd_message.y_percentage = screened_cmd_array[1]
		cmd_pub.publish(cmd_message)

		#wait for hardware to complete action
		wait_for_action()

		#subscribe/read state
		# state = {'x': xState, 'y': yState}
		self.state = [xState_global, yState_global]
		self.xState = self.state[0]
		self.yState = self.state[1]
		# print('\tState information: \t\txState:' + str(self.xState) + '\t\t\t\tyState: ' + str(self.yState))
		# print('\tState information: \t\txStatePrev:' + str(self.xStatePrev) + '\t\t\t\tyStatePrev: ' + str(self.yStatePrev))
		print("\tState Information\t| \t  xState: %6.3f \t  yState: %6.3f" %(self.xState, self.yState))
		print("\t                 \t| \t  xSPrev: %6.3f \t  ySPrev: %6.3f" %(self.xStatePrev, self.yStatePrev))
		self.log_file.write("\tState Information\t| \t  xState: %6.3f \t  yState: %6.3f\n" %(self.xState, self.yState))
		self.log_file.write("\t                 \t| \t  xSPrev: %6.3f \t  ySPrev: %6.3f\n" %(self.xStatePrev, self.yStatePrev))
		#compute reward
		#use beginning of episode as zero
		# self.reward, self.xPos, self.yPos = rewardCalculation(xPos_global, yPos_global, self.xZero, self.yZero, self.xPosPrev, self.yPosPrev)
		#use each steps starting position to find reward
		self.reward = rewardCalculation(xPos_global, yPos_global, xPos_startstep, yPos_startstep)
		#print("x position: {}", format(xPosition))
		#print("y position: {}", format(yPosition))
		# print("x calibrated: {}", format(x_calibrated))
		# print("y calibrated: {}", format(y_calibrated))
		# print("reward: {}", format(self.reward))
		# print('--Position and Reward Data--')
		# print('\tPosition information: \t\txPos: '+ str(self.xPos) + '\tyPos: ' + str(self.yPos))
		# print('\tPrevious Position: \t\txPosPrev: '+ str(self.xPosPrev) + '\t\t\t\tyPosPrev: ' + str(self.yPosPrev))
		# print('\tReward Information: \t\tReward: ' + str(self.reward))

		self.xPos = xPos_global
		self.yPos = yPos_global

		print("\tPosition Information\t| \t    xPos: %6.3f \t    yPos: %6.3f" %(self.xPos, self.yPos))
		print("\t                    \t| \txPosstrt: %6.3f \tyPosstrt: %6.3f" %(xPos_startstep, yPos_startstep))
		print("\t                    \t| \t   xZero: %6.3f \t   yZero: %6.3f" %(self.xZero, self.yZero))
		print("\tReward Information  \t| \t  Reward: %6.3f" %(self.reward))
		self.log_file.write("\tPosition Information\t| \t    xPos: %6.3f \t    yPos: %6.3f\n" %(self.xPos, self.yPos))
		self.log_file.write("\t                    \t| \txPosstrt: %6.3f \tyPosstrt: %6.3f\n" %(xPos_startstep, yPos_startstep))
		self.log_file.write("\t                    \t| \t   xZero: %6.3f \t   yZero: %6.3f\n" %(self.xZero, self.yZero))
		self.log_file.write("\tReward Information  \t| \t  Reward: %6.3f\n" %(self.reward))

		#assign all current data to previous data containers for next state
		self.xStatePrev = self.xState
		self.yStatePrev = self.yState
		self.xCmdPrev = self.xCmd
		self.yCmdPrev = self.yCmd
		self.xPosPrev = self.xPos
		self.yPosPrev = self.yPos

		#increment and finish step
		self.TotalStepCount = self.TotalStepCount + 1
		# step_count = step_count +1
		# print ("step count: {}", format(step_count))
		
		self.n_steps += 1
		if self.n_steps > NUM_STEPS_EPISODE:
			self.TotalEpisodeCount = self.TotalEpisodeCount + 1
			print('====END OF EPISODE====')
			self.log_file.write('====END OF EPISODE====\n')
		done = self.n_steps > NUM_STEPS_EPISODE

		self.log_file.close()

		return self.state, self.reward, done, {}


if __name__ == '__main__':
	
	#run suscriber nodes
	RL_subscribers()
	print("Starting...")

	time.sleep(3) #give ros time to set up

	#init environmnet
	env = soft_learner()
	
	print('done')

	

	a_dim = env.action_space.shape[0]
	ddpg_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(a_dim), sigma=NOISE_CONSTANT*np.ones(a_dim)) 
	ddpg_env = DummyVecEnv([lambda: env])
	ddpg_model = DDPG(DDPGMlpPolicy, ddpg_env,  action_noise=ddpg_noise,
					verbose=VERBOSE,
					tensorboard_log='tensorboard')

	
	env.reset()
	ddpg_model.learn(total_timesteps=TOTAL_STEPS)
	ddpg_model.save("ddpg_model")
	print('Complete training ddpg')
	# file.close()
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


