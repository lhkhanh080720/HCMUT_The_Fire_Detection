import Jetson.GPIO as GPIO
import time
import os
 
output_pin1 = 32 #BlackCam
output_pin2 = 33 #WhiteCam
 
GPIO.setmode(GPIO.BOARD)
 
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
p1 = GPIO.PWM(output_pin1, 50)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
p2 = GPIO.PWM(output_pin2, 50)

valueAngle = 6.5
timeOT = time.time()

 
if __name__ == '__main__':
    while True:
        if time.time() - timeOT >= 5:
            inputChar = input("Enter = ")
            if inputChar == 'q':
                break
            valueAngle = float(inputChar)
            p1.start(valueAngle)
            p2.start(valueAngle)
    GPIO.cleanup()
    os._exit(1)
