from functools import partial
from threading import Lock
import numpy as np
import time
import cv2
import os
from libs import *

from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication)
from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, Qt, QSize, QTimer, QTime, QDate, QObject, QEvent)
from PyQt5.QtGui import (QImage, QPixmap, QFont, QIcon, QColor)

numClass = 2     #The numbers of classes
cls_dict = get_cls_dict(numClass)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO('obj', numClass, False)
# -----------------------------------------
class Thread(QtCore.QThread):
# When use the func Thread, return var "imgSignal"  
    imgSignal = pyqtSignal(np.ndarray, int, bool)

    def __init__(self, parent, cam_link, index):
        super().__init__()
        self._lock = Lock()
        self.p = parent
        self.cam_link = cam_link
        self.index = index

    def run(self):
        with self._lock:
        # self._lock.acquire()
            cap = cv2.VideoCapture(self.cam_link, cv2.CAP_V4L2)
            while cap.isOpened():
                has, img = cap.read()
                if not has: 
                    break # video has limit
                self.imgSignal.emit(img, self.index, True)
                # cv2.waitKey(capture_delay) & 0xFF # works, dont set 1, will crash, too fast

    def stop(self):
        self._lock.release()
        cv2.destroyAllWindows()
        self.cap.release()

# -----------------------------------------
class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        #===================Add=================#
        self.cam_links = []
        self.cam_links.append('/dev/video0')
        self.cam_links.append('/dev/video1')

        self.threads = []
        for index, cam_link in enumerate(self.cam_links):
            #Thread-----------------------
            th = Thread(self, cam_link, index)
            th.imgSignal.connect(self.getImg)  # Function of Thread: def getImg()
            self.threads.append(th)
        
        self.refreshThread()
        # Timer Auto Restart threads 
        self.timer_th = QTimer(self)
        self.timer_th.timeout.connect(self.refreshThread)
        self.timer_th.start(60000) # 60 secs
        #===================Study=================#
        #Call Button: self.uic.Button_start_2.clicked...
    @pyqtSlot(np.ndarray, int, bool)
    def getImg(self, img, index):
        global trt_yolo, vis
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.detectObjects(trt_yolo, vis, img)
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
        if index == 0:
            self.uic.labelText1.setPixmap(QPixmap.fromImage(img))
        elif index == 1:
            self.uic.labelText2.setPixmap(QPixmap.fromImage(img))

    def detectObjects(self, trt_yolo, vis, frame):  
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

    def clear(self): pass

    def closeEvent(self, event):
        ret = QMessageBox.information(self, "Quit Program", # title 
                                      "Are you sure to Quit?", # content
        QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.timer_th.stop()
            for th in self.threads:
                th.stop()
            event.accept()
        else:
            event.ignore()

    def refreshThread(self):
        for th in self.threads:
            th.start()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())