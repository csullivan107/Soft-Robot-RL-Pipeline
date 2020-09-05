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
from stable_baselines.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise, AdaptiveParamNoiseSpec
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.callbacks import CallbackList, CheckpointCallback, EvalCallback, EveryNTimesteps, BaseCallback
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
action_done_flag = False

#define constants
NUM_STEPS_EPISODE = 24 #index at 0 - (desirednum - 1)
TOTAL_STEPS = 3000
TIME_PER_STEP = 1 #this could be variable depending on hardware
robotName = "robot_1"
NOISE_CONSTANT = .03 #how do i update this inside the TD3.learn function
#just going to put this at a rate large enough taht we liikkely wont get hardware hangups

#here are the constants for the TD3 Model
GAMMA = 0.99
LEARNING_RATE = .003
BUFFER_SIZE = 50000
LEARNING_STARTS = 500
GRADIENT_STEPS = 1
BATCH_SIZE = 32
TRAIN_FREQ = 1
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
	xPos_global = data.x_pos_gnd*1000
	yPos_global = data.y_pos_gnd*1000
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

	reward = yDist

	return reward

def wait_for_action(is_homing):
	global action_done
	count = 0
	timeout = 10 #seconds
	if is_homing:
		timeout = 20
	start = time.time()
	while not action_done:
		count = count + 1
		# Sometimes if the commands are too close the system completes the action so fast the system doesnt get
		# a chance to register it. no action should take more than 10 seconds so if greater than that assume the 
		# action is done
		if ((time.time()-start) > timeout): #this is 10 seconds
			action_done = True
		
		
		
	print("\t--Action Complete--\t|")
	time.sleep(1) #this ensures things tont compute too quickly and action done works for the rest of the episode meaning only one action complete

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
	wait_for_action(True)
	time.sleep(.5)
	direct_cmd_publisher.publish('G92 X0 Y0')
	print("Homing Complete - moving to robot 0 state")
	# cmd_message = gcode_packager()
	#publish action
	# cmd_message.x_percentage = 0.
	# cmd_message.y_percentage = 0.
	# # time.sleep(1)
	# cmd_pub.publish(cmd_message)
	# wait_for_action(False)

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
		# self.observation_space = spaces.Box(low=np.array([0.,0.]), high=np.array([100.,100.])) #obs space = continuous, 
		
		#remapping observations -1 to 1 so debug "convergence problem"
		self.observation_space = spaces.Box(low=np.array([-1.,-1.]), high=np.array([1.,1.])) #obs space = continuous, 

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

		xReturn = self.x/50-1
		yReturn = self.y/50-1

		#run calibration function here
		return xReturn, yReturn

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
		# screened_cmd_array = screenCmdData(generated_cmd_array, self.xCmdPrev, self.yCmdPrev)
		# self.xCmd = screened_cmd_array[0]
		# self.yCmd = screened_cmd_array[1]

		self.xCmd = generated_cmd_array[0]
		self.yCmd = generated_cmd_array[1]
		print("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f" %(self.xCmd, self.yCmd))
		self.log_file.write("\tCommand Generated\t| \t    xCmd: %6.3f \t    yCmd: %6.3f\n" %(self.xCmd, self.yCmd))
		#publish action
		cmd_message.x_percentage = self.xCmd
		cmd_message.y_percentage = self.yCmd
		# time.sleep(1)
		cmd_pub.publish(cmd_message)
		print("\t--Command Sent   --\t|")
		
		

		#wait for hardware to complete action
		wait_for_action(False)
		# print("\t--Action Complete--\t|")
		# print("\t--Done waiting   --\t|")
		
		#subscribe/read state
		self.state = [xState_global, yState_global]
		# print("\t--state data got --\t|")
		self.xState = self.state[0]
		# print("\t--state 0 set    --\t|")
		self.yState = self.state[1]
		# print("\t--state 1 set    --\t|")
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
		
		left_data = open(os.path.join(dirName,"left_data.txt"), "a")
		left_data.write(str(self.xCmd) + '\n')
		left_data.close()
		right_data = open(os.path.join(dirName,"right_data.txt"),"a")
		right_data.write(str(self.yCmd) + '\n')
		right_data.close()

		#remap states from -1 to 1 - this was after much debugging
		self.state[0] = (self.state[0]/50)-1
		self.state[1] = (self.state[1]/50)-1
		return self.state, self.reward, done, {}


