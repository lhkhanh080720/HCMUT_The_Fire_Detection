from tkinter import *
import tkinter
from tkinter.ttk import * #for combobox
import cv2
import PIL.Image, PIL.ImageTk
from threading import Thread
from datetime import datetime

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

camera_id = "/dev/video1"
videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
# Wait a second to let the port initialize
camID = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=21/1 ! nvvidconv flip-method='+'2'+' ! video/x-raw, width='+'640'+', height='+'480'+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink' 
cam = cv2.VideoCapture(camID)
time.sleep(1)


class MultiCameraCapture:
    def __init__(self, sources: dict) -> None:
        assert sources
        print(sources)

        self.captures = {}
        for camera_name, link in sources.items():
            


photo = None
def updateFrame():
    global canvas, photo, frame, canvas2, frame2, photo2
    ret, frame = videoCapture.read()
    ret, frame2 = cam.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))

    canvas2.create_image(0, 0, image=photo2, anchor=tkinter.NW)
    window.after(10, updateFrame)


window = Tk()

window.title("The Fire Detection")
window.geometry("1300x650")
# window.resizable(False, False)
#add background
canvas1 = Canvas(window, width=1120, height=800, bg='red')
canvas1.place(x = 0, y = 0) 

#add cam
canvas = Canvas(window, width=640, height=480)
canvas.place(x = 4, y = 100)
canvas2 = Canvas(window, width=640, height=480)
canvas2.place(x = 650, y = 100)
updateFrame()

window.mainloop()


# camID = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=21/1 ! nvvidconv flip-method='+'2'+' ! video/x-raw, width='+'640'+', height='+'480'+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink' 
# cam = cv2.VideoCapture(camID)

# camera_id = "/dev/video1"
# videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
# videoCapture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))

# # while True:
# #     ret, frame = cam.read()
# #     ret, frame2 = videoCapture.read()

# #     cv2.imshow('Cam', frame)
# #     cv2.moveWindow('Cam', 0, 0)  

# #     cv2.imshow('Webcam', frame2)
# #     cv2.moveWindow('Webcam',  650, 1) 

# #     if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
# #         break


# photo = None
# photo2 = None
# count = 0
# def updateFrame():
#     global cam, videoCapture, frame, frame2, canvas2, count

#     ret, frame = cam.read()
#     if count < 2:
#         print('===========================')
#         cv2.imshow('Cam', frame)
#         cv2.moveWindow('Cam', count*100, 0) 
#     # ret, frame2 = videoCapture.read()
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
#     # frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    
#     # photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))

#     canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
#     # canvas2.create_image(0, 0, image=photo2, anchor=tkinter.NW)
#     window.after(10, updateFrame)

# window = Tk()

# window.title("The Fire Detection")
# window.geometry("1035x650")
# window.resizable(False, False)
# #add background
# canvas = Canvas(window, width=1120, height=800, bg='red')
# canvas.place(x = 0, y = 0) 
# #add cam1
# canvas2 = Canvas(window, width=640, height=480)
# canvas2.place(x = 4, y = 100)
# #add cam2
# # canvas1 = Canvas(window, width=640, height=480)
# # canvas1.place(x = 650, y = 100)

# updateFrame()

# window.mainloop()
