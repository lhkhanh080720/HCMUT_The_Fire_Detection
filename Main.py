import os
import time
import argparse # Library support Command Line Interface (CLI)
import numpy as np
import serial

import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver

from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO

#print(cv2.__version__)

# =========Take the video and process:=========
# cam = cv2.VideoCapture('Video/myCam.avi')
# in while:
#     ret, frame = cam.read()

#     cv2.imshow('realVideo', frame)
#     cv2.moveWindow('realVideo', 0, 0)    
# =============================================

# =========Save the Video:=========
# outVid = cv2.VideoWriter('Video/myCam.avi', cv2.VideoWriter_fourcc(*'XVID'), 21, (dispW, dispH)) # Write the Video with fps = 21
# in while:
#     ret, frame = cam.read()

#     cv2.imshow('realVideo', frame)
#     cv2.moveWindow('realVideo', 0, 0)  
#     outVid.write(frame)  
# outVid.release()       #Make sure Write the video is turn off
# =============================================

ser = serial.Serial('/dev/ttyTHS1', 115200)
angleD = 86
angleN = 75
flagC = 0
ERROR_Y = 15
ERROR_X = 10

outVid = cv2.VideoWriter('Video/myCam.avi', cv2.VideoWriter_fourcc(*'XVID'), 21, (480, 640)) # Write the Video with fps = 21

timeAngle = time.time()
def detectObjects(trt_yolo, vis, frame):   
    global angleD, angleN, flagC, obj, timeAngle
    boxes, confs, clss = trt_yolo.detect(frame, 0.3)
    timeAngle = timeAngle

    #Precise poison filter (> 0.6)
    indexDel = []
    for index, value in enumerate(confs):
        if value <= 0.7:
            indexDel.append(index)
    boxes = np.delete(boxes, indexDel, 0)
    confs = np.delete(confs, indexDel)
    clss = np.delete(clss, indexDel)
    
    if len(confs) > 0: 
        flagC = 1
        frame, (x_min, y_min, x_max, y_max) = vis.draw_bboxes(frame, boxes, confs, clss)
        objX = (x_min + x_max) / 2
        objY = y_max
        obj = (int(objX), int(objY))
        errorX = objX - 640 / 2
        errorY = objY - 480 / 2
        if time.time() - timeAngle > 0.1:
            timeAngle = time.time()
            if abs(errorY) > ERROR_Y:
                angleD = int(angleD + errorY/abs(errorY))
                print('ErrorY: ', errorY)
            if abs(errorX) > ERROR_X:
                angleN = int(angleN - errorX/abs(errorX))
                print('ErrorX: ', errorX)
            if angleD > 130:
                angleD = 130
            elif angleD < 34:
                angleD = 34
            if angleN < 25:
                angleN = 25
            elif angleN > 122:
                angleN = 122
    else:
        flagC = 0
    

windowTitle = 'USB Cam'
def showCam():
    timerTest = time.time()
    global angleD, angleN, flagC
    buff = ''

    numClass = 2     #The numbers of classes
    cls_dict = get_cls_dict(numClass)
    vis = BBoxVisualization(cls_dict)
    trt_yolo = TrtYOLO('obj', numClass, False)

    camera_id = "/dev/video0"
    videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    videoCapture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
    fps = 0
    timeCount = 0
    if videoCapture.isOpened():
        windowHandle = cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
        preTime = time.time()
        while True:
            ret, frame = videoCapture.read()

            #Calc FPS
            Time = time.time()
            curr_fps = 1.0 / (Time - preTime)
            fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
            preTime = Time

            if cv2.getWindowProperty(windowTitle, cv2.WND_PROP_AUTOSIZE) >= 0:
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,0), 3)
                cv2.circle(frame, (320, 240), 2, (255, 0, 0), -1)
                cv2.putText(frame, 'C', (320, 240), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                cv2.rectangle(frame, (320 - ERROR_X, 240 - ERROR_Y), (320 + ERROR_X, 240 + ERROR_Y), (0, 255, 0), 1)

                detectObjects(trt_yolo, vis, frame)

                if flagC:
                    #On -> time count
                    timeCount = time.time()             
                    cv2.circle(frame, obj, 2, (255, 0, 0), -1)
                    cv2.putText(frame, 'obj', obj, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                else:
                    #Process -> time count
                    if (time.time() - timeCount) >= 10:
                        angleD = 86
                        angleN = 75 

                if int(angleN) >= 100 and int(angleD) >= 100:
                    data = 'D' + str(int(angleD)) + 'N' + str(int(angleN)) + '-'
                elif int(angleN) >= 100 or int(angleD) >= 100:
                    data = 'D' + str(int(angleD)) + 'N' + str(int(angleN)) + '--'
                elif int(angleN) < 100 and int(angleD) < 100:
                    data = 'D' + str(int(angleD)) + 'N' + str(int(angleN)) + '---'
                if buff != data:
                    print(data)
                    ser.write(data.encode())
                    buff = data
                    print('=========================') 
                    print('=>>>>> time', time.time() - timerTest)          

                cv2.imshow(windowTitle, frame)
                cv2.moveWindow(windowTitle, 0, 0)
                outVid.write(frame)
            else:
                break
            if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
                break
        videoCapture.release()
        cv2.destroyAllWindows()
        outVid.release()       #Make sure Write the video is turn off
    else:
        print('Unable to open Camera!')

if __name__ == '__main__':
    showCam()

