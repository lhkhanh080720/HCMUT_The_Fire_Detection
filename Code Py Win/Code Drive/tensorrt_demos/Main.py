import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
LedW = 18
LedW1= 7
LedB = 12
LedB1= 16

GPIO.setup(LedW, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam White
GPIO.setup(LedB, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam Black
GPIO.setup(LedW1, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam White
GPIO.setup(LedB1, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam Black 
GPIO.output(LedB1, GPIO.LOW)
GPIO.output(LedW1, GPIO.LOW)

if __name__ == "__main__":
    while True:
        # controlServel()
        # time.sleep(0.5)
        text = input("Enter: ")
        if text == "off":
            GPIO.output(LedB, GPIO.HIGH)
            GPIO.output(LedW, GPIO.LOW)
            print("12 - Hight")
        elif text == "on":
            GPIO.output(LedW, GPIO.HIGH)
            GPIO.output(LedB, GPIO.LOW)
            print("18 - Hight")
        elif text == "all":
            GPIO.output(LedW, GPIO.HIGH)
            GPIO.output(LedB, GPIO.HIGH)
        elif text == "out":
            GPIO.output(LedB, GPIO.LOW)
            GPIO.output(LedW, GPIO.LOW)
            GPIO.cleanup()
            break
