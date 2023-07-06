# ===============pyuic5 -x ui_interface.ui -o ui_interface.py===============
from libs import *
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication)
from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, Qt, QSize, QTimer, QTime, QDate, QObject, QEvent)
from PyQt5.QtGui import (QImage, QPixmap, QFont, QIcon, QColor)
import datetime

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
WaterW = 18 # PIN (+) in motor W
WaterB = 12 # PIN (+) in motor B

GPIO.setup(WaterW, GPIO.OUT, initial=GPIO.LOW) # control waterW
GPIO.setup(WaterB, GPIO.OUT, initial=GPIO.LOW) # control waterB
GPIO.output(WaterW, GPIO.LOW)
GPIO.output(WaterB, GPIO.LOW)

output_pin1 = 33 #BlackCam
output_pin2 = 32 #WhiteCam
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
p1 = GPIO.PWM(output_pin1, 50)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
p2 = GPIO.PWM(output_pin2, 50)
p1.start(7)
indexS1 = [306, 234, 156]
statusS1 = 0
p2.start(6)
indexS2 = [271, 157, 93]#Black CAm
statusS2 = 0

timeB = time.time()
timeW = time.time()

class MAIN_HANDLE(QMainWindow):
    camID1 = "WhiteCam"
    cap1 = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    camID2 = "BlackCam"
    cap2 = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L2)

    #------for func Notice------
    timeOut = 2
    valueAngle1 = 7
    valueAngle2 = 6

    statusWarning = False

    areaW = False
    areaB = False

    flagControl = False

    statusBtnW = False
    statusBtnB = False

    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        #Add
        #=================Stack Widget=================#
        self.uic.mainFrame.setCurrentWidget(self.uic.homeF)

        self.uic.menuBtn.clicked.connect(self.show2Cam)
        self.uic.cam1Btn.clicked.connect(self.settingsSystem)
        self.uic.camWBtn.clicked.connect(self.camWBtnFc)
        self.uic.camBBtn.clicked.connect(self.camBBtnFc)
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
        self.timer3 = QtCore.QTimer()
        self.timer3.timeout.connect(self.move_camera1)
        # self.timer3.start(15000)
        # Move Camera2:
        self.timer4 = QtCore.QTimer()
        self.timer4.timeout.connect(self.move_camera2)
        # self.timer4.start(15000)
        # Feature for 2 widget Cam1 and Cam2
        self.Cam3 = Camera(MAIN_HANDLE.cap1, self.uic.label_5, MAIN_HANDLE.camID1)
        self.Cam4 = Camera(MAIN_HANDLE.cap2, self.uic.label_6, MAIN_HANDLE.camID2)
        self.timer5 = QtCore.QTimer()
        self.timer5.timeout.connect(self.Cam3.update_frame)
        self.timer5.timeout.connect(self.Cam4.update_frame)
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
        self.timer5.stop()
        self.timer2.start(1)
        self.timer1.start(1)
        self.timer3.start(15000)
        self.timer4.start(15000)
        self.timer8.stop()
        p1.stop()
        p2.stop()
        MAIN_HANDLE.flagControl = False
        
    # Widget 2: Settings
    def settingsSystem(self):
        self.uic.mainFrame.setCurrentWidget(self.uic.cam1F)
        self.uic.menuBtn.setStyleSheet("background-color: #16191d;")
        self.uic.cam1Btn.setStyleSheet("background-color: #1f232a;")
        MAIN_HANDLE.flagControl = True
        GPIO.output(WaterW, GPIO.LOW)
        GPIO.output(WaterB, GPIO.LOW)
        p1.start(7)
        p2.start(6)
        self.timer1.stop()
        self.timer7.stop()
        self.timer8.stop()
        self.timer2.stop()
        self.timer3.stop()
        self.timer4.stop()
        self.timer5.start(1)

    # Btn control Cam W
    def camWBtnFc(self):
        self.uic.camBBtn.setStyleSheet("background-color: #1f232a;")
        self.uic.camWBtn.setStyleSheet("background-color: #16191d;")
        if not MAIN_HANDLE.statusBtnW:
            GPIO.output(WaterW, GPIO.HIGH)
            self.uic.camWBtn.setText("OFF")
        elif MAIN_HANDLE.statusBtnW:
            GPIO.output(WaterW, GPIO.LOW)
            self.uic.camWBtn.setText("ON")
        MAIN_HANDLE.statusBtnW = not MAIN_HANDLE.statusBtnW

    # Btn control Cam W
    def camBBtnFc(self):
        self.uic.camWBtn.setStyleSheet("background-color: #1f232a;")
        self.uic.camBBtn.setStyleSheet("background-color: #16191d;")
        if not MAIN_HANDLE.statusBtnB:
            GPIO.output(WaterB, GPIO.HIGH)
            self.uic.camBBtn.setText("OFF")
        elif MAIN_HANDLE.statusBtnB:
            GPIO.output(WaterB, GPIO.LOW)
            self.uic.camBBtn.setText("ON")
        MAIN_HANDLE.statusBtnB = not MAIN_HANDLE.statusBtnB

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
                self.timer3.stop()
                self.timer4.stop()
                p1.stop()
                p2.stop()
        elif time.time() - self.Cam1.countFire > MAIN_HANDLE.timeOut:
            if not self.Cam1.flag0Fire:
                print("Cam1: no Fire")
                self.Cam1.objectF = 0
                self.Cam1.flagFire = False
                self.Cam1.flag0Fire = True
                self.Cam1.flag = False
                self.timer3.start(15000)
                self.timer4.start(15000)
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
                self.timer3.stop()
                self.timer4.stop()
                p1.stop()
                p2.stop()
        elif time.time() - self.Cam2.countFire > MAIN_HANDLE.timeOut:
            if not self.Cam2.flag0Fire:
                print("Cam2: no Fire")
                self.Cam2.flagFire = False
                self.Cam2.flag0Fire = True
                self.Cam2.flag = False
                self.Cam2.objectF = 0
                self.timer3.start(15000)
                self.timer4.start(15000)
                self.Cam2.saveCam = False
                outVid2.release()

        if self.Cam1.flag0Fire and self.Cam2.flag0Fire:
            self.timer7.stop()
            self.timer8.stop()
            self.areaW = False
            self.areaB = False
            self.uic.mainFrame.setStyleSheet("background-color: #1f232a;")    
            GPIO.output(WaterB, GPIO.LOW)
            GPIO.output(WaterW, GPIO.LOW)
            self.Cam1.objectF = 0
            self.Cam2.objectF = 0

    # Control servo to move cam
    def move_camera1(self):
        global statusS1
        p1.start(MAIN_HANDLE.valueAngle1)
        if MAIN_HANDLE.valueAngle1 == 7:
            statusS1 = 0
        else:
            statusS1 += 1
        MAIN_HANDLE.valueAngle1 += 0.5
        if MAIN_HANDLE.valueAngle1 > 8.5:
            MAIN_HANDLE.valueAngle1 = 7
            p1.start(MAIN_HANDLE.valueAngle1)
            statusS1 = 0
            self.timer3.start(15000)
        else:
            self.timer3.start(5000)

    def move_camera2(self):
        global statusS2
        p2.start(MAIN_HANDLE.valueAngle2)
        if MAIN_HANDLE.valueAngle2 == 6:
            statusS2 = 0
        else:
            statusS2 += 1
        MAIN_HANDLE.valueAngle2 += 0.5
        if MAIN_HANDLE.valueAngle2 > 7.5:
            MAIN_HANDLE.valueAngle2 = 6
            p2.start(MAIN_HANDLE.valueAngle2)
            statusS2 = 0
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
        global statusS1, statusS2, indexS1, indexS2, timeW, timeB
        if len(self.Cam1.objectF) > 0:
            for index, value in enumerate(self.Cam1.objectF):
                if value <= indexS1[statusS1]:
                    self.areaB = True 
                    self.areaW = False or self.areaW
                elif value > indexS1[statusS1]:
                    self.areaW = True
                    self.areaB = False or self.areaB
        else:
            self.areaB = False
            self.areaW = False

        if len(self.Cam2.objectF) > 0:
            for index, value in enumerate(self.Cam2.objectF):
                if value <= indexS2[statusS2]:
                    self.areaW = True 
                    self.areaB = False or self.areaB
                elif value > indexS2[statusS2]:
                    self.areaB = True
                    self.areaW = False or self.areaW
        else:
            self.areaW = False or self.areaW
            self.areaB = False or self.areaB

        if self.areaB:
            print("area ==>> B")
            if not MAIN_HANDLE.flagControl:
                GPIO.output(WaterB, GPIO.HIGH)
                timeB = time.time()
        else:
            if not MAIN_HANDLE.flagControl and time.time() - timeB >= 2:
                GPIO.output(WaterB, GPIO.LOW)

        if self.areaW:
            print("area ==>> W")
            if not MAIN_HANDLE.flagControl:
                GPIO.output(WaterW, GPIO.HIGH)
                timeW = time.time()
        else:
            if not MAIN_HANDLE.flagControl and time.time() - timeW >= 2:
                GPIO.output(WaterW, GPIO.LOW)
        
        self.areaW = False 
        self.areaB = False

    def clear(self): pass

    def closeEvent(self, event):
        GPIO.output(WaterW, GPIO.LOW)
        GPIO.output(WaterB, GPIO.LOW)

        self.timer1.stop()
        self.timer2.stop()
        self.timer3.stop()
        self.timer4.stop()
        self.timer5.stop()
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
        self.objectF = 0

    def update_frame(self):   
        global statusS1, statusS2, indexS1, indexS2       
        ret, self.frame = self.source.read()
        if not MAIN_HANDLE.flagControl:
            self.detectObjects(self.frame)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        # add text feature
        now = datetime.datetime.now()
        self.text = self.camID + now.strftime("--%d/%m/%Y %H:%M")
        cv2.putText(self.frame, self.text, (20, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
        # add line
        if self.camID == "WhiteCam":
            cv2.line(self.frame, (0, indexS1[statusS1]), (640, indexS1[statusS1]), (0, 255, 0), 2)
        elif self.camID == "BlackCam":
            cv2.line(self.frame, (0, indexS2[statusS2]), (640, indexS2[statusS2]), (0, 255, 0), 2)
        
        if MAIN_HANDLE.flagControl:
            self.frame = cv2.resize(self.frame, (600, 450))

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
            self.frame, y_max = vis.draw_bboxes(frame, boxes, confs, clss)
            self.objectF = y_max
            self.flag = True
        else:
            self.flag = False
            self.objectF = []

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_win = MAIN_HANDLE()
    main_win.show()
    sys.exit(app.exec_())
