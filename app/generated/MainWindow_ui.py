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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setContentsMargins(12, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_timer_value = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_timer_value.sizePolicy().hasHeightForWidth())
        self.lbl_timer_value.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_timer_value.setFont(font)
        self.lbl_timer_value.setAutoFillBackground(False)
        self.lbl_timer_value.setObjectName("lbl_timer_value")
        self.horizontalLayout.addWidget(self.lbl_timer_value)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_toggle_timer = QtWidgets.QPushButton(self.frame_3)
        self.btn_toggle_timer.setObjectName("btn_toggle_timer")
        self.verticalLayout_2.addWidget(self.btn_toggle_timer)
        self.btn_reset_timer = QtWidgets.QPushButton(self.frame_3)
        self.btn_reset_timer.setObjectName("btn_reset_timer")
        self.verticalLayout_2.addWidget(self.btn_reset_timer)
        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame_2)
        self.lst_tasks = QtWidgets.QListWidget(self.centralwidget)
        self.lst_tasks.setObjectName("lst_tasks")
        self.verticalLayout.addWidget(self.lst_tasks)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txt_task_title = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.txt_task_title.setFont(font)
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
        self.lbl_timer_value.setText(_translate("MainWindow", "10"))
        self.btn_toggle_timer.setText(_translate("MainWindow", "Start"))
        self.btn_reset_timer.setText(_translate("MainWindow", "Reset"))
        self.btn_add_task.setText(_translate("MainWindow", "+"))