class customCallback(BaseCallback):
	"""
	A custom callback that derives from ``BaseCallback``.

	:param verbose: (int) Verbosity level 0: not output 1: info 2: debug
	"""

	def __init__(self, verbose=0):
		super(customCallback, self).__init__(verbose)
		# Those variables will be accessible in the callback
		# (they are defined in the base class)
		# The RL model
		# self.model = None  # type: BaseRLModel
		# An alias for self.model.get_env(), the environment used for training
		# self.training_env = None  # type: Union[gym.Env, VecEnv, None]
		# Number of time the callback was called
		# self.n_calls = 0  # type: int
		# self.num_timesteps = 0  # type: int
		# local and global variables
		# self.locals = None  # type: Dict[str, Any]
		# self.globals = None  # type: Dict[str, Any]
		# The logger object, used to report things in the terminal
		# self.logger = None  # type: logger.Logger
		# # Sometimes, for event callback, it is useful
		# # to have access to the parent object
		# self.parent = None  # type: Optional[BaseCallback]
		self.startTime = None
		self.endTime = None

	def _on_training_start(self) -> None:
		"""
		This method is called before the first rollout starts.
		"""
		self.startTime = time.time()
		print("Begin training")
		pass

	def _on_rollout_start(self) -> None:
		"""
		A rollout is the collection of environment interaction
		using the current policy.
		This event is triggered before collecting new samples.

		"""

		print("\t--Rollout Strt   --\t|")
		pass

	def _on_step(self) -> bool:
		"""
		This method will be called by the model after each call to `env.step()`.

		For child callback (of an `EventCallback`), this will be called
		when the event is triggered.

		:return: (bool) If the callback returns False, training is aborted early.
		"""
		if self.num_timesteps % 100:
			t = time.time()
			time_elapsed = t-self.startTime #seconds
		print("\t--Step Done      --\t|")
		if yPos_global > 200:
			input("Please reset the robot to start and press enter key to continue..")

		return True

	def _on_rollout_end(self) -> None:
		"""
		This event is triggered before updating the policy.
		"""
		print("\t--Updte Ploicy   --\t|")

		pass

	def _on_training_end(self) -> None:
		"""
		This event is triggered before exiting the `learn()` method.
		"""
		self.endTime = time.time()
		time_elapsed = (self.endTime - self.startTime)/60 #minutes
		avg = self.num_timesteps/time_elapsed
		print("\t--Train Complt   --\t|")
		print("\t elapsed time: " + str(time_elapsed) + " min\tavg tiem/step: " + str(avg) + " sec")
		pass

# Use deterministic actions for evaluation



if __name__ == '__main__':
	
	#run suscriber nodes
	RL_subscribers()
	print("Starting...")

	time.sleep(3) #give ros time to set up

	#init environmnet
	env = soft_learner()
	
	print('done')

	

	a_dim = env.action_space.shape[0]
	# td3_noise = OrnsteinUhlenbeckActionNoise(np.zeros(a_dim), .9*np.ones(a_dim)) 
	td3_noise = NormalActionNoise(0,.75)
	td3_env = DummyVecEnv([lambda: env])
	# td3_env = env

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

	#every x episodes fun the model for y amount of episodes and evaluate it
	eval_callback = EvalCallback(td3_env, best_model_save_path='./logs/',
                             log_path='./logs/', eval_freq=100,
                             deterministic=True, render=False)

	checkpoint_callback = CheckpointCallback(save_freq=100, save_path= dirName,
                                         name_prefix='rl_model')

	# td3_model.learning_starts = 100
	
	custom_callback = customCallback(verbose=0)
	callback = CallbackList([custom_callback, checkpoint_callback])
	td3_model.learn(total_timesteps = TOTAL_STEPS, callback=callback)
	td3_model.save("td3_model_int_test")

	# for i in range(10):
	# 	td3_model.learn(total_timesteps = 10, _init_setup_model = False)
		
	# 	td3_model.learning_starts = 0
	# 	if yPos_global > 200:
	# 		input("Please reset the robot to start and press enter key to continue..")
	

	#only 100 steps showed up in the final taensorboard. i think it has to do with the for loop. doing a thouand steps

	# for i in range(10):
		
		
	# 	print('++++++++++++++ Saving TD3 model | 100 Steps Completed ++++++++++++++++')
	# 	if i == 5:
	# 		print ("add order of magnitude to learning rate and redurce noise constant")
	# 		new_rate = LEARNING_RATE/10
	# 		td3_model.learning_rate = new_rate
	# 		# td3_model.noise = NormalActionNoise(0,.6)
	# 		td3_model.action_noise = OrnsteinUhlenbeckActionNoise(np.zeros(a_dim), .6*np.ones(a_dim)) 
	# 		# print ("turning off learning starts")
	# 		# td3_model.learning_starts = 0
	# 	if i == 8:
	# 		print ("add order of magnitude to learning rate and reduce noise constant")
	# 		new_rate = LEARNING_RATE/100
	# 		td3_model.learning_rate = new_rate
	# 		# td3_model.noise = NormalActionNoise(0,.3)
	# 		td3_model.action_noise = OrnsteinUhlenbeckActionNoise(np.zeros(a_dim), .3*np.ones(a_dim)) 

	print("learning complete")





