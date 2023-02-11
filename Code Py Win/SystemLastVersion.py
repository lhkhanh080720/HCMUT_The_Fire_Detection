# ===============pyuic5 -x mainv1.ui -o mainv1.py===============
from libs import *
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication)
from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, Qt, QSize, QTimer, QTime, QDate, QObject, QEvent)
from PyQt5.QtGui import (QImage, QPixmap, QFont, QIcon, QColor)

class MAIN_HANDLE(QMainWindow):
    camID1 = "Cam White"
    cap1 = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    camID2 = "Cam Black"
    cap2 = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L2)

    #------for func Notice------
    timeOut = 3
    counterFire = 0
    notiFire = False
    noti0FireMo = False
    noti0Fire = False

    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        #------------------add feature------------------#
        self.Cam1 = Camera(MAIN_HANDLE.cap1, self.uic.labelText1, MAIN_HANDLE.camID1)    
        self.Cam2 = Camera(MAIN_HANDLE.cap2, self.uic.labelText2, MAIN_HANDLE.camID2)
        self.Cam1.update_frame()
        self.Cam2.update_frame()

        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.Cam1.update_frame)
        self.timer1.timeout.connect(self.Cam2.update_frame)
        self.timer1.timeout.connect(self.check_Fire)
        self.timer1.start(1)

        # Update CPU and T
        self.update_CPU()
        self.update_Temp()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_CPU)
        self.timer.timeout.connect(self.update_Temp)
        self.timer.start(5000)
    
    def check_Fire(self):
        if self.Cam1.flag or self.Cam2.flag:
            if not MAIN_HANDLE.notiFire:
                print("Detected the fire")
                MAIN_HANDLE.notiFire = True
                MAIN_HANDLE.noti0FireMo = False
                MAIN_HANDLE.noti0Fire = False
            MAIN_HANDLE.counterFire = time.time()
        elif not self.Cam1.flag and not self.Cam2.flag:
            if time.time() - MAIN_HANDLE.counterFire <= MAIN_HANDLE.timeOut:
                if not MAIN_HANDLE.noti0FireMo:
                    print("No Fire in the Frame")
                    MAIN_HANDLE.notiFire = False
                    MAIN_HANDLE.noti0FireMo = True
                    MAIN_HANDLE.noti0Fire = False
            else:
                if not MAIN_HANDLE.noti0Fire:
                    print("No Fire in the System")
                    MAIN_HANDLE.notiFire = False
                    MAIN_HANDLE.noti0FireMo = False
                    MAIN_HANDLE.noti0Fire = True           

    def clear(self): pass

    def closeEvent(self, event):
        ret = QMessageBox.information(self, "Quit Program", # title 
                                      "Are you sure to Quit?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.timer.stop()
            self.timer1.stop()
            event.accept()
        else:
            event.ignore()

    def update_CPU(self):
        per_cpu_percent = psutil.cpu_percent(percpu=True)
        for i, cpu_percent in enumerate(per_cpu_percent):
            if i == 0:
                self.uic.labelCPU1.setText("CPU1: " + str(cpu_percent) + "%")
            if i == 1:
                self.uic.labelCPU2.setText("CPU2: " + str(cpu_percent) + "%")
            if i == 2:
                self.uic.labelCPU3.setText("CPU3: " + str(cpu_percent) + "%")
            if i == 3:
                self.uic.labelCPU4.setText("CPU4: " + str(cpu_percent) + "%")

    def update_Temp(self):
        current_time = datetime.datetime.now().time()
        self.uic.labelREALTIME.setText("TIME = " + str(current_time.strftime("%H:%M:%S")))
        with open("/sys/devices/virtual/thermal/thermal_zone1/temp", "r") as temp_file:
            self.uic.labelTEMP1.setText("CPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone2/temp", "r") as temp_file:
            self.uic.labelTEMP2.setText("GPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone5/temp", "r") as temp_file:
            self.uic.labelTEMP3.setText("Thermal Fan: " + str(int(temp_file.read().strip())/1000))


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
