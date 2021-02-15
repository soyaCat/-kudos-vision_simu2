from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import ActionTuple
import numpy as np
import datetime
import time
import math
from collections import deque
import os

import cv2
import random
import CustomFuncionFor_mlAgent as CF

game = "-kudos-vision_simulator.exe"
env_path = "./Build/"+game
env = UnityEnvironment(file_name = env_path)
env.reset()
behavior_names = list(env.behavior_specs)
ConversionDataType = CF.ConversionDataType()
totalEpisodeCount = 10

if __name__ == "__main__":
    for episodeCount in range(totalEpisodeCount):
        behavior_name = behavior_names[0]
        decision_steps, terminal_steps = env.get_steps(behavior_name)
        behavior_name_Num = ConversionDataType.ConvertBehaviorname2Num(behavior_name)
        vec_observation, vis_observation_list, done = AgentsHelper.getObservation(behavior_name)
        vis_observation = vis_observation_list[0]
        print(type(vis_observation_list))
        print(vis_observation_list.shape())