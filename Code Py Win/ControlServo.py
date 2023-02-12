import Jetson.GPIO as GPIO
#import RPi.GPIO as GPIO
import time
import threading
import os
import cv2
 
output_pin1 = 32 #BlackCam
output_pin2 = 33 #WhiteCam
 
GPIO.setmode(GPIO.BOARD)
 
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
p1 = GPIO.PWM(output_pin1, 50)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
p2 = GPIO.PWM(output_pin2, 50)
 
def p1_loop():
    while flag:
        p1.start(8)
        print("p1 start at 2.5%")
        time.sleep(1)
        # p1.start(7.25)
        # print("p1 start at 7.25%")
        # time.sleep(1)
        # p1.start(12)
        # print("p1 start at 12%")
        # time.sleep(1)
        # p1.start(7.25)
        # print("p1 start at 7.25%")
        # time.sleep(1)
 
def p2_loop():
    while flag:
        p2.start(8)
        print("p2 start at 2.5%")
        time.sleep(1)
        # p2.start(7.25)
        # print("p2 start at 7.25%")
        # time.sleep(1)
        # p2.start(12)
        # print("p2 start at 12%")
        # time.sleep(1)
        # p2.start(7.25)
        # print("p2 start at 7.25%")
        # time.sleep(1)
 
if __name__ == '__main__':
    count = time.time()
    if time.time() - count <= 3:
        p1.start(6)
        p2.start(6)
        time.sleep(0.5)
    while True:
        timeCOunt = 7
        if time.time() - count >= timeCOunt:
            break
            
    # print("You pressed q")
    # flag = False
    # thread_1.join()
    # thread_2.join()
    p1.stop()
    p2.stop()
    GPIO.cleanup()
    os._exit(1)