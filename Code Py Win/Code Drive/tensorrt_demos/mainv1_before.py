# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainv1.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1335, 658)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelText1 = QtWidgets.QLabel(self.centralwidget)
        self.labelText1.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.labelText1.setObjectName("labelText1")
        self.labelText2 = QtWidgets.QLabel(self.centralwidget)
        self.labelText2.setGeometry(QtCore.QRect(640, 0, 640, 480))
        self.labelText2.setObjectName("labelText2")
        self.labelCPU1 = QtWidgets.QLabel(self.centralwidget)
        self.labelCPU1.setGeometry(QtCore.QRect(10, 500, 221, 31))
        self.labelCPU1.setObjectName("labelCPU1")
        self.labelCPU2 = QtWidgets.QLabel(self.centralwidget)
        self.labelCPU2.setGeometry(QtCore.QRect(10, 530, 221, 31))
        self.labelCPU2.setObjectName("labelCPU2")
        self.labelCPU4 = QtWidgets.QLabel(self.centralwidget)
        self.labelCPU4.setGeometry(QtCore.QRect(10, 590, 221, 31))
        self.labelCPU4.setObjectName("labelCPU4")
        self.labelCPU3 = QtWidgets.QLabel(self.centralwidget)
        self.labelCPU3.setGeometry(QtCore.QRect(10, 560, 221, 31))
        self.labelCPU3.setObjectName("labelCPU3")
        self.labelTEMP2 = QtWidgets.QLabel(self.centralwidget)
        self.labelTEMP2.setGeometry(QtCore.QRect(280, 540, 221, 31))
        self.labelTEMP2.setObjectName("labelTEMP2")
        self.labelTEMP3 = QtWidgets.QLabel(self.centralwidget)
        self.labelTEMP3.setGeometry(QtCore.QRect(280, 570, 221, 31))
        self.labelTEMP3.setObjectName("labelTEMP3")
        self.labelTEMP1 = QtWidgets.QLabel(self.centralwidget)
        self.labelTEMP1.setGeometry(QtCore.QRect(280, 510, 221, 31))
        self.labelTEMP1.setObjectName("labelTEMP1")
        self.labelREALTIME = QtWidgets.QLabel(self.centralwidget)
        self.labelREALTIME.setGeometry(QtCore.QRect(580, 530, 221, 31))
        self.labelREALTIME.setObjectName("labelREALTIME")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1335, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Systerm Detect Fire"))
        self.labelText1.setText(_translate("MainWindow", "TextLabel"))
        self.labelText2.setText(_translate("MainWindow", "TextLabel"))
        self.labelCPU1.setText(_translate("MainWindow", "TextLabel"))
        self.labelCPU2.setText(_translate("MainWindow", "TextLabel"))
        self.labelCPU4.setText(_translate("MainWindow", "TextLabel"))
        self.labelCPU3.setText(_translate("MainWindow", "TextLabel"))
        self.labelTEMP2.setText(_translate("MainWindow", "TextLabel"))
        self.labelTEMP3.setText(_translate("MainWindow", "TextLabel"))
        self.labelTEMP1.setText(_translate("MainWindow", "TextLabel"))
        self.labelREALTIME.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

