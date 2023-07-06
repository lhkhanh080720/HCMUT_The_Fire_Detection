from pyexpat.errors import XML_ERROR_SUSPEND_PE
from time import sleep
import serial
import string
import os
import time
import argparse # Library support Command Line Interface (CLI)
import numpy as np

import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver

from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO

ser = serial.Serial('/dev/ttyUSB0', 115200)
# while True:
#     dataRec = input("Input = ")
#     ser.write(dataRec.encode())
#     sleep(1)

evt = -1
def click(event, x, y, flags, params):
    global evt
    global pnt
    global xReal
    global yReal
    if event == cv2.EVENT_LBUTTONDOWN:
        #print('Mouse event was: ', event)
        #print(x, ',', y)
        pnt = (x, y)
        xReal = x
        yReal = y
        evt = event

outVid = cv2.VideoWriter('Video/myCam.avi', cv2.VideoWriter_fourcc(*'XVID'), 21, (640, 480)) # Write the Video with fps = 21
windowTitle = 'USB Cam'
def showCam():
    buff = ''

    cv2.namedWindow(windowTitle)
    cv2.setMouseCallback(windowTitle, click)

    camera_id = "/dev/video0"
    videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
    videoCapture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
    
    fps = 0
    if videoCapture.isOpened():
        windowHandle = cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
        frame_width = int(videoCapture.get(3))
        frame_height = int(videoCapture.get(4))
        #print('=======> ', frame_height, ' ', frame_width)
        preTime = time.time()
        while True:
            ret, frame = videoCapture.read()

            # #Calc FPS
            Time = time.time()
            curr_fps = 1.0 / (Time - preTime)
            fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
            preTime = Time

            if cv2.getWindowProperty(windowTitle, cv2.WND_PROP_AUTOSIZE) >= 0:
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,0), 3)
                
                #cv2.circle(frame, (int(frame_width/2), int(frame_height/2)), 2, (0, 0, 255), -1)
                #cv2.putText(frame, '(320, 240)', (int(frame_width/2), int(frame_height/2)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                #cv2.line(frame, (0, 240), (640, 240), (0, 0 ,255), 1)

                if evt == 1:
                    cv2.circle(frame, pnt, 2, (0, 0, 255), -1)
                    cv2.putText(frame, str(pnt), pnt, cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                    xSend = -9 * xReal / 80 + 132
                    ySend = -47 * yReal / 480 + 132
                    data = '-' + str(int(xSend)) + '-' + str(int(ySend)) + '\r'
                    if buff != data:
                        print(data)
                        ser.write(data.encode())
                        buff = data
                        print('=========================')

                cv2.imshow(windowTitle, frame)
                outVid.write(frame)  
                #cv2.moveWindow(windowTitle, 0, 0)
               
            else:
                break
            if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
                break
        videoCapture.release()
        cv2.destroyAllWindows()
        outVid.release() 
    else:
        print('Unable to open Camera!')


if __name__ == '__main__':
    showCam()