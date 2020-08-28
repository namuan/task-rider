# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/views/TaskItemWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TaskItemWidget(object):
    def setupUi(self, TaskItemWidget):
        TaskItemWidget.setObjectName("TaskItemWidget")
        TaskItemWidget.resize(417, 50)
        font = QtGui.QFont()
        font.setPointSize(10)
        TaskItemWidget.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(TaskItemWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_task_done = QtWidgets.QToolButton(TaskItemWidget)
        self.btn_task_done.setObjectName("btn_task_done")
        self.horizontalLayout.addWidget(self.btn_task_done)
        self.lbl_task_title = QtWidgets.QLabel(TaskItemWidget)
        self.lbl_task_title.setText("")
        self.lbl_task_title.setObjectName("lbl_task_title")
        self.horizontalLayout.addWidget(self.lbl_task_title)

        self.retranslateUi(TaskItemWidget)
        QtCore.QMetaObject.connectSlotsByName(TaskItemWidget)

    def retranslateUi(self, TaskItemWidget):
        _translate = QtCore.QCoreApplication.translate
        TaskItemWidget.setWindowTitle(_translate("TaskItemWidget", "Form"))
        self.btn_task_done.setText(_translate("TaskItemWidget", "..."))
