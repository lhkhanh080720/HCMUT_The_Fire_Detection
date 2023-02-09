from functools import partial
from threading import Lock
import numpy as np
import time
import cv2
import os

from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication)
from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, Qt, QSize, QTimer, QTime, QDate, QObject, QEvent)
from PyQt5.QtGui import (QImage, QPixmap, QFont, QIcon, QColor)

os.environ['OPENCV_VIDEOIO_DEBUG'] = '1'
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

# pip uninstall cryptography -y 
# pip install --upgrade cryptography
# pip install pywin32-ctypes
# pip install pyinstaller

# create single installer.exe --onefile IS NOT WORKING because pywin32
# pyinstaller --onefile --windowed --icon icon.png multi_cam_4x4.py

# create directory installer for instead
# pyinstaller --onedir --windowed --icon icon.png multi_cam_4x4.py

# without icon (works), check 'dist/'
# pyinstaller --onefile --windowed multi_cam_4x4.py
# OR
# pyinstaller --onedir --windowed multi_cam_4x4.py


# width, height = 480*4, 640*4
width, height = 480*6, 270*6
# capture_delay = 10000 # 10 seconds
capture_delay = 100 # 100ms , Dont set 1, too fast, crash


# -----------------------------------------
class Thread(QThread):
	imgSignal = pyqtSignal(np.ndarray, int, bool)

	def __init__(self, parent, cam_link, index):
		QThread.__init__(self, parent)
		self._lock = Lock()
		self.p = parent
		self.cam_link = cam_link
		self.index = index

	def run(self):
		# self._lock.acquire()
		with self._lock:
			cap = cv2.VideoCapture(self.cam_link)
			while cap.isOpened():
				has, img = cap.read()
				if not has: break # video has limit
				# img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
				self.imgSignal.emit(img, self.index, True)
				cv2.waitKey(capture_delay) & 0xFF # works, dont set 1, will crash, too fast
			
			img = np.zeros((height,width,3), np.uint8)
			self.imgSignal.emit(img, self.index, False)
			cv2.waitKey(capture_delay) & 0xFF # works, dont set 1, will crash, too fast

	# def stop(self):
	# 	self._lock.release()
	# 	cv2.destroyAllWindows()
	# 	self.cap.release()


# -----------------------------------------
# https://wiki.python.org/moin/PyQt/Making%20non-clickable%20widgets%20clickable
def clickable(widget):
	class Filter(QObject):
		clicked = pyqtSignal()
		def eventFilter(self, obj, event):
			if obj == widget:
				if event.type() == QEvent.MouseButtonRelease:
					self.clicked.emit()
					return True
			return False

	filter = Filter(widget)
	widget.installEventFilter(filter)
	return filter.clicked


