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
import pprint
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


pp = pprint.PrettyPrinter(indent = 4)

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
TOTAL_STEPS = 10000
TIME_PER_STEP = 1 #this could be variable depending on hardware
robotName = "robot_1"
NOISE_CONSTANT = .03 #how do i update this inside the TD3.learn function
#just going to put this at a rate large enough taht we liikkely wont get hardware hangups

#here are the constants for the TD3 Model
GAMMA = 0.9
LEARNING_RATE = .1
BUFFER_SIZE = 50000
LEARNING_STARTS = 50
TRAIN_FREQ = 100
GRADIENT_STEPS = 100
BATCH_SIZE = 64
TAU = .005
POLICY_DELAY = 16
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
baseDir = 'src/soft_robot_learning/src/learning_logs/' + robotName + '/learining_run_TD3_'

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
	# 
	# 
#Define various functions used throughout script	

def rewardCalculation(x_current, y_current, x_startstep, y_startstep):
	xDist = x_current - x_startstep
	yDist = y_current - y_startstep

	reward = yDist*1000

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
			xScreened = xGen - random.uniform(2,5)
		else:
			xScreened = xGen + random.uniform(2,5)
	else:
		xScreened = xGen

	if (abs(yDiff) < checkRange):
		if yGen >  (100. - changeAmount): #this would result in a greator than 100 command
			yScreened = yGen - random.uniform(2,5)
		else:
			yScreened = yGen + random.uniform(2,5)
	else:
		yScreened = yGen

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

		generated_cmd_array = np.clip(generated_cmd_array, self.action_space.low, self.action_space.high)

		#declare message type
		cmd_message = gcode_packager()
		
		#preprocess generated commands to make sure they are sufficiently far enough away from last command to not freeze system and within 0-100
		screened_cmd_array = screenCmdData(generated_cmd_array, self.xCmdPrev, self.yCmdPrev)
		self.xCmd = screened_cmd_array[0]
		self.yCmd = screened_cmd_array[1]

		# self.xCmd = generated_cmd_array[0]
		# self.yCmd = generated_cmd_array[1]
		print("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f" %(self.xCmd, self.yCmd))
		self.log_file.write("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f\n" %(self.xCmd, self.yCmd))
		#publish action
		cmd_message.x_percentage = self.xCmd
		cmd_message.y_percentage = self.yCmd
		cmd_pub.publish(cmd_message)

		#wait for hardware to complete action
		wait_for_action()

		#subscribe/read state
		self.state = [xState_global, yState_global]
		self.xState = self.state[0]
		self.yState = self.state[1]
		print("\tState Information\t| \t  xState: %6.3f \t  yState: %6.3f" %(self.xState, self.yState))
		print("\t                 \t| \t  xSPrev: %6.3f \t  ySPrev: %6.3f" %(self.xStatePrev, self.yStatePrev))
		self.log_file.write("\tState Information\t| \t  xState: %6.3f \t  yState: %6.3f\n" %(self.xState, self.yState))
		self.log_file.write("\t                 \t| \t  xSPrev: %6.3f \t  ySPrev: %6.3f\n" %(self.xStatePrev, self.yStatePrev))
		#compute reward
		#use beginning of episode as zero
		# self.reward, self.xPos, self.yPos = rewardCalculation(xPos_global, yPos_global, self.xZero, self.yZero, self.xPosPrev, self.yPosPrev)
		#use each steps starting position to find reward
		self.reward = rewardCalculation(xPos_global, yPos_global, xPos_startstep, yPos_startstep)
		

		self.xPos = xPos_global
		self.yPos = yPos_global

		print("\tPosition Information\t| \t    xPos: %6.3f \t    yPos: %6.3f" %(self.xPos, self.yPos))
		print("\t                    \t| \txPosPrev: %6.3f \tyPosPrev: %6.3f" %(self.xPosPrev, self.yPosPrev))
		print("\t                    \t| \t   xZero: %6.3f \t   yZero: %6.3f" %(self.xZero, self.yZero))
		print("\tReward Information  \t| \t  Reward: %6.3f" %(self.reward))
		self.log_file.write("\tPosition Information\t| \t    xPos: %6.3f \t    yPos: %6.3f\n" %(self.xPos, self.yPos))
		self.log_file.write("\t                    \t| \txPosPrev: %6.3f \tyPosPrev: %6.3f\n" %(self.xPosPrev, self.yPosPrev))
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
	td3_noise = OrnsteinUhlenbeckActionNoise(np.zeros(a_dim), NOISE_CONSTANT*np.ones(a_dim)) 
	td3_env = DummyVecEnv([lambda: env])

	td3_model = TD3(Td3MlpPolicy, td3_env,
					gamma = GAMMA,
					learning_rate = LEARNING_RATE,
					buffer_size = BUFFER_SIZE,
					learning_starts = LEARNING_STARTS,
					train_freq = TRAIN_FREQ,
					gradient_steps = GRADIENT_STEPS,
					batch_size = BATCH_SIZE,
					tau = TAU,
					policy_delay = POLICY_DELAY,
					action_noise = td3_noise,
					target_policy_noise = TARGET_POLICY_NOISE,
					target_noise_clip = TARGET_NOISE_CLIP,
					random_exploration = RANDOM_EXPLORATION,
					verbose = VERBOSE,
					tensorboard_log = TENSORBOARD_LOG,
					_init_setup_model = _INIT_SETUP_MODEL,
					policy_kwargs = POLICY_KWARGS,
					full_tensorboard_log = FULL_TENSORBOARD_LOG,
					seed = SEED,
					n_cpu_tf_sess = N_CPU_TF_SESS)

	env.reset()

	pp.pprint(td3_model.get_parameter_list())

	for i in range(int(TOTAL_STEPS/10)):
		td3_model.learn(total_timesteps=int(TOTAL_STEPS/10))
		td3_model.save("td3_model")
		print('++++++++++++++ Saving TD3 model | '+ str((TOTAL_STEPS/10)) + ' Steps Completed ++++++++++++++++')
		if i == 5:
			print ("add order of magnitude to learning rate")
			new_rate = LEARNING_RATE/10
			td3_model.learning_rate = new_rate
			print ("turning off learning starts")
			td3_model.learning_starts = 0
		if i == 8:
			print ("add order of magnitude to learning rate")
			new_rate = LEARNING_RATE/100
			td3_model.learning_rate = new_rate

	print("learning complete")





