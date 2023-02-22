# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_interface.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1436, 574)
        MainWindow.setStyleSheet(u"*{\n"
"	border:none;\n"
"	background-color:transparent;\n"
"	background:transparent;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	color: #fff;\n"
"}\n"
"#centralwidget{\n"
"	background-color: #1f232a;\n"
"}\n"
"#menuFrame{\n"
"	background-color: #16191d;\n"
"}\n"
"#menuFrame menuBtn{\n"
"	text-align: left;\n"
"	padding: 5px 10px;\n"
"	boder-top-left-radius: 10px;\n"
"	boder-bottom-left-radius: 10px;\n"
"}\n"
"#centerMenuSubContainer{\n"
"	background-color: #2c313c;\n"
"}\n"
"#frame_4{\n"
"	background-color: #16191d;\n"
"	border-radius: 10px\n"
"}\n"
"#titleFrame{\n"
"	background-color: #2c313c;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.menuFrame = QFrame(self.centralwidget)
        self.menuFrame.setObjectName(u"menuFrame")
        self.menuFrame.setGeometry(QRect(5, 0, 105, 600))
        self.menuFrame.setFrameShape(QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QFrame.Raised)
        self.menuBtn = QPushButton(self.menuFrame)
        self.menuBtn.setObjectName(u"menuBtn")
        self.menuBtn.setGeometry(QRect(4, 52, 105, 50))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuBtn.sizePolicy().hasHeightForWidth())
        self.menuBtn.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.menuBtn.setFont(font)
        self.menuBtn.setLayoutDirection(Qt.LeftToRight)
        self.menuBtn.setStyleSheet(u"background-color: #1f232a;")
        icon = QIcon()
        icon.addFile(u":/icons/icons/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.menuBtn.setIcon(icon)
        self.menuBtn.setIconSize(QSize(24, 24))
        self.cam1Btn = QPushButton(self.menuFrame)
        self.cam1Btn.setObjectName(u"cam1Btn")
        self.cam1Btn.setGeometry(QRect(4, 106, 105, 50))
        self.cam1Btn.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/camera.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.cam1Btn.setIcon(icon1)
        self.cam1Btn.setIconSize(QSize(24, 24))
        self.cam2Btn = QPushButton(self.menuFrame)
        self.cam2Btn.setObjectName(u"cam2Btn")
        self.cam2Btn.setGeometry(QRect(4, 160, 105, 50))
        self.cam2Btn.setFont(font)
        self.cam2Btn.setIcon(icon1)
        self.cam2Btn.setIconSize(QSize(24, 24))
        self.label_8 = QLabel(self.menuFrame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(30, 3, 48, 48))
        self.label_8.setMinimumSize(QSize(20, 20))
        self.label_8.setPixmap(QPixmap(u":/image/logoBK.png"))
        self.label_8.setScaledContents(True)
        self.titleFrame = QFrame(self.centralwidget)
        self.titleFrame.setObjectName(u"titleFrame")
        self.titleFrame.setGeometry(QRect(110, 0, 1324, 50))
        self.titleFrame.setFrameShape(QFrame.StyledPanel)
        self.titleFrame.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.titleFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(600, 20, 191, 16))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_2.setFont(font1)
        self.label = QLabel(self.titleFrame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(560, 10, 31, 31))
        self.label.setMinimumSize(QSize(20, 20))
        self.label.setPixmap(QPixmap(u":/image/fire.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_7 = QLabel(self.titleFrame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(760, 10, 31, 31))
        self.label_7.setMinimumSize(QSize(20, 20))
        self.label_7.setPixmap(QPixmap(u":/image/fire.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(Qt.AlignCenter)
        self.mainFrame = QStackedWidget(self.centralwidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setGeometry(QRect(110, 50, 1324, 559))
        self.mainFrame.setStyleSheet(u"")
        self.homeF = QWidget()
        self.homeF.setObjectName(u"homeF")
        self.label_3 = QLabel(self.homeF)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 20, 640, 480))
        self.label_4 = QLabel(self.homeF)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(680, 20, 640, 480))
        self.mainFrame.addWidget(self.homeF)
        self.cam1F = QWidget()
        self.cam1F.setObjectName(u"cam1F")
        self.label_5 = QLabel(self.cam1F)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 20, 640, 480))
        self.mainFrame.addWidget(self.cam1F)
        self.cam2F = QWidget()
        self.cam2F.setObjectName(u"cam2F")
        self.label_6 = QLabel(self.cam2F)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 20, 640, 480))
        self.mainFrame.addWidget(self.cam2F)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuBtn.setText(QCoreApplication.translate("MainWindow", u"Home      ", None))
        self.cam1Btn.setText(QCoreApplication.translate("MainWindow", u"Camera 1", None))
        self.cam2Btn.setText(QCoreApplication.translate("MainWindow", u"Camera 2", None))
        self.label_8.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Fire Detection", None))
        self.label.setText("")
        self.label_7.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

