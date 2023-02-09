# ===============pyuic5 -x mainv1.ui -o mainv1.py===============
from libs import *
from threading import Lock

class MAIN_HANDLE(Ui_MainWindow):
    camera_id1 = "/dev/video0"
    cap1 = cv2.VideoCapture(camera_id1, cv2.CAP_V4L2)
    camera_id2 = "/dev/video1"
    cap2 = cv2.VideoCapture(camera_id2, cv2.CAP_V4L2)
    numClass = 2     #The numbers of classes
    cls_dict = get_cls_dict(numClass)
    vis = BBoxVisualization(cls_dict)
    trt_yolo = TrtYOLO('obj', numClass, False)
    camID1 = "White"
    camID2 = "Black"
    def __init__(self):
        self.setupUi(MainWindow)

        #------------------add feature------------------#
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.update_frame1)
        self.timer1.timeout.connect(self.update_frame2)
        self.timer1.start(1)
        MainWindow.closeEvent = self.closeEvent

        # Update CPU and T
        self.update_CPU()
        self.update_Temp()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_CPU)
        self.timer.timeout.connect(self.update_Temp)
        self.timer.start(5000)

        #Flag "Fire"
        self.fire = False
        self.counter = 0  #Time to end notification

    def update_frame1(self):
        ret, frame = MAIN_HANDLE.cap1.read()
        self.detectObjects(MAIN_HANDLE.trt_yolo, MAIN_HANDLE.vis, frame, MAIN_HANDLE.camID1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.labelText1.setPixmap(QPixmap.fromImage(image))
    
    def update_frame2(self):
        ret, frame = MAIN_HANDLE.cap2.read()
        self.detectObjects(MAIN_HANDLE.trt_yolo, MAIN_HANDLE.vis, frame, MAIN_HANDLE.camID2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.labelText2.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.timer.stop()
        self.timer1.stop()
        event.accept()

    def update_CPU(self):
        per_cpu_percent = psutil.cpu_percent(percpu=True)
        for i, cpu_percent in enumerate(per_cpu_percent):
            if i == 0:
                self.labelCPU1.setText("CPU1: " + str(cpu_percent) + "%")
            if i == 1:
                self.labelCPU2.setText("CPU2: " + str(cpu_percent) + "%")
            if i == 2:
                self.labelCPU3.setText("CPU3: " + str(cpu_percent) + "%")
            if i == 3:
                self.labelCPU4.setText("CPU4: " + str(cpu_percent) + "%")

    def update_Temp(self):
        current_time = datetime.datetime.now().time()
        self.labelREALTIME.setText("TIME = " + str(current_time.strftime("%H:%M:%S")))
        with open("/sys/devices/virtual/thermal/thermal_zone1/temp", "r") as temp_file:
            self.labelTEMP1.setText("CPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone2/temp", "r") as temp_file:
            self.labelTEMP2.setText("GPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone5/temp", "r") as temp_file:
            self.labelTEMP3.setText("Thermal Fan: " + str(int(temp_file.read().strip())/1000))

    def detectObjects(self, trt_yolo, vis, frame, camID):  
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
            
            #Detected the fire
            self.fire = True
            print(camID + " Detect the Fire")
            self.counter = time.time()
        if self.fire:
            if time.time() - self.counter >= 5:
                self.fire = False
                print(camID + " Done!")

            else:
                print(camID + " Timer ==> 5s")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MAIN_HANDLE()
    MainWindow.show()
    sys.exit(app.exec_())
