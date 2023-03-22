import cv2
import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
output_pin1 = 33 #BlackCam
output_pin2 = 32 #WhiteCam
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
p1 = GPIO.PWM(output_pin1, 50)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
p2 = GPIO.PWM(output_pin2, 50)
valueAngle1 = 6.5
valueAngle2 = 5.5
p1.start(valueAngle1)
p2.start(valueAngle2)

camID1 = "WhiteCam"
cap1 = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
camID2 = "BlackCam"
cap2 = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L2)

def mouse_callback1(event, x, y, flags, params):
    global valueAngle1, camID1
    if event == cv2.EVENT_LBUTTONDOWN:
        print(camID1 + " + Corner " + str(valueAngle1) + " => " + str(y))
        valueAngle1 += 0.5
        p1.start(valueAngle1)
        if valueAngle1 >= 8.5: 
            valueAngle1 = 6.5
            p1.start(valueAngle1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("None")
        valueAngle1 += 0.5
        p1.start(valueAngle1)
        if valueAngle1 >= 8.5: 
            valueAngle1 = 6.5
            p1.start(valueAngle1)

def mouse_callback2(event, x, y, flags, params):
    global valueAngle2, camID2
    if event == cv2.EVENT_LBUTTONDOWN:
        print(camID2 + " + Corner " + str(valueAngle2) + " => " + str(y))
        valueAngle2 += 0.5
        p2.start(valueAngle2)
        if valueAngle2 >= 7.5: 
            valueAngle2 = 5.5
            p2.start(valueAngle2)
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("None")
        valueAngle2 += 0.5
        p2.start(valueAngle2)
        if valueAngle2 >= 7.5: 
            valueAngle2 = 5.5
            p2.start(valueAngle2)

if __name__ == "__main__":
    while True:
        ret1, frame1 = cap1.read()
        cv2.imshow(camID1, frame1)
        cv2.setMouseCallback(camID1, mouse_callback1)

        ret2, frame2 = cap2.read()
        cv2.imshow(camID2, frame2)
        cv2.setMouseCallback(camID2, mouse_callback2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap1.release()
    cap2.release()
    GPIO.cleanup()
    cv2.destroyAllWindows()