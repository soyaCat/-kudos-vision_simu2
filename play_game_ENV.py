import sys
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
    pass
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import ActionTuple
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
import numpy as np
import datetime
import time
import math
from collections import deque
import os
import zmq
import zmqnumpy as znp

import cv2
import random
import CustomFuncionFor_mlAgent as CF
from PIL import Image
from tqdm import tqdm

#game = "-kudos-vision_simulator.exe"
#env_path = "./Build/"+game
game = "kudos_vision_simulator.x86_64"
env_path = "./Linux_build/"+game
save_picture_path = "./made_data/"
channel = EngineConfigurationChannel()
channel.set_configuration_parameters(time_scale = 1.0, target_frame_rate = 60, capture_frame_rate = 60)
env = UnityEnvironment(file_name = env_path, side_channels = [channel])
env.reset()
behavior_names = list(env.behavior_specs)

ConversionDataType = CF.ConversionDataType()
totalEpisodeCount = 100
AgentsHelper = CF.AgentsHelper(env, string_log = None, ConversionDataType = ConversionDataType)
write_file_name_list_index_instead_of_correct_name = False
list_index_for_ALL = 0
list_index_for_ball = 1
list_index_for_flag = 2
list_index_for_stage = 7
list_index_for_goal1_detection = 3
list_index_for_goal2_detection = 5
list_index_for_goal1_range = 4
list_index_for_goal2_range = 6

generate_ALL = False
generate_ball_map = False
generate_stage = False
generate_flag = False
generate_ball = False
generate_goal_dectecion = False
generate_goal_range = False
generate_yolo_txt_file = False

write_txt_file_ball_pos = False
write_txt_file_goal_pos = False

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
    ball_map_npArr = np.zeros((im_width_size, im_hight_size))
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
                ball_map_npArr[width][hight] = 255
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

    return left, bottom, right, top, ball_map_npArr

def get_rectangle_point_for_yolo_no_map(ball_npArr):
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

    return left, bottom, right, top #round(n,2)

def get_txt_line_for_yolo_txt(episodeCount, left, bottom, right, top, ID):
    height_distance = bottom-top
    width_distance = left-right
    height_center = bottom-(height_distance/2)
    width_center = left-(width_distance/2)
    data = str(ID)+" "+str(round(height_center,6))+" "+str(round(width_center,6))+" "+str(round(height_distance, 6))+" "+str(round(width_distance, 6)) + "\n"
    
    return data

def write_txt_file_like_yolo_mark(episodeCount, ball_list, goal1_list, goal2_list, no_ball, no_goal1, no_goal2):
    f = open("./made_data/"+str(episodeCount)+"_ALL.txt", 'w')
    if no_ball == False:
        left = ball_list[0]
        bottom = ball_list[1]
        right = ball_list[2]
        top = ball_list[3]
        data = get_txt_line_for_yolo_txt(episodeCount, left, bottom, right, top, 0)
        f.write(data)
    if no_goal1 == False:
        left = goal1_list[0]
        bottom = goal1_list[1]
        right = goal1_list[2]
        top = goal1_list[3]
        data = get_txt_line_for_yolo_txt(episodeCount, left, bottom, right, top, 1)
        f.write(data)
    if no_goal2 == False:
        left = goal2_list[0]
        bottom = goal2_list[1]
        right = goal2_list[2]
        top = goal2_list[3]
        data = get_txt_line_for_yolo_txt(episodeCount, left, bottom, right, top, 1)
        f.write(data)

    f.close()

def write_train_txt_file_for_yolo(totalEpisodeCount):
    f = open("./made_data/"+"train.txt", 'w')
    for i in range(totalEpisodeCount):
        data = "data/kudos_obj/"+str(i)+"_ALL.jpg"+"\n"
        f.write(data)

    f.close()

def save_numpy_file(append_name, list_index, wfnliiocn):
    im = Image.fromarray(vis_observation_list[list_index].astype('uint8'), 'RGB')
    if wfnliiocn == False:
        im.save(save_picture_path+str(episodeCount)+append_name+'.jpg')
    else:
        im.save(save_picture_path+str(list_index)+'.jpg')

def change_numpy_rgb_to_bgr(npArr):
    bgr_npArr = np.zeros_like(npArr)
    bgr_npArr[:,:,0:1] = npArr[:,:,2:]
    bgr_npArr[:,:,1:2] = npArr[:,:,1:2]
    bgr_npArr[:,:,2:] = npArr[:,:,0:1]

    return bgr_npArr

if __name__ == "__main__":
    write_train_txt_file_for_yolo(totalEpisodeCount)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:9010")
    print("wait receive message from client...")
    message = socket.recv()
    print("message: ", message)

    for episodeCount in tqdm(range(totalEpisodeCount)):
        behavior_name = behavior_names[0]
        decision_steps, terminal_steps = env.get_steps(behavior_name)
        vec_observation, vis_observation_list, done = AgentsHelper.getObservation(behavior_name)
        vis_observation = vis_observation_list[0]
        wfnliiocn = write_file_name_list_index_instead_of_correct_name

        if generate_ALL == True:
            save_numpy_file('_ALL', list_index_for_ALL, wfnliiocn)
        if generate_stage == True:
            save_numpy_file('_stage', list_index_for_stage, wfnliiocn)
        if generate_ball == True:
            save_numpy_file('_ball', list_index_for_ball, wfnliiocn)
        if generate_flag == True:
            save_numpy_file('_flag', list_index_for_flag, wfnliiocn)
        if generate_goal_dectecion == True:
            save_numpy_file('_goal1_detection', list_index_for_goal1_detection, wfnliiocn)
            save_numpy_file('_goal2_detection', list_index_for_goal2_detection, wfnliiocn)
        if generate_goal_range == True:
            save_numpy_file('_goal1_range', list_index_for_goal1_range, wfnliiocn)
            save_numpy_file('_goal2_range', list_index_for_goal2_range, wfnliiocn)

        ALL_npArr = vis_observation_list[list_index_for_ALL]
        ALL_npArr = change_numpy_rgb_to_bgr(ALL_npArr)
        znp.send_array(socket, ALL_npArr)

        received_position_npArr = znp.recv_array(socket)
        print("receive msg from client:", received_position_npArr)

        
        action = [2,0,0,0]
        actionTuple = ConversionDataType.ConvertList2DiscreteAction(action,behavior_name)
        env.set_actions(behavior_name, actionTuple)

        env.step()
    env.close()

