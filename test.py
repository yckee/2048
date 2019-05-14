import numpy as np
import gym
import gym_2048

env = gym.make('MountainCar-v0')
st = env.reset()

state_size = env.observation_space.shape[0]
action_size = env.action_space.n
