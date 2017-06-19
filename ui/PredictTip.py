# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PredictTip.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from ui.Paint import Ui_Paint

class Ui_Form(object):

    titleName = ['代码','开始时间', '结束时间', '3:5','1:3' ,'振幅高度1', '振幅高度2', '中枢高度1',\
                 '中枢高度2', '波浪个数1','波浪个数2', '标准类型','预警周期','预警价格']

    dirPath =''
    def outputData(self):
        if self.tableWidget_predict.rowCount()==0:
            QtWidgets.QMessageBox.information(self.parent, '提示', '当前无预警信息！')
            return
        file_path = QFileDialog.getSaveFileName(self.parent,'导出预警数据文件','预警信息','.txt')
        if file_path == None:
            return
        savePath = file_path[0]+'.txt'
        with open(savePath, 'w') as f:
            for code in self.data.keys():
                f.write(code+'\n')
        QMessageBox.information(self.parent,'提示', '导出信息完成！')

    def openPaintWidget(self, x, y):
        # 获取当前行 第一个股票code信息
        code = self.tableWidget_predict.item(x,0).text()
        self.widget3 = QtWidgets.QWidget()
        self.paintWidget = Ui_Paint(self.widget3)
        self.widget3.setWindowTitle('当前绘制股票代码为 '+ code)
        self.paintWidget.setPaintData(self.data[code])
        self.widget3.showMaximized()
        print('ok')

    def setTableDatas(self, data:dict):
        self.tableWidget_predict.clearContents()
        self.data = data
        # 添加数据
        i = 0
        self.tableWidget_predict.setRowCount(len(data.keys()))
        for key in data.keys():

            item = QTableWidgetItem(key)
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 0, item)

            item = QTableWidgetItem(str(data[key]['startTm']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 1, item)

            item = QTableWidgetItem(str(data[key]['findTm']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 2, item)

            item = QTableWidgetItem(str(data[key]['5:3']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 3, item)

            item = QTableWidgetItem(str(data[key]['1:3']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 4, item)

            item = QTableWidgetItem(str(data[key]['rangeWave1']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 5, item)

            item = QTableWidgetItem(str(data[key]['rangeWave2']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 6, item)

            item = QTableWidgetItem(str(data[key]['rangeMid1']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 7, item)

            item = QTableWidgetItem(str(data[key]['rangeMid2']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 8, item)

            item = QTableWidgetItem(str(data[key]['waveCnt1']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 9, item)

            item = QTableWidgetItem(str(data[key]['waveCnt2']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 10, item)

            item = QTableWidgetItem(str(data[key]['stand']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 11, item)

            item = QTableWidgetItem(str(data[key]['Ktype']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 12, item)

            item = QTableWidgetItem(str(data[key]['alarmPrice']))
            item.setTextAlignment(Qt.AlignHCenter |  Qt.AlignVCenter)
            self.tableWidget_predict.setItem(i, 13, item)
            i += 1
        self.tableWidget_predict.show()

    def clearData(self):
        self.data.clear()
        self.tableWidget_predict.clearContents()

    def rightMenu(self, pos):
        menu = QMenu()
        row_num = -1
        for i in self.tableWidget_predict.selectionModel().selection().indexes():
            row_num = i.row()
        item = menu.addAction('删除')
        action = menu.exec_(self.tableWidget_predict.mapToGlobal(pos))
        if action == item:
            # 从列表数据中也删除此数据
            code = self.tableWidget_predict.item(row_num, 0).text()
            self.data.pop(code)
            # 删除当前item
            self.tableWidget_predict.removeRow(row_num)

        pass

    def __init__(self, parent):
        self.parent = parent
        self.setupUi(parent)
        # 添加表格右键菜单
        self.tableWidget_predict.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget_predict.customContextMenuRequested.connect(self.rightMenu)
        self.pBtn_out.clicked.connect(self.outputData)
        self.pBtn_clear.clicked.connect(self.clearData)

        # 设置每一列自适应宽度
        self.tableWidget_predict.resizeColumnsToContents()
        self.tableWidget_predict.setColumnWidth(0, 60)
        self.tableWidget_predict.setColumnWidth(1, 150)
        self.tableWidget_predict.setColumnWidth(2, 150)
        self.tableWidget_predict.setColumnWidth(3, 60)
        self.tableWidget_predict.setColumnWidth(4, 60)

        # 设置排序相关
        from PyQt5.QtWidgets import QHeaderView
        header = self.tableWidget_predict.horizontalHeader()
        header.setSortIndicatorShown(True)
        #header.setClickable(True)
        print('deeeee')
        header.sectionClicked.connect(self.tableWidget_predict.sortByColumn)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 521)
        Form.setMinimumSize(QtCore.QSize(428, 500))
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_predict = QtWidgets.QTableWidget(Form)
        self.tableWidget_predict.setMinimumSize(QtCore.QSize(0, 30))
        self.tableWidget_predict.setObjectName("tableWidget_predict")
        self.tableWidget_predict.setColumnCount(len(self.titleName))
        self.tableWidget_predict.setRowCount(0)

        for i in range(len(self.titleName)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_predict.setHorizontalHeaderItem(i, item)

        self.verticalLayout.addWidget(self.tableWidget_predict)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 150))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pBtn_clear = QtWidgets.QPushButton(self.groupBox_2)
        self.pBtn_clear.setMinimumSize(QtCore.QSize(60, 30))
        self.pBtn_clear.setMaximumSize(QtCore.QSize(60, 30))
        self.pBtn_clear.setObjectName("pBtn_clear")
        self.horizontalLayout.addWidget(self.pBtn_clear)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pBtn_out = QtWidgets.QPushButton(self.groupBox_2)
        self.pBtn_out.setMinimumSize(QtCore.QSize(60, 30))
        self.pBtn_out.setMaximumSize(QtCore.QSize(60, 30))
        self.pBtn_out.setObjectName("pBtn_out")
        self.horizontalLayout.addWidget(self.pBtn_out)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.tableWidget_predict.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_predict.setSelectionBehavior(QAbstractItemView.SelectRows)

        ############# 为何没用 ###############
        self.tableWidget_predict.cellDoubleClicked.connect(self.openPaintWidget)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "预警数据展示"))
        for i in range(len(self.titleName)):
            item = self.tableWidget_predict.horizontalHeaderItem(i)
            item.setText(_translate("Form", self.titleName[i]))
        self.pBtn_clear.setText(_translate("Form", "清空"))
        self.pBtn_out.setText(_translate("Form", "导出"))



