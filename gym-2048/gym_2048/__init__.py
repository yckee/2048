from gym.envs.registration import register
from .env_2048 import Env_2048
register(id='2048-v0', 
    entry_point='gym_2048.env_2048:Env_2048', 
)