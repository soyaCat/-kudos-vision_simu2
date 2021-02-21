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
from tqdm import tqdm

game = "-kudos-vision_simulator.exe"
env_path = "./Build/"+game
save_picture_path = "./made_data/"
env = UnityEnvironment(file_name = env_path)
env.reset()
behavior_names = list(env.behavior_specs)
ConversionDataType = CF.ConversionDataType()
totalEpisodeCount = 1500
AgentsHelper = CF.AgentsHelper(env, string_log = None, ConversionDataType = ConversionDataType)
list_index_for_ALL = 0
list_index_for_ball = 1
list_index_for_flag = 2
list_index_for_stage = 5
list_index_for_goal1 = 4
list_index_for_goal2 = 3

generate_ball_map = False
generate_stage = False
generate_flag = False
generate_ball = False
generate_goal = False
generate_yolo_txt_file = True

write_txt_file_ball_pos = True
write_txt_file_goal_pos = True

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

if __name__ == "__main__":
    write_train_txt_file_for_yolo(totalEpisodeCount)
    for episodeCount in tqdm(range(totalEpisodeCount)):
        behavior_name = behavior_names[0]
        decision_steps, terminal_steps = env.get_steps(behavior_name)
        vec_observation, vis_observation_list, done = AgentsHelper.getObservation(behavior_name)
        vis_observation = vis_observation_list[0]

        im = Image.fromarray(vis_observation_list[list_index_for_ALL].astype('uint8'), 'RGB')
        im.save(save_picture_path+str(episodeCount)+'_ALL.jpg')
        if generate_stage == True:
            im_stage = Image.fromarray(vis_observation_list[list_index_for_stage].astype('uint8'), 'RGB')
            im_stage.save(save_picture_path+str(episodeCount)+'_stage.jpg')
        if generate_ball == True:
            im_ball = Image.fromarray(vis_observation_list[list_index_for_ball].astype('uint8'), 'RGB')
            im_ball.save(save_picture_path+str(episodeCount)+'_ball.jpg')
        if generate_flag == True:
            im_flag = Image.fromarray(vis_observation_list[list_index_for_flag].astype('uint8'), 'RGB')
            im_flag.save(save_picture_path+str(episodeCount)+'_flag.jpg')
        if generate_goal == True:
            im_goal1 = Image.fromarray(vis_observation_list[list_index_for_goal1].astype('uint8'), 'RGB')
            im_goal1.save(save_picture_path+str(episodeCount)+'_goal1.jpg')
            im_goal2 = Image.fromarray(vis_observation_list[list_index_for_goal2].astype('uint8'), 'RGB')
            im_goal2.save(save_picture_path+str(episodeCount)+'_goal2.jpg')

        ball_npArr = vis_observation_list[list_index_for_ball]
        goal1_npArr = vis_observation_list[list_index_for_goal1]
        goal2_npArr = vis_observation_list[list_index_for_goal2]
        left = 0.0
        bottom = 0.0
        right = 1.0
        top = 1.0
        g1_left = 0.0
        g1_bottom = 0.0
        g1_right = 1.0
        g1_top = 1.0
        g2_left = 0.0
        g2_bottom = 0.0
        g2_right = 1.0
        g2_top = 1.0

        if write_txt_file_ball_pos == True:
            left, bottom, right, top, ball_map_npArr = get_rectangle_point_for_yolo(ball_npArr)
            left, bottom, right, top = mapping_point_to_float_shape(ball_npArr, left, bottom, right, top)
            if generate_ball_map == True:
                im_ball_map = Image.fromarray(ball_map_npArr.astype('uint8'), 'L')
                im_ball_map.save(save_picture_path+str(episodeCount)+'_ball_map.jpg')

        if write_txt_file_goal_pos == True:
            g1_left, g1_bottom, g1_right, g1_top = get_rectangle_point_for_yolo_no_map(goal1_npArr)
            g1_left, g1_bottom, g1_right, g1_top = mapping_point_to_float_shape(goal1_npArr, g1_left, g1_bottom, g1_right, g1_top)
            g2_left, g2_bottom, g2_right, g2_top = get_rectangle_point_for_yolo_no_map(goal2_npArr)
            g2_left, g2_bottom, g2_right, g2_top = mapping_point_to_float_shape(goal2_npArr, g2_left, g2_bottom, g2_right, g2_top)


        ball_result = get_result_about_Is_same_1D_npArr(np.array([left, bottom, right, top]), np.array([0.0, 0.0, 1.0, 1.0]))
        goal1_result = get_result_about_Is_same_1D_npArr(np.array([g1_left, g1_bottom, g1_right, g1_top]), np.array([0.0, 0.0, 1.0, 1.0]))
        goal2_result = get_result_about_Is_same_1D_npArr(np.array([g2_left, g2_bottom, g2_right, g2_top]), np.array([0.0, 0.0, 1.0, 1.0]))


        if generate_yolo_txt_file == True:
            ball_pos = [left, bottom, right, top]
            goal1_pos = [g1_left, g1_bottom, g1_right, g1_top]
            goal2_pos = [g2_left, g2_bottom, g2_right, g2_top]
            write_txt_file_like_yolo_mark(episodeCount, ball_pos, goal1_pos, goal2_pos, ball_result, goal1_result, goal2_result)
        
        action = [1]
        actionTuple = ConversionDataType.ConvertList2DiscreteAction(action,behavior_name)
        env.set_actions(behavior_name, actionTuple)

        env.step()
    env.close()
