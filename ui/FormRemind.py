# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormRemind.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_Remind(object):

    def updateRemind(self):
        sder = self.parent.sender()
        if sder == self.checkBox_popup:
            self.params['popup'] = self.checkBox_popup.isChecked()
        elif sder == self.checkBox_music:
            self.params['music'] = self.checkBox_music.isChecked()

    def setParam(self, params):
        self.params = params
        self.checkBox_popup.setChecked(params['popup'])
        self.checkBox_music.setChecked(params['music'])

    def __init__(self, parent):
        self.parent = parent
        self.setupUi(parent)

    def setupUi(self, Form_Remind):
        Form_Remind.setObjectName("Form_Remind")
        Form_Remind.resize(291, 80)
        Form_Remind.setMinimumSize(QtCore.QSize(291, 80))
        Form_Remind.setMaximumSize(QtCore.QSize(291, 80))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form_Remind)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_popup = QtWidgets.QCheckBox(Form_Remind)
        self.checkBox_popup.setObjectName("checkBox_popup")
        self.horizontalLayout.addWidget(self.checkBox_popup)
        self.checkBox_music = QtWidgets.QCheckBox(Form_Remind)
        self.checkBox_music.setObjectName("checkBox_music")
        self.horizontalLayout.addWidget(self.checkBox_music)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBox_3 = QtWidgets.QCheckBox(Form_Remind)
        self.checkBox_3.setEnabled(False)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout.addWidget(self.checkBox_3)

        self.retranslateUi(Form_Remind)
        QtCore.QMetaObject.connectSlotsByName(Form_Remind)

    def retranslateUi(self, Form_Remind):
        _translate = QtCore.QCoreApplication.translate
        Form_Remind.setWindowTitle(_translate("Form_Remind", "提醒方式"))
        self.checkBox_popup.setText(_translate("Form_Remind", "弹窗提醒"))
        self.checkBox_music.setText(_translate("Form_Remind", "铃声提醒"))
        self.checkBox_3.setText(_translate("Form_Remind", "短信提醒"))

