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

ser = serial.Serial('/dev/ttyTHS1', 115200)
# Wait a second to let the port initialize
time.sleep(1)
angleD = 86
angleN = 75
flagC = 0
ERROR_Y = 15
ERROR_X = 10
errorState = 0
detectFire = 0
i = 1
flagS = 1


def acceptControl():
    global flagS
    if btnL["state"] == "disabled":
        btnL["state"] = "active"
        btnR["state"] = "active"
        btnD["state"] = "active"
        btnU["state"] = "active"
        btnDL["state"] = "active"
        btnUL["state"] = "active"
        flagS = 0
    else:
        btnL["state"] = "disabled"
        btnR["state"] = "disabled"
        btnD["state"] = "disabled"
        btnU["state"] = "disabled"
        btnDL["state"] = "disabled"
        btnUL["state"] = "disabled"
        flagS = 1

def showError():
    global errorState
    if errorState == 1:
        errorState = 0
    else:
        errorState = 1

def acceptDetect():
    global detectFire, i, flagS
    if detectFire == 1:
        detectFire = 0
        listbox.insert(i, "------Out------")
    else:
        detectFire = 1
        listbox.insert(i, "Detecting....")
        btnL["state"] = "disabled"
        btnR["state"] = "disabled"
        btnD["state"] = "disabled"
        btnU["state"] = "disabled"
        btnDL["state"] = "disabled"
        btnUL["state"] = "disabled"
        flagS = 1
    i += 1


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
        if time.time() - timeAngle > 0.3:
            timeAngle = time.time()
            if abs(errorY) > ERROR_Y:
                angleD = int(angleD + errorY/abs(errorY))
            if abs(errorX) > ERROR_X:
                angleN = int(angleN - errorX/abs(errorX))
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

photo = None
numClass = 2     #The numbers of classes
cls_dict = get_cls_dict(numClass)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO('obj', numClass, False)
timeCount = 0
buff = ''
flagV = 0
def updateFrame():
    global canvas, photo, frame, errorState, detectFire, timeCount, angleD, angleN, buff, flagS, outVid, flagV
    ret, frame = videoCapture.read()
    
    if errorState:
        cv2.circle(frame, (320, 240), 2, (255, 0, 0), -1)
        cv2.rectangle(frame, (320 - ERROR_X, 240 - ERROR_Y), (320 + ERROR_X, 240 + ERROR_Y), (0, 255, 0), 1)
        if flagC:
            cv2.circle(frame, obj, 2, (255, 0, 0), -1)
    if detectFire:
        detectObjects(trt_yolo, vis, frame)
        if flagC:
            #On -> time count
            timeCount = time.time()
            if flagV == 0:
                now = datetime.now()
                nameVideo = 'Videos/' + str(now.strftime("%d-%m-%Y %H_%M_%S")) + '.avi'
                outVid = cv2.VideoWriter(nameVideo, cv2.VideoWriter_fourcc(*'XVID'), 21, (640, 480)) # Write the Video with fps = 21 
                flagV = 1
            outVid.write(frame)            
        else:
            #Process -> time count
            if (time.time() - timeCount) >= 3:
                angleD = 86
                angleN = 75
                if flagV:
                    outVid.release()       #Make sure Write the video is turn off
                    flagV = 0
        if flagS:
            if int(angleN) >= 100 and int(angleD) >= 100:
                data = 'D' + str(int(angleD)) + 'N' + str(int(angleN)) + '-'
            elif int(angleN) >= 100 or int(angleD) >= 100:
                data = 'D' + str(int(angleD)) + 'N' + str(int(angleN)) + '--'
            elif int(angleN) < 100 and int(angleD) < 100:
                data = 'D' + str(int(angleD)) + 'N' + str(int(angleN)) + '---'
            if buff != data:
                ser.write(data.encode())
                buff = data

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    window.after(10, updateFrame)

def goUp():
    global i
    dataS = '#UC------'
    ser.write(dataS.encode())
    listbox.insert(i, dataS)
    i += 1
def goDown():
    global i
    dataS = '#DC------'
    ser.write(dataS.encode())
    listbox.insert(i, dataS)
    i += 1
def goRight():
    global i
    dataS = '#RC------'
    ser.write(dataS.encode())
    listbox.insert(i, dataS)
    i += 1
def goLeft():
    global i
    dataS = '#LC------'
    ser.write(dataS.encode())
    listbox.insert(i, dataS)
    i += 1
