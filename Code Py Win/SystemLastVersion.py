# ===============pyuic5 -x mainv1.ui -o mainv1.py===============
from libs import *
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication)
from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, Qt, QSize, QTimer, QTime, QDate, QObject, QEvent)
from PyQt5.QtGui import (QImage, QPixmap, QFont, QIcon, QColor)

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
LedW = 18
LedB = 12
GPIO.setup(LedW, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam White
GPIO.setup(LedB, GPIO.OUT, initial=GPIO.LOW) # led to noti fire in Cam Black

output_pin1 = 32 #BlackCam
output_pin2 = 33 #WhiteCam
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
p1 = GPIO.PWM(output_pin1, 50)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
p2 = GPIO.PWM(output_pin2, 50)
p1.start(6.5)
p2.start(6.5)


class MAIN_HANDLE(QMainWindow):
    camID1 = "Cam White"
    cap1 = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L2)

    camID2 = "Cam Black"
    cap2 = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    #------for func Notice------
    timeOut = 3
    valueAngle1 = 6.5
    valueAngle2 = 6.5

    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        #------------------add feature------------------#
        self.Cam1 = Camera(MAIN_HANDLE.cap1, self.uic.labelText1, MAIN_HANDLE.camID1)    
        self.Cam2 = Camera(MAIN_HANDLE.cap2, self.uic.labelText2, MAIN_HANDLE.camID2)
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
        self.timer3.start(15000)
        # Move Camera2:
        self.timer4 = QtCore.QTimer()
        self.timer4.timeout.connect(self.move_camera2)
        self.timer4.start(15000)
    
    def check_Fire(self):
        # Detected the Fire
        if self.Cam1.flag: 
            self.Cam1.countFire = time.time()
            if not self.Cam1.flagFire:
                print("Cam1: Fire!")
                GPIO.output(LedW, GPIO.HIGH)
                self.Cam1.flagFire = True
                self.Cam1.flag0Fire = False
                self.timer4.stop()
        elif time.time() - self.Cam1.countFire > MAIN_HANDLE.timeOut:
            if not self.Cam1.flag0Fire:
                print("Cam1: no Fire")
                self.Cam1.flagFire = False
                GPIO.output(LedW, GPIO.LOW)
                self.Cam1.flag0Fire = True
                self.Cam1.flag = False
                self.timer4.start()

        if self.Cam2.flag: 
            self.Cam2.countFire = time.time()
            if not self.Cam2.flagFire:
                print("Cam2: Fire!")
                GPIO.output(LedB, GPIO.HIGH)
                self.Cam2.flagFire = True
                self.Cam2.flag0Fire = False
                self.timer3.stop()
        elif time.time() - self.Cam2.countFire > MAIN_HANDLE.timeOut:
            if not self.Cam2.flag0Fire:
                print("Cam2: no Fire")
                self.Cam2.flagFire = False
                GPIO.output(LedB, GPIO.LOW)
                self.Cam2.flag0Fire = True
                self.Cam2.flag = False
                self.timer3.start()

    def clear(self): pass

    def closeEvent(self, event):
        ret = QMessageBox.information(self, "Quit Program", # title 
                                      "Are you sure to Quit?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.timer1.stop()
            self.timer2.stop()
            self.timer3.stop()
            self.timer4.stop()
            GPIO.cleanup()
            event.accept()
        else:
            event.ignore()

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


numClass = 2     #The numbers of classes
cls_dict = get_cls_dict(numClass)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO('obj', numClass, False)
class Camera:
    def __init__(self, cam_link, output, camID):
        self.source = cam_link
        self.output = output
        self.camID = camID
        self.flag = False
        self.flagFire = False
        self.flag0Fire = False
        self.countFire = 0

    def update_frame(self):          
        ret, self.frame = self.source.read()
        self.detectObjects(self.frame)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
        self.output.setPixmap(QPixmap.fromImage(image))

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
            self.flag = True
        else:
            self.flag = False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_win = MAIN_HANDLE()
    main_win.show()
    sys.exit(app.exec_())
