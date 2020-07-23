#!/usr/bin/env python3

from gym import spaces
import numpy as np
from stable_baselines.td3.policies import MlpPolicy as Td3MlpPolicy
from stable_baselines import TD3
from stable_baselines.ddpg.noise import OrnsteinUhlenbeckActionNoise
from stable_baselines.common.vec_env import DummyVecEnv

class find_five():
    
    def __init__(self):
        self.x = 0.
        self.dt = 0.01
        self.n_steps = 0
        self.observation_space = spaces.Box(low=np.array([-np.inf]), high=np.array([np.inf]))
        self.action_space = spaces.Box(low=np.array([-5.]), high=np.array([5.]))
        self.metadata = 0
    
    def reset(self):
        # print('got reset')
        self.x = 0.
        self.n_steps = 0
        return self.x
        
    def step(self):
        v = np.clip(v, self.action_space.low, self.action_space.high)
        # print('v = {}'.format(v))
        # print('x before = {}'.format(self.x))
        self.x += self.dt*v
        # print('x after = {}'.format(self.x))
        # print('x = {}'.format(self.x))
        r = -abs(self.x - 5)
        self.n_steps += 1
        done = self.n_steps > 1000
        # print('done? {}'.format(done))
        return self.x, r, done, {}
    
def train_td3(env):
    a_dim = env.action_space.shape[0]
    td3_noise = OrnsteinUhlenbeckActionNoise(np.zeros(a_dim), 0.3*np.ones(a_dim))
    td3_env = DummyVecEnv([lambda: env])
    td3_model = TD3(Td3MlpPolicy, td3_env, verbose=1, action_noise=td3_noise, tensorboard_log='tensorboard')
    td3_model.learn(total_timesteps=1000)
    td3_model.save("td3_model")
    print('Completed training TD3')
    
if __name__ == "__main__":
    env = find_five()
    env.reset()
    x, r, done, _ = env.step(4.95)
    print('x = {}'.format(x))
    print('r = {}'.format(r))
    a_dim = env.action_space.shape[0]
    td3_noise = OrnsteinUhlenbeckActionNoise(np.zeros(a_dim), 0.003*np.ones(a_dim))
    td3_env = DummyVecEnv([lambda: env])
    td3_model = TD3(Td3MlpPolicy, td3_env, verbose=1, action_noise=td3_noise, tensorboard_log='tensorboard')
    td3_model.learn(total_timesteps=100000)
    td3_model.save("td3_model")
    print('Completed training TD3')
    x = td3_env.reset()
    for i in range(100):
        v = td3_model.predict(x)
        x, r, _, _ = td3_env.step(v)
        print(v)
        print(x)
        print(r)
        
    
    