def goUpL():
    global i
    dataS = '#UL------'
    ser.write(dataS.encode())
    listbox.insert(i, dataS)
    i += 1
def goDownL():
    global i
    dataS = '#DL------'
    ser.write(dataS.encode())
    listbox.insert(i, dataS)
    i += 1


window = Tk()

window.title("The Fire Detection")
window.geometry("1035x650")
window.resizable(False, False)
#add background
canvas1 = Canvas(window, width=1120, height=800, bg='white')
canvas1.place(x = 0, y = 0) 
canvas1.create_rectangle(0, 0, 1035, 90, width=1)
canvas1.create_rectangle(0, 90, 662, 650, width=1)
canvas1.create_rectangle(662, 90, 900, 650, width=1)
canvas1.create_rectangle(662, 90, 900, 340, width=1)
canvas1.create_rectangle(900, 90, 1035, 650, width=1)
canvas1.create_rectangle(662, 550, 900, 650, width=1)
#add logo
img = PIL.Image.open("Images/logo.png")
img = img.resize(((75, 75)))
photoImg = PIL.ImageTk.PhotoImage(img)
lbl1 = tkinter.Label(window, image=photoImg, bg='white', width=80, anchor=W)
lbl1.place(x = 4, y = 4)
#add cam
canvas = Canvas(window, width=640, height=480)
canvas.place(x = 4, y = 100)
#add button control
img1 = PIL.Image.open("Images/left.png")
photoImg1 = PIL.ImageTk.PhotoImage(img1)
btnL = tkinter.Button(window, image=photoImg1, command = goLeft, state=DISABLED, bg = 'white', width=50,height=50)
btnL.place(x = 680, y = 170)
img2 = PIL.Image.open("Images/up.png")
photoImg2 = PIL.ImageTk.PhotoImage(img2)
btnU = tkinter.Button(window, image=photoImg2, command = goUp, state=DISABLED, bg = 'white', width=50,height=50)
btnU.place(x = 750, y = 100)
img3 = PIL.Image.open("Images/right.png")
photoImg3 = PIL.ImageTk.PhotoImage(img3)
btnR = tkinter.Button(window, image=photoImg3, command = goRight, state=DISABLED, bg = 'white', width=50,height=50)
btnR.place(x = 820, y = 170)
img4 = PIL.Image.open("Images/down.png")
photoImg4 = PIL.ImageTk.PhotoImage(img4)
btnD = tkinter.Button(window, image=photoImg4, command = goDown, state=DISABLED, bg = 'white', width=50,height=50)
btnD.place(x = 750, y = 240)
img5 = PIL.Image.open("Images/up.png")
photoImg5 = PIL.ImageTk.PhotoImage(img5)
btnUL = tkinter.Button(window, image=photoImg5, command = goUpL, state=DISABLED, bg = 'white', width=50,height=50)
btnUL.place(x = 750, y = 350)
img6 = PIL.Image.open("Images/down.png")
photoImg6 = PIL.ImageTk.PhotoImage(img6)
btnDL = tkinter.Button(window, image=photoImg6, command = goDownL, state=DISABLED, bg = 'white', width=50,height=50)
btnDL.place(x = 750, y = 450)
#add listbox
listbox = Listbox(height=24, width=11, activestyle='dotbox', font='Helvetica')
listbox.place(x = 918, y = 100)
#add text
lbl = tkinter.Label(window, text="Lê Hữu Khánh\r1812590",bg='white', fg="#102A8B", font=("Segoe UI", 13), height=3, anchor=E)
lbl.place(x = 900, y = 10)
#add button cam
img7 = PIL.Image.open("Images/fire-extinguisher.png")
img7 = img7.resize(((48, 48)))
photoImg7 = PIL.ImageTk.PhotoImage(img7)
btnDC = tkinter.Button(window, image=photoImg7, command = acceptDetect, bg = 'white', width=50,height=50)
btnDC.place(x = 78, y = 592)
img8 = PIL.Image.open("Images/error (1).png")
photoImg8 = PIL.ImageTk.PhotoImage(img8)
btnEC = tkinter.Button(window, image=photoImg8, command = showError, bg = 'white', width=50,height=50)
btnEC.place(x = 290, y = 592)
img9 = PIL.Image.open("Images/control.png")
photoImg9 = PIL.ImageTk.PhotoImage(img9)
btnAC = tkinter.Button(window, image=photoImg9, command = acceptControl, bg = 'white', width=50,height=50)
btnAC.place(x = 508, y = 592)

updateFrame()

window.mainloop()























