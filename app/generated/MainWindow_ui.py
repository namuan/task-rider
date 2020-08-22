# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/views/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(389, 818)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTimer = QtWidgets.QLCDNumber(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTimer.sizePolicy().hasHeightForWidth())
        self.lblTimer.setSizePolicy(sizePolicy)
        self.lblTimer.setObjectName("lblTimer")
        self.horizontalLayout.addWidget(self.lblTimer)
        self.btnPause = QtWidgets.QPushButton(self.frame_2)
        self.btnPause.setObjectName("btnPause")
        self.horizontalLayout.addWidget(self.btnPause)
        self.btnReset = QtWidgets.QPushButton(self.frame_2)
        self.btnReset.setObjectName("btnReset")
        self.horizontalLayout.addWidget(self.btnReset)
        self.verticalLayout.addWidget(self.frame_2)
        self.lst_tasks = QtWidgets.QListWidget(self.centralwidget)
        self.lst_tasks.setObjectName("lst_tasks")
        self.verticalLayout.addWidget(self.lst_tasks)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txt_task_title = QtWidgets.QLineEdit(self.frame)
        self.txt_task_title.setObjectName("txt_task_title")
        self.horizontalLayout_2.addWidget(self.txt_task_title)
        self.btn_add_task = QtWidgets.QToolButton(self.frame)
        self.btn_add_task.setObjectName("btn_add_task")
        self.horizontalLayout_2.addWidget(self.btn_add_task)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TaskRider"))
        self.btnPause.setText(_translate("MainWindow", "Pause"))
        self.btnReset.setText(_translate("MainWindow", "Reset"))
        self.btn_add_task.setText(_translate("MainWindow", "+"))
