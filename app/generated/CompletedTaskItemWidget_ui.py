# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/views/CompletedTaskItemWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompletedTaskItemWidget(object):
    def setupUi(self, CompletedTaskItemWidget):
        CompletedTaskItemWidget.setObjectName("CompletedTaskItemWidget")
        CompletedTaskItemWidget.resize(417, 50)
        font = QtGui.QFont()
        font.setPointSize(10)
        CompletedTaskItemWidget.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(CompletedTaskItemWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_task_reopen = QtWidgets.QToolButton(CompletedTaskItemWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/new-48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_task_reopen.setIcon(icon)
        self.btn_task_reopen.setObjectName("btn_task_reopen")
        self.horizontalLayout.addWidget(self.btn_task_reopen)
        self.lbl_task_title = QtWidgets.QLabel(CompletedTaskItemWidget)
        self.lbl_task_title.setText("")
        self.lbl_task_title.setObjectName("lbl_task_title")
        self.horizontalLayout.addWidget(self.lbl_task_title)

        self.retranslateUi(CompletedTaskItemWidget)
        QtCore.QMetaObject.connectSlotsByName(CompletedTaskItemWidget)

    def retranslateUi(self, CompletedTaskItemWidget):
        _translate = QtCore.QCoreApplication.translate
        CompletedTaskItemWidget.setWindowTitle(_translate("CompletedTaskItemWidget", "Form"))
        self.btn_task_reopen.setText(_translate("CompletedTaskItemWidget", "..."))