# -----------------------------------------
class NewWindow(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.p = parent
		self.index = None

		self.label = QLabel()
		self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		self.label.setScaledContents(True)
		self.label.setFont(QFont("Times", 30))
		self.label.setStyleSheet(
			"color: rgb(255,0,255);"
			"background-color: rgb(0,0,0);"
			"qproperty-alignment: AlignCenter;")

		layout = QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		# layout.setSpacing(2)
		layout.addWidget(self.label)
		self.setLayout(layout)
		self.setWindowTitle('Camera {}'.format(self.index))

	def sizeHint(self):
		return QSize(width//4, height//4)

	def resizeEvent(self, event):
		self.update()

	def close(self):
		self.accept()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.accept()


# -----------------------------------------
class TableStatus(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.p = parent

		# Table Widget ---------------
		# https://pythonspot.com/pyqt5-table/
		# https://freeprog.tistory.com/333
		# https://likegeeks.com/pyqt5-tutorial/
		self.table = QTableWidget()
		self.table.setSelectionMode(QAbstractItemView.SingleSelection)
		# self.table.setSelectionMode(QAbstractItemView.MultiSelection)
		self.table.setRowCount(len(self.p.cam_links))
		self.table.setColumnCount(2)
		self.table.setHorizontalHeaderLabels(('ID', 'Status')) # NOTE: after setColumnsCount()
		self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
		self.table.horizontalHeader().setStretchLastSection(True)
		self.table.horizontalHeader().setFont(QFont("Times", 13))
		# self.table.verticalHeader().setStretchLastSection(True)
		# self.table.setSortingEnabled(True)
		style = "::section {""background-color: darkcyan; color: rgb(230,230,230);}"
		self.table.horizontalHeader().setStyleSheet(style)
		self.table.verticalHeader().setStyleSheet(style)
		# self.table.setShowGrid(True)

		self.table.resizeColumnsToContents()
		self.table.resizeRowsToContents()
		# self.table.sortByColumn(0, Qt.AscendingOrder)
		self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) # Read-Only

		# self.table.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		layout = QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		# layout.setSpacing(2)
		layout.addWidget(self.table)
		self.setLayout(layout)
		self.setWindowTitle('Camera Status')

	def sizeHint(self):
		return QSize(width//4, height//4)

	def resizeEvent(self, event):
		self.update()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.accept()
			# self.table.clear()
			self.p.buttonStatus.setStyleSheet(
				"color: rgb(127,255,127); background-color: rgb(0,0,0);")

	def closeEvent(self, event):
		event.accept()
		self.p.buttonStatus.setStyleSheet(
			"color: rgb(127,255,127); background-color: rgb(0,0,0);")

	def updateTable(self, cam_links, actives):
		for i, (cam_link, active) in enumerate(zip(cam_links, actives)):
			# simple
			# self.table.setItem(i,0, QTableWidgetItem(str(cam_link))) # rowi,col0
			# self.table.setItem(i,1, QTableWidgetItem(str(active))) # rowi,col1

			# complex
			col1 = QTableWidgetItem(str(cam_link))
			col1.setFont(QFont("Times", 13))
			col1.setForeground(QColor(127,255,255))				# fg
			if i % 2 == 0: col1.setBackground(QColor(0,0,0))	# bg
			else: col1.setBackground(QColor(61,53,53))			# bg
			col1.setTextAlignment(Qt.AlignLeft)
			self.table.setItem(i,0, col1)

			col2 = QTableWidgetItem(str(active))
			col2.setFont(QFont("Times", 13))
			if active: col2.setForeground(QColor(127,255,127))	# fg
			else: col2.setForeground(QColor(255,127,127))		# fg
			if i % 2 == 0: col2.setBackground(QColor(0,0,0))	# bg
			else: col2.setBackground(QColor(61,53,53))			# bg
			col2.setTextAlignment(Qt.AlignCenter)
			self.table.setItem(i,1, col2)

		self.table.resizeColumnsToContents()
		self.table.resizeRowsToContents()
		# self.resize(QSize(width//4, height//4))

		self.p.buttonStatus.setStyleSheet(
			"color: rgb(255,127,127); background-color: rgb(0,0,0);")


# -----------------------------------------
class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()

		# -----------------------------------
		# self.cam_links = list(range(0,16))

		self.cam_links = []
		self.cam_links.append(0)
		self.cam_links.append(1)
		self.cam_links.append('video\\challenge.mp4')
		self.cam_links.append(3)
		self.cam_links.append('video\\input.mp4')
		self.cam_links.extend(list(range(5,11)))
		self.cam_links.append('video\\testvideo2.mp4')
		self.cam_links.append(12)
		self.cam_links.append('video\\traffic_sign_detection_POV 2019-04-29.mp4')
		self.cam_links.append(14)
		self.cam_links.append(15)

		# self.cam_links = []
		# self.cam_links.append(0)
		# self.cam_links.append(1)
		# self.cam_links.append('data\\video\\ae5a40dfe1c9e5d0326fe5666d4a176f.mp4')
		# self.cam_links.append(3)
		# self.cam_links.append('data\\video\\challenge.mp4')
		# self.cam_links.extend(list(range(5,11)))
		# self.cam_links.append('data\\video\\d0543lj6z66.p712.1.mp4')
		# self.cam_links.append(12)
		# self.cam_links.append('data\\video\\input.mp4')
		# self.cam_links.append(14)
		# self.cam_links.append(15)
		# -----------------------------------

		self.actives = [False for i in range(len(self.cam_links))]

		layout = QGridLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(2)

		self.labels = []
		self.threads = []
		for index, cam_link in enumerate(self.cam_links):

			# Thread ---------------------
			th = Thread(self, cam_link, index)
			th.imgSignal.connect(self.getImg)
			self.threads.append(th)

			# Screen ---------------------
			label = QLabel()
			label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
			label.setScaledContents(True)
			label.setFont(QFont("Times", 30))
			label.setStyleSheet(
				"color: rgb(255,0,255);"
				"background-color: rgb(0,0,0);"
				"qproperty-alignment: AlignCenter;")

			# https://wiki.python.org/moin/PyQt/Making%20non-clickable%20widgets%20clickable
			clickable(label).connect(partial(self.showCam, index))

			self.labels.append(label)

			# https://www.learnpyqt.com/courses/start/layouts/
			if index == 0:
				layout.addWidget(label, 0,0) # row1,col1
			elif index == 1:
				layout.addWidget(label, 0,1) # row1,col2
			elif index == 2:
				layout.addWidget(label, 0,2) # row1,col3
			elif index == 3:
				layout.addWidget(label, 0,3) # row1,col4

			elif index == 4:
				layout.addWidget(label, 1,0) # row2,col1
			elif index == 5:
				layout.addWidget(label, 1,1) # row2,col2
			elif index == 6:
				layout.addWidget(label, 1,2) # row2,col3
			elif index == 7:
				layout.addWidget(label, 1,3) # row2,col4

			elif index == 8:
				layout.addWidget(label, 2,0) # row3,col1
			elif index == 9:
				layout.addWidget(label, 2,1) # row3,col2
			elif index == 10:
				layout.addWidget(label, 2,2) # row3,col3
			elif index == 11:
				layout.addWidget(label, 2,3) # row3,col4

			elif index == 12:
				layout.addWidget(label, 3,0) # row4,col1
			elif index == 13:
				layout.addWidget(label, 3,1) # row4,col2
			elif index == 14:
				layout.addWidget(label, 3,2) # row4,col3
			elif index == 15:
				layout.addWidget(label, 3,3) # row4,col4
			else:
				raise ValueError("n Camera != rows/cols")


		# Button Detection -----------
		self.buttonDetection = QPushButton('Spills Detection!')
		self.buttonDetection.setFont(QFont("Times", 30))
		self.buttonDetection.setStyleSheet(
			"color: rgb(255,127,127);"
			"background-color: rgb(0,0,0);")
		self.buttonDetection.clicked.connect(self.buttonDetectionClicked)
		# layout.addWidget(self.buttonDetection, 4,0,1,4)
		# layout.addWidget(self.buttonDetection, 4,0,1,2)
		layout.addWidget(self.buttonDetection, 4,0,1,2)

		# Button Status ---------------
		self.buttonStatus = QPushButton('Status?')
		self.buttonStatus.setFont(QFont("Times", 30))
		self.buttonStatus.setStyleSheet(
			"color: rgb(127,255,127);"
			"background-color: rgb(0,0,0);")
		self.buttonStatus.clicked.connect(self.buttonStatusClicked)
		layout.addWidget(self.buttonStatus, 4,2,1,1)

		# Button Refresh --------------
		self.buttonRefresh = QPushButton('Refresh...')
		self.buttonRefresh.setFont(QFont("Times", 30))
		self.buttonRefresh.setStyleSheet(
			"color: rgb(127,255,255);"
			"background-color: rgb(0,0,0);")
		self.buttonRefresh.clicked.connect(self.buttonRefreshClicked)
		layout.addWidget(self.buttonRefresh, 4,3,1,1)


		# Time Screen ----------------
		timer = QTimer(self)
		timer.timeout.connect(self.showTime)
		timer.start(1000)
		self.showTime()

		# Timer Auto Restart threads -
		timer_th = QTimer(self)
		timer_th.timeout.connect(self.refreshThread)
		timer_th.start(60000) # 60 secs

		# -----------------------------
		self.setLayout(layout)

		self.setWindowTitle("CCTV")
		self.setWindowIcon(QIcon('icon.png'))
		# left, top = 0, 0
		# self.setGeometry(left, top, width, height)

		self.newWindow = NewWindow(self)
		self.tableStatus = TableStatus(self)

		self.refreshThread()


	def sizeHint(self):
		return QSize(width, height)

	def resizeEvent(self, event):
		self.update()

	@pyqtSlot(np.ndarray, int, bool)
	def getImg(self, img, index, active):
		self.actives[index] = active
		if active:
			if self.buttonDetection.text() == "Spills Detection!":
				# Detection all objects
				pass
			else:
				# Detection spills objects
				pass

			# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			# img = QImage(img.data, width, height, 3*width, QImage.Format_RGB888)
			img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888).rgbSwapped()
			self.labels[index].setPixmap(QPixmap.fromImage(img))

			if index == self.newWindow.index:
				self.newWindow.label.setPixmap(QPixmap.fromImage(img))
			# QApplication.processEvents()
		else:
			# threads[index].exec_()
			# QApplication.processEvents()
			# Close the big screen if movie end
			if index == self.newWindow.index:
				self.newWindow.close()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
		elif event.key() == Qt.Key_Space:
			self.clear()

	def clear(self): pass

	def closeEvent(self, event):
		ret = QMessageBox.information(self,
			"Quit CCTV", # title
			"Are you sure to Quit?", # content
			QMessageBox.Yes | QMessageBox.No)
		if ret == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def showTime(self):
		# Time
		time = QTime.currentTime()
		textTime = time.toString('hh:mm:ss')
		# Date
		date = QDate.currentDate()
		textDate = date.toString('ddd, MMMM d')

		text = "{}\n{}".format(textTime, textDate)
		# label.setText(text)

		for index, (label, active) in enumerate(zip(self.labels, self.actives)):
			if not active:
				text_ = "Camera {}\n".format(index) + text
				label.setText(text_)


	def showCam(self, index):
		self.newWindow.index = index
		if not self.actives[index]:
			text_ = "Camera {}\nNot active!".format(index)
			self.newWindow.label.setText(text_)
		self.newWindow.setWindowTitle('Camera {}'.format(index))
		self.newWindow.show()

	def buttonDetectionClicked(self):
		text = self.buttonDetection.text()
		if text == "Spills Detection!":
			self.buttonDetection.setText("All Detection!")
		else:
			self.buttonDetection.setText("Spills Detection!")

	def buttonStatusClicked(self):
		self.tableStatus.updateTable(self.cam_links, self.actives)
		# self.tableStatus.close()
		self.tableStatus.hide()
		self.tableStatus.show()

	def buttonRefreshClicked(self):
		self.buttonRefresh.setEnabled(False)
		self.refreshThread()
		self.buttonRefresh.setEnabled(True)

	def refreshThread(self):
		# for th in self.threads:
		# 	# th.terminate()
		# 	th.stop()
		for th in self.threads:
			th.start()





if __name__ == '__main__':

	import sys

	app = QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())