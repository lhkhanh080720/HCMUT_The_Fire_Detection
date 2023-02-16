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
        MainWindow.resize(1300, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelText1 = QtWidgets.QLabel(self.centralwidget)
        self.labelText1.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.labelText1.setObjectName("labelText1")
        self.labelText2 = QtWidgets.QLabel(self.centralwidget)
        self.labelText2.setGeometry(QtCore.QRect(643, 0, 640, 480))
        self.labelText2.setObjectName("labelText2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 20))
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


