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
from PIL import Image

game = "-kudos-vision_simulator.exe"
env_path = "./Build/"+game
save_picture_path = "./made_data/"
env = UnityEnvironment(file_name = env_path)
env.reset()
behavior_names = list(env.behavior_specs)
ConversionDataType = CF.ConversionDataType()
totalEpisodeCount = 11
AgentsHelper = CF.AgentsHelper(env, string_log = None, ConversionDataType = ConversionDataType)

if __name__ == "__main__":
    for episodeCount in range(totalEpisodeCount):
        behavior_name = behavior_names[0]
        decision_steps, terminal_steps = env.get_steps(behavior_name)
        vec_observation, vis_observation_list, done = AgentsHelper.getObservation(behavior_name)
        vis_observation = vis_observation_list[0]
        print(type(vis_observation_list))
        print(np.shape(vis_observation_list))

        im = Image.fromarray(vis_observation_list[0].astype('uint8'), 'RGB')
        im.save(save_picture_path+str(episodeCount)+'_ALL.jpg')
        im_stage = Image.fromarray(vis_observation_list[3].astype('uint8'), 'RGB')
        im_stage.save(save_picture_path+str(episodeCount)+'_stage.jpg')
        im_ball = Image.fromarray(vis_observation_list[1].astype('uint8'), 'RGB')
        im_ball.save(save_picture_path+str(episodeCount)+'_ball.jpg')
        im_flag = Image.fromarray(vis_observation_list[2].astype('uint8'), 'RGB')
        im_flag.save(save_picture_path+str(episodeCount)+'_flag.jpg')


        action = [1]
        actionTuple = ConversionDataType.ConvertList2DiscreteAction(action,behavior_name)
        env.set_actions(behavior_name, actionTuple)

        env.step()

