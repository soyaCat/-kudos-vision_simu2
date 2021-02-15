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
totalEpisodeCount = 13
AgentsHelper = CF.AgentsHelper(env, string_log = None, ConversionDataType = ConversionDataType)
list_index_for_ALL = 0
list_index_for_ball = 1
list_index_for_flag = 2
list_index_for_stage = 3

def get_result_about_Is_same_1D_npArr(myArr1, myArr2):
    result = True
    for index in range(np.shape(myArr1)[0]):
        if myArr1[index] != myArr2[index]:
            result = False
    return result

def get_rectangle_point_for_yolo(ball_npArr):
    '''
    print(ball_npArr) #완전히 black인 부분은 [0,0,0]으로 표시된다.
    print(np.shape(ball_npArr)) #416,416,3, 직관적으로 이미지의 박스는 left, bottom, right, top으로 표시되어야 함(크다,크다,작다,작다)
    '''
    im_width_size = np.shape(ball_npArr)[0]
    im_hight_size = np.shape(ball_npArr)[1]
    candidate_width_list = []
    candidate_hight_list = []

    for width in range(im_width_size):
        Is_width_list_append = False
        for hight in range(im_hight_size):
            result = get_result_about_Is_same_1D_npArr(ball_npArr[width][hight], np.array([0, 0, 0]))
            if result == False:
                candidate_hight_list.append(hight)
                if Is_width_list_append == False:
                    candidate_width_list.append(width)
                    Is_width_list_append = True
    left = 0 #큰수여야함
    bottom = 0#큰수여야함
    right = im_width_size#작은수여야함
    top = im_hight_size#작은수여야 함

    for candidate_width in candidate_width_list:
        if right>candidate_width:
            right = candidate_width
        if left<candidate_width:
            left = candidate_width

    for candidate_hight in candidate_hight_list:
        if top>candidate_hight:
            top = candidate_hight
        if bottom<candidate_hight:
            bottom = candidate_hight

    return left, bottom, right, top

def mapping_point_to_float_shape(npArr, left, bottom, right, top):
    im_width_size = np.shape(npArr)[0]
    im_hight_size = np.shape(npArr)[1]
    left = left/im_width_size
    bottom = bottom/im_hight_size
    right = right/im_width_size
    top = top/im_hight_size

    return round(left,6), round(bottom,6), round(right,6), round(top,6) #round(n,2)

def write_txt_file_like_yolo_mark(episodeCount, left, bottom, right, top, write_data):
    f = open("./made_data/"+str(episodeCount)+"_ALL.txt", 'w')
    if write_data == True:
        data = str(0)+" "+str(left)+" "+str(bottom)+" "+str(right)+" "+str(top)
        f.write(data)

    f.close()

if __name__ == "__main__":
    for episodeCount in range(totalEpisodeCount):
        behavior_name = behavior_names[0]
        decision_steps, terminal_steps = env.get_steps(behavior_name)
        vec_observation, vis_observation_list, done = AgentsHelper.getObservation(behavior_name)
        vis_observation = vis_observation_list[0]

        im = Image.fromarray(vis_observation_list[list_index_for_ALL].astype('uint8'), 'RGB')
        im.save(save_picture_path+str(episodeCount)+'_ALL.jpg')
        im_stage = Image.fromarray(vis_observation_list[list_index_for_stage].astype('uint8'), 'RGB')
        im_stage.save(save_picture_path+str(episodeCount)+'_stage.jpg')
        im_ball = Image.fromarray(vis_observation_list[list_index_for_ball].astype('uint8'), 'RGB')
        im_ball.save(save_picture_path+str(episodeCount)+'_ball.jpg')
        im_flag = Image.fromarray(vis_observation_list[list_index_for_flag].astype('uint8'), 'RGB')
        im_flag.save(save_picture_path+str(episodeCount)+'_flag.jpg')

        ball_npArr = vis_observation_list[list_index_for_ball]
        left, bottom, right, top = get_rectangle_point_for_yolo(ball_npArr)
        print(left, bottom, right, top)
        left, bottom, right, top = mapping_point_to_float_shape(ball_npArr, left, bottom, right, top)
        print(left, bottom, right, top)
        result = get_result_about_Is_same_1D_npArr(np.array([left, bottom, right, top]), np.array([0.0, 0.0, 1.0, 1.0]))
        if result == False:
            write_txt_file_like_yolo_mark(episodeCount, left, bottom, right, top, True)
        if result == True:
            write_txt_file_like_yolo_mark(episodeCount, left, bottom, right, top, False)

        
        action = [1]
        actionTuple = ConversionDataType.ConvertList2DiscreteAction(action,behavior_name)
        env.set_actions(behavior_name, actionTuple)

        env.step()

