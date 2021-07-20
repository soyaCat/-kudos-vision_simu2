## 영상으로부터 프레임을 잘라서 저장해주는 함수
## starting_number와 사이즈를 지정하고 시작하자
## yolo 파일 리스트를 리턴해 줌

import cv2
vidcap = cv2.VideoCapture('./real_data/no_ball.mp4')
starting_number = 1300
def write_train_txt_file_for_yolo(totalEpisodeCount):
    f = open("./real_data/"+"train.txt", 'w')
    for i in range(totalEpisodeCount):
        data = "data/kudos_obj/"+str(i)+"_ALL.jpg"+"\n"
        f.write(data)
while(vidcap.isOpened()):
    ret, image = vidcap.read()
    try:
        image = cv2.resize(image, (416, 416))
        if(int(vidcap.get(1)) % 20 == 0):
            print('Saved frame number : ' + str(int(vidcap.get(1))))
            cv2.imwrite("./real_data/%d_ALL.jpg" % starting_number, image)
            f = open("./real_data/" + str(starting_number) + "_ALL.txt", 'w')
            f.close()
            starting_number += 1
    except Exception as e:
        break
write_train_txt_file_for_yolo(starting_number)
vidcap.release()