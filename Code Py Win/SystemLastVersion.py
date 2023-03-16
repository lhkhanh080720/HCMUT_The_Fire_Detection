# ===============pyuic5 -x ui_interface.ui -o ui_interface.py===============
from libs import *
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication)
from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, Qt, QSize, QTimer, QTime, QDate, QObject, QEvent)
from PyQt5.QtGui import (QImage, QPixmap, QFont, QIcon, QColor)
import datetime

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
WaterW = 18 # PIN (+) in motor W
WaterW1= 7  # PIN (-) in motor W
WaterB = 12 # PIN (+) in motor B
WaterB1= 16 # PIN (-) in motor B

LedW = 11
LedB = 13
GPIO.setup(LedW, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam White
GPIO.setup(LedB, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam Black
GPIO.setup(WaterW, GPIO.OUT, initial=GPIO.LOW) # control waterW
GPIO.setup(WaterB, GPIO.OUT, initial=GPIO.LOW) # control waterB
GPIO.setup(WaterW1, GPIO.OUT, initial=GPIO.LOW) # control waterW
GPIO.setup(WaterB1, GPIO.OUT, initial=GPIO.LOW) # control waterB
GPIO.output(LedW, GPIO.HIGH)
GPIO.output(LedB, GPIO.HIGH)
GPIO.output(WaterW, GPIO.LOW)
GPIO.output(WaterB, GPIO.LOW)
GPIO.output(WaterW1, GPIO.LOW)
GPIO.output(WaterB1, GPIO.LOW)

output_pin1 = 32 #BlackCam
output_pin2 = 33 #WhiteCam
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
p1 = GPIO.PWM(output_pin1, 50)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
p2 = GPIO.PWM(output_pin2, 50)
p1.start(5.5)
p2.start(6.5)

class MAIN_HANDLE(QMainWindow):
    camID1 = "WhiteCam"
    cap1 = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    camID2 = "BlackCam"
    cap2 = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L2)

    #------for func Notice------
    timeOut = 3
    valueAngle1 = 5.5
    valueAngle2 = 6.5

    statusWarning = False

    areaW = False
    aeraB = False

    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        #Add
        #=================Stack Widget=================#
        self.uic.mainFrame.setCurrentWidget(self.uic.homeF)

        self.uic.menuBtn.clicked.connect(self.show2Cam)
        self.uic.cam1Btn.clicked.connect(self.showCam1)
        self.uic.cam2Btn.clicked.connect(self.showCam2)
        #=================Add feature=================#
        self.Cam1 = Camera(MAIN_HANDLE.cap1, self.uic.label_3, MAIN_HANDLE.camID1)    
        self.Cam2 = Camera(MAIN_HANDLE.cap2, self.uic.label_4, MAIN_HANDLE.camID2)
        self.Cam1.update_frame()
        self.Cam2.update_frame()
        # Update Camera
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.Cam1.update_frame)
        self.timer1.timeout.connect(self.Cam2.update_frame)
        self.timer1.start(1)
        # Detect the Fire
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.check_Fire)
        self.timer2.start(1)
        # Move Camera1:
        # self.timer3 = QtCore.QTimer()
        # self.timer3.timeout.connect(self.move_camera1)
        # self.timer3.start(15000)
        # Move Camera2:
        # self.timer4 = QtCore.QTimer()
        # self.timer4.timeout.connect(self.move_camera2)
        # self.timer4.start(15000)
        # Feature for 2 widget Cam1 and Cam2
        self.Cam3 = Camera(MAIN_HANDLE.cap1, self.uic.label_5, MAIN_HANDLE.camID1)
        self.Cam4 = Camera(MAIN_HANDLE.cap2, self.uic.label_6, MAIN_HANDLE.camID2)
        self.timer5 = QtCore.QTimer()
        self.timer5.timeout.connect(self.Cam3.update_frame)
        self.timer6 = QtCore.QTimer()
        self.timer6.timeout.connect(self.Cam4.update_frame)
        # Warning in system
        self.timer7 = QtCore.QTimer()
        self.timer7.timeout.connect(self.warningFire)
        # Check location of the fire
        self.timer8 = QtCore.QTimer()
        self.timer8.timeout.connect(self.controlWater)

    # Widget 1: Show 2 camera
    def show2Cam(self):
        self.uic.mainFrame.setCurrentWidget(self.uic.homeF)
        self.uic.menuBtn.setStyleSheet("background-color: #1f232a;")
        self.uic.cam1Btn.setStyleSheet("background-color: #16191d;")
        self.uic.cam2Btn.setStyleSheet("background-color: #16191d;")
        self.timer1.start(1)
        
    # Widget 2: Show camera 1
    def showCam1(self):
        self.uic.mainFrame.setCurrentWidget(self.uic.cam1F)
        self.uic.menuBtn.setStyleSheet("background-color: #16191d;")
        self.uic.cam1Btn.setStyleSheet("background-color: #1f232a;")
        self.uic.cam2Btn.setStyleSheet("background-color: #16191d;")
        self.timer5.start(1)

        self.timer1.stop()
        self.timer6.stop()

    # Widget 3: Show camera 2
    def showCam2(self):
        self.uic.mainFrame.setCurrentWidget(self.uic.cam2F)
        self.uic.menuBtn.setStyleSheet("background-color: #16191d;")
        self.uic.cam1Btn.setStyleSheet("background-color: #16191d;")
        self.uic.cam2Btn.setStyleSheet("background-color: #1f232a;")
        self.timer6.start(1)
        
        self.timer1.stop()
        self.timer5.stop()

    # Detected the Fire
    def check_Fire(self):
        global outVid1, outVid2
        if self.Cam1.flag:
            self.Cam1.countFire = time.time()
            if not self.Cam1.flagFire:
                if not self.timer7.isActive():
                    print("Timer is running")
                    self.timer7.start(700)
                titleVideo = datetime.datetime.now()
                outVid1 = cv2.VideoWriter('Videos/WCam/' + str(titleVideo) + '.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 480)) # Write the Video with fps = 21
                print("Name video: ", str(titleVideo))
                print("Cam1: Fire!")
                # Control water & led
                if not self.timer8.isActive():
                    self.timer8.start(1)
                self.Cam1.flagFire = True
                self.Cam1.flag0Fire = False 
                self.Cam1.saveCam = True
                # self.timer4.stop()
        elif time.time() - self.Cam1.countFire > MAIN_HANDLE.timeOut:
            if not self.Cam1.flag0Fire:
                print("Cam1: no Fire")
                self.Cam1.flagFire = False
                self.Cam1.flag0Fire = True
                self.Cam1.flag = False
                # self.timer4.start()
                self.Cam1.saveCam = False
                outVid1.release()

        if self.Cam2.flag: 
            self.Cam2.countFire = time.time()
            if not self.Cam2.flagFire:
                if not self.timer7.isActive():
                    self.timer7.start(700)
                titleVideo1 = datetime.datetime.now()
                outVid2 = cv2.VideoWriter('Videos/BCam/' + str(titleVideo1) + '.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (640, 480)) # Write the Video with fps = 21
                print("Name video: ", str(titleVideo1))
                print("Cam2: Fire!")
                # Control water & led
                if not self.timer8.isActive():
                    self.timer8.start(1)
                self.Cam2.flagFire = True
                self.Cam2.flag0Fire = False
                self.Cam2.saveCam = True
                # self.timer3.stop()
        elif time.time() - self.Cam2.countFire > MAIN_HANDLE.timeOut:
            if not self.Cam2.flag0Fire:
                print("Cam2: no Fire")
                self.Cam2.flagFire = False
                self.Cam2.flag0Fire = True
                self.Cam2.flag = False
                # self.timer3.start()
                self.Cam2.saveCam = False
                outVid2.release()

        if self.Cam1.flag0Fire and self.Cam2.flag0Fire:
            self.timer7.stop()
            self.timer8.stop()
            self.aeraW = False
            self.aeraB = False
            self.uic.mainFrame.setStyleSheet("background-color: #1f232a;")    
            GPIO.output(LedW, GPIO.LOW)
            GPIO.output(LedB, GPIO.LOW)  
            self.Cam1.objectF = (0, 0)
            self.Cam2.objectF = (0, 0)

    # Control servo to move cam
    def move_camera1(self):
        p1.start(MAIN_HANDLE.valueAngle1)
        MAIN_HANDLE.valueAngle1 += 0.5
        if MAIN_HANDLE.valueAngle1 > 9:
            MAIN_HANDLE.valueAngle1 = 6.5
            p1.start(MAIN_HANDLE.valueAngle1)
            self.timer3.start(15000)
        else:
            self.timer3.start(5000)

    def move_camera2(self):
        p2.start(MAIN_HANDLE.valueAngle2)
        MAIN_HANDLE.valueAngle2 += 0.5
        if MAIN_HANDLE.valueAngle2 > 9:
            MAIN_HANDLE.valueAngle2 = 6.5
            p2.start(MAIN_HANDLE.valueAngle2)
            self.timer4.start(15000)
        else:
            self.timer4.start(5000)

    def warningFire(self):
        if not MAIN_HANDLE.statusWarning:
            self.uic.mainFrame.setStyleSheet("background-color: rgb(255, 0, 0);")
        elif MAIN_HANDLE.statusWarning:
            self.uic.mainFrame.setStyleSheet("background-color: #1f232a;")
        if not MAIN_HANDLE.statusWarning:
            MAIN_HANDLE.statusWarning = True
        elif MAIN_HANDLE.statusWarning:
            MAIN_HANDLE.statusWarning = False
    
    def controlWater(self):
        if self.Cam1.objectF != (0, 0):
            print("CAM1: Fire => " + str(self.Cam1.objectF))
            if 7/320 * self.Cam1.objectF[0] + 236 - self.Cam1.objectF[1] >= 0:
                self.aeraB = True
                self.aeraW = False
                print("CAM1: Location => Blue")
            else:
                self.aeraW = True
                self.aeraB = False
                print("CAM1: Location => Red")
        else:
            self.aeraB = False
            self.aeraW = False

        if self.Cam2.objectF != (0, 0):
            print("CAM2: Fire => " + str(self.Cam2.objectF))
            if self.Cam2.objectF[0]/32*(-1) + 246 - self.Cam2.objectF[1] >= 0:
                self.aeraW = True
                self.aeraB = False or self.aeraB
                print("CAM2: Location => Red")
            else:
                self.aeraB = True
                self.aeraW = False or self.aeraW
                print("CAM2: Location => Blue")
        else:
            self.aeraW = False or self.aeraW
            self.aeraB = False or self.aeraB

        if self.aeraB:
            GPIO.output(LedB, GPIO.HIGH)
            GPIO.output(LedB, GPIO.HIGH)
        else:
            GPIO.output(LedB, GPIO.LOW)
            GPIO.output(LedB, GPIO.HIGH)

        if self.aeraW:
            GPIO.output(LedW, GPIO.HIGH)
            GPIO.output(LedB, GPIO.HIGH)
        else:
            GPIO.output(LedW, GPIO.LOW)
            GPIO.output(LedB, GPIO.HIGH)

    def clear(self): pass

    def closeEvent(self, event):
        print(self.aeraW)
        print(self.aeraB)
        self.timer1.stop()
        self.timer2.stop()
        # self.timer3.stop()
        # self.timer4.stop()
        self.timer5.stop()
        self.timer6.stop()
        self.timer7.stop()
        self.timer8.stop()
        GPIO.cleanup()
        event.accept()

# Class Camera
numClass = 2     #The numbers of classes
cls_dict = get_cls_dict(numClass)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO('obj', numClass, False)
class Camera:
    global outVid1, outVid2
    def __init__(self, cam_link, output, camID):
        self.source = cam_link
        self.output = output
        self.camID = camID
        self.flag = False
        self.flagFire = False
        self.flag0Fire = False
        self.countFire = 0
        self.saveCam = False
        self.objectF = (0, 0)

    def update_frame(self):          
        ret, self.frame = self.source.read()
        self.detectObjects(self.frame)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        # add text feature
        now = datetime.datetime.now()
        self.text = self.camID + now.strftime("--%d/%m/%Y %H:%M")
        cv2.putText(self.frame, self.text, (20, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
        # add line
        if self.camID == "WhiteCam":
            cv2.line(self.frame, (0, 236), (640, 250), (0, 255, 0), 2)
        elif self.camID == "BlackCam":
            cv2.line(self.frame, (0, 246), (640, 230), (0, 255, 0), 2)

        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
        self.output.setPixmap(QPixmap.fromImage(image))
        # save frame
        if self.saveCam:
            if self.camID == "WhiteCam":
                outVid1.write(cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
            elif self.camID == "BlackCam":
                outVid2.write(cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))

    def detectObjects(self, frame):  
        global vis, trt_yolo
        boxes, confs, clss = trt_yolo.detect(frame, 0.3)
        #Precise poison filter (> 0.6)
        indexDel = []
        for index, value in enumerate(confs):
            if value <= 0.7:
                indexDel.append(index)
        boxes = np.delete(boxes, indexDel, 0)
        confs = np.delete(confs, indexDel)
        clss = np.delete(clss, indexDel)
        if len(confs) > 0: 
            self.frame, (x_min, y_min, x_max, y_max) = vis.draw_bboxes(frame, boxes, confs, clss)
            self.objectF = ((x_min + x_max)/2, y_max)
            self.flag = True
        else:
            self.flag = False

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_win = MAIN_HANDLE()
    main_win.show()
    sys.exit(app.exec_())
