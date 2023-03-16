# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_interface.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1436, 561)
        MainWindow.setStyleSheet("*{\n"
"    border:none;\n"
"    background-color:transparent;\n"
"    background:transparent;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"    color: #fff;\n"
"}\n"
"#centralwidget{\n"
"    background-color: #1f232a;\n"
"}\n"
"#menuFrame{\n"
"    background-color: #16191d;\n"
"}\n"
"#menuFrame menuBtn{\n"
"    text-align: left;\n"
"    padding: 5px 10px;\n"
"    boder-top-left-radius: 10px;\n"
"    boder-bottom-left-radius: 10px;\n"
"}\n"
"#centerMenuSubContainer{\n"
"    background-color: #2c313c;\n"
"}\n"
"#frame_4{\n"
"    background-color: #16191d;\n"
"    border-radius: 10px\n"
"}\n"
"#titleFrame{\n"
"    background-color: #2c313c;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.menuFrame = QtWidgets.QFrame(self.centralwidget)
        self.menuFrame.setGeometry(QtCore.QRect(0, 0, 105, 600))
        self.menuFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menuFrame.setObjectName("menuFrame")
        self.menuBtn = QtWidgets.QPushButton(self.menuFrame)
        self.menuBtn.setGeometry(QtCore.QRect(4, 52, 105, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuBtn.sizePolicy().hasHeightForWidth())
        self.menuBtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.menuBtn.setFont(font)
        self.menuBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menuBtn.setStyleSheet("background-color: #1f232a;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/home.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuBtn.setIcon(icon)
        self.menuBtn.setIconSize(QtCore.QSize(24, 24))
        self.menuBtn.setObjectName("menuBtn")
        self.cam1Btn = QtWidgets.QPushButton(self.menuFrame)
        self.cam1Btn.setGeometry(QtCore.QRect(4, 106, 105, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cam1Btn.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/camera.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cam1Btn.setIcon(icon1)
        self.cam1Btn.setIconSize(QtCore.QSize(24, 24))
        self.cam1Btn.setObjectName("cam1Btn")
        self.cam2Btn = QtWidgets.QPushButton(self.menuFrame)
        self.cam2Btn.setGeometry(QtCore.QRect(4, 160, 105, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.cam2Btn.setFont(font)
        self.cam2Btn.setIcon(icon1)
        self.cam2Btn.setIconSize(QtCore.QSize(24, 24))
        self.cam2Btn.setObjectName("cam2Btn")
        self.label_8 = QtWidgets.QLabel(self.menuFrame)
        self.label_8.setGeometry(QtCore.QRect(30, 3, 48, 48))
        self.label_8.setMinimumSize(QtCore.QSize(20, 20))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap(":/image/logoBK.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.titleFrame = QtWidgets.QFrame(self.centralwidget)
        self.titleFrame.setGeometry(QtCore.QRect(105, 0, 1344, 50))
        self.titleFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.titleFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.titleFrame.setObjectName("titleFrame")
        self.label_2 = QtWidgets.QLabel(self.titleFrame)
        self.label_2.setGeometry(QtCore.QRect(600, 20, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.titleFrame)
        self.label.setGeometry(QtCore.QRect(560, 10, 31, 31))
        self.label.setMinimumSize(QtCore.QSize(20, 20))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/image/fire.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_7 = QtWidgets.QLabel(self.titleFrame)
        self.label_7.setGeometry(QtCore.QRect(760, 10, 31, 31))
        self.label_7.setMinimumSize(QtCore.QSize(20, 20))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/image/fire.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.mainFrame = QtWidgets.QStackedWidget(self.centralwidget)
        self.mainFrame.setGeometry(QtCore.QRect(105, 50, 1344, 559))
        self.mainFrame.setStyleSheet("")
        self.mainFrame.setObjectName("mainFrame")
        self.homeF = QtWidgets.QWidget()
        self.homeF.setObjectName("homeF")
        self.label_3 = QtWidgets.QLabel(self.homeF)
        self.label_3.setGeometry(QtCore.QRect(15, 15, 640, 480))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.homeF)
        self.label_4.setGeometry(QtCore.QRect(675, 15, 640, 480))
        self.label_4.setObjectName("label_4")
        self.mainFrame.addWidget(self.homeF)
        self.cam1F = QtWidgets.QWidget()
        self.cam1F.setObjectName("cam1F")
        self.label_5 = QtWidgets.QLabel(self.cam1F)
        self.label_5.setGeometry(QtCore.QRect(15, 15, 640, 480))
        self.label_5.setObjectName("label_5")
        self.mainFrame.addWidget(self.cam1F)
        self.cam2F = QtWidgets.QWidget()
        self.cam2F.setObjectName("cam2F")
        self.label_6 = QtWidgets.QLabel(self.cam2F)
        self.label_6.setGeometry(QtCore.QRect(15, 15, 640, 480))
        self.label_6.setObjectName("label_6")
        self.mainFrame.addWidget(self.cam2F)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.mainFrame.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuBtn.setText(_translate("MainWindow", "Home      "))
        self.cam1Btn.setText(_translate("MainWindow", "Camera 1"))
        self.cam2Btn.setText(_translate("MainWindow", "Camera 2"))
        self.label_2.setText(_translate("MainWindow", "Fire Detection"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))

import GUI.resource_rc



