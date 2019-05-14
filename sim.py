import numpy as np
import gym
import gym_2048

env = gym.make('2048-v0')
env.render()


done = False
while not done:
    action = str(input())
    state, reward, done, _ = env.step(action)
    env.render()
