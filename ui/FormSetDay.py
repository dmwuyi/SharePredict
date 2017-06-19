# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FormSetDay.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_setDay(object):

    def setParams(self, params):
        self.spinBox_5.setValue(params['day5'])
        self.spinBox_15.setValue(params['day15'])
        self.spinBox_30.setValue(params['day30'])
        self.spinBox_60.setValue(params['day60'])

    def __init__(self, parent):
        self.parent = parent
        self.setupUi(parent)

    def setupUi(self, Form_setDay):
        Form_setDay.setObjectName("Form_setDay")
        Form_setDay.resize(288, 100)
        Form_setDay.setMinimumSize(QtCore.QSize(288, 100))
        Form_setDay.setMaximumSize(QtCore.QSize(288, 100))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form_setDay)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form_setDay)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox_5 = QtWidgets.QSpinBox(Form_setDay)
        self.spinBox_5.setObjectName("spinBox_5")
        self.horizontalLayout.addWidget(self.spinBox_5)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form_setDay)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_15 = QtWidgets.QSpinBox(Form_setDay)
        self.spinBox_15.setObjectName("spinBox_15")
        self.horizontalLayout_2.addWidget(self.spinBox_15)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Form_setDay)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.spinBox_30 = QtWidgets.QSpinBox(Form_setDay)
        self.spinBox_30.setObjectName("spinBox_30")
        self.horizontalLayout_4.addWidget(self.spinBox_30)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(Form_setDay)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.spinBox_60 = QtWidgets.QSpinBox(Form_setDay)
        self.spinBox_60.setObjectName("spinBox_60")
        self.horizontalLayout_3.addWidget(self.spinBox_60)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.retranslateUi(Form_setDay)
        QtCore.QMetaObject.connectSlotsByName(Form_setDay)

    def retranslateUi(self, Form_setDay):
        _translate = QtCore.QCoreApplication.translate
        Form_setDay.setWindowTitle(_translate("Form_setDay", "不同周期数据天数"))
        self.label.setText(_translate("Form_setDay", "5分钟"))
        self.label_2.setText(_translate("Form_setDay", "15分钟"))
        self.label_3.setText(_translate("Form_setDay", "30分钟"))
        self.label_4.setText(_translate("Form_setDay", "60分钟"))

