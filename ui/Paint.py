# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Paint.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from  PyQt5.QtCore import pyqtSignal, QObject

import matplotlib

matplotlib.use("Qt5Agg")
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import tushare as ts
import matplotlib.finance as mpf

class MyMplCanvas(FigureCanvas):
    # 绘图勾选参数
    hasData = False
    close = False
    low = False
    high = False
    ma = False
    # 5浪绘图参数
    wave5 = False
    mid5 = False
    trend5 = False
    # 设置绘图数据
    isOriginData = True

    def setData(self, data):
      #   code = '600021'
      #   startTm = '2017-06-12'
      #   endTm = '2017-06-15'
      #   self.infos  = ts.get_hist_data(code,ktype='5', start=startTm, end=endTm )
      # #  self.infos = data
      #   print('get data over')
        # 初始化相关配置
        self.infos = data
        self.hasData = True
        self.close = True
        self.high = False
        self.low = False
        self.ma = False
        self.trend5 = True
        self.mid5 = False
        self.wave5 = False
        self.isOriginData = True

        self.update_figure()

    def __init__(self, parent=None, width=11, height=7, dpi=100):
        #   self.infos = None
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        # 每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
        #  self.axes.hold(False)
      #  self.update_figure()
        FigureCanvas.__init__(self, self.fig)
        self.fig.subplots_adjust(bottom=0.3)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Maximum, QSizePolicy.Maximum)
        FigureCanvas.updateGeometry(self)


    # def update_figure(self):
    #     import threading
    #     self.tHread2 = threading.Thread(target=self.updateFigureByThread, name='updateFigureByThread')
    #     self.tHread2.start()


    # def updateFigureByThread(self):
    #     if self.hasData == True:
    #         data_list = []
    #       #  del self.axes.lines[:]
    #         # help(self.axes)
    #         # 首先处理原始轨迹绘制
    #         if self.isOriginData:
    #             data = self.infos['origin']
    #         else:
    #             data = self.infos['filterData']
    #         i = 0
    #         x1 = []
    #         for dates,row in data.iterrows():
    #             open,high, close,low = row[:4]
    #             x1.append(len(data)-1-i)
    #             datas = (len(data)-1- i,open,high,low,close)
    #             data_list.append(datas)
    #             i += 1
    #
    #         mpf.candlestick_ohlc(self.axes,data_list,width=1.5,colorup='r',colordown='green')
    #         mpf.xrange(x1[-1], x1[0])
    #
    #         if self.ma:
    #             y4 = data['ma10']
    #             self.axes.plot(x1, y4, 'blue')
    #
    #         # 绘制横坐标标签
    #         subName = []
    #         subX = []
    #         N = int(len(data_list) / 20 +1)
    #         print('N',N)
    #         for i in range(len(data_list)):
    #             if i % N == 0:
    #                 subX.append(x1[i])
    #                 subName.append(data['close'].index[i])
    #         self.axes.set_xticks(subX)
    #         self.axes.set_xticklabels(subName, rotation=75)
    #
    #         # # 绘制5浪数据
    #         indexs = self.infos['5maxIndexs']  # 先获取5浪各个定位点的位置信息
    #         print(indexs)
    #         x5wave = []
    #         y5wave = []
    #         for i in indexs:  # y轴记录close数据位置
    #             y5wave.append(self.infos['filterData']['close'][i])
    #             index = data['close'].index.get_loc(self.infos['filterData']['close'].index[i])
    #             x5wave.append(len(data) - 1 - index)
    #
    #         self.axes.set_xlim(x1[-1], x1[0])
    #         if self.trend5:
    #             self.axes.plot(x5wave, y5wave, 'purple')
    #         self.draw()


    def update_figure(self):
        if self.hasData == True:

            del self.axes.lines[:]
            # help(self.axes)
            # 首先处理原始轨迹绘制
            if self.isOriginData:
                data = self.infos['origin']
            else:
                data = self.infos['filterData']
            x1 = list(reversed(range(len(data))))
            print('X1 len:', len(x1))
            if self.close:
                y1 = data['close']
                self.axes.plot(x1, y1, 'black')
            if self.high:
                y2 = data['high']
                self.axes.plot(x1, y2, 'blue')
            if self.low:
                y3 = data['low']
                self.axes.plot(x1, y3, 'brown')
            if self.ma:
                y4 = data['ma10']
                self.axes.plot(x1, y4, 'blue')

            # 绘制横坐标标签
            subX = []
            subName = []
            N = int(len(x1) / 20 +1)
            for i in range(len(x1)-1):
                if i % N == 0:
                    subX.append(x1[i])
                    subName.append(data['close'].index[i])
            subX.append(x1[-1])
            subName.append(data['close'].index[-1])
            self.axes.set_xticks(subX)
            # help(self.axes)
            self.axes.set_xticklabels(subName, rotation=30)

            # 绘制5浪数据

            indexs = self.infos['5maxIndexs']  # 先获取5浪各个定位点的位置信息
            print(indexs)
            x5wave = []
            y5wave = []
            for i in indexs:  # y轴记录close数据位置
                y5wave.append(self.infos['filterData']['close'][i])
                index = data['close'].index.get_loc(self.infos['filterData']['close'].index[i])
                x5wave.append(len(data) - 1 - index)

            self.axes.set_xlim(x1[-1], x1[0])
            if self.trend5:
                self.axes.plot(x5wave, y5wave, 'purple')

            if self.wave5:
                # 计算波动区间范围
                waveY1 = min(self.infos['filterData']['close'][indexs[1]: indexs[2] + 1])
                waveY2 = max(self.infos['filterData']['close'][indexs[1]: indexs[2] + 1])
                waveX1 = x5wave[2]
                waveX2 = x5wave[1]
                self.axes.plot([waveX1, waveX1, waveX2, waveX2, waveX1], \
                               [waveY1, waveY2, waveY2, waveY1, waveY1], 'orange')

                waveY1 = min(self.infos['filterData']['close'][indexs[3]: indexs[4] + 1])
                waveY2 = max(self.infos['filterData']['close'][indexs[3]: indexs[4] + 1])
                waveX1 = x5wave[4]
                waveX2 = x5wave[3]
                self.axes.plot([waveX1, waveX1, waveX2, waveX2, waveX1], \
                               [waveY1, waveY2, waveY2, waveY1, waveY1], 'orange')

            if self.mid5:
                pass
                # 计算中枢区间范围
                if indexs[2] - indexs[1] < 3:
                    cut = indexs[2] - indexs[1]
                else:
                    cut = 3

                waveY1 = min(self.infos['filterData']['close'][indexs[2] - cut: indexs[2] + 1])
                waveY2 = max(self.infos['filterData']['close'][indexs[2] - cut: indexs[2] + 1])
                waveX1 = x5wave[2]
                waveX2 = x5wave[1]
                self.axes.plot([waveX1, waveX1, waveX2, waveX2, waveX1], \
                               [waveY1, waveY2, waveY2, waveY1, waveY1], 'red')

                if indexs[4] - indexs[3] < 3:
                    cut = indexs[4] - indexs[3]
                else:
                    cut = 3
                waveY1 = min(self.infos['filterData']['close'][indexs[4] - cut: indexs[4] + 1])
                waveY2 = max(self.infos['filterData']['close'][indexs[4] - cut: indexs[4] + 1])
                waveX1 = x5wave[4]
                waveX2 = x5wave[3]
                self.axes.plot([waveX1, waveX1, waveX2, waveX2, waveX1], \
                               [waveY1, waveY2, waveY2, waveY1, waveY1], 'red')
            self.draw()


class Ui_Paint(object):

    def setPaintData(self, data):
        self.canvas.setData(data)
        self.checkBox_close.setChecked(True)
        self.checkBox_high.setChecked(False)
        self.checkBox_low.setChecked(False)
        self.checkBox_ma10.setChecked(False)
        self.checkBox_5.setChecked(True)

    # 绘图界面各个控件的响应事件  通过sender()来识别信号发出者
    def updateDrawContent(self):
        sder = self.widget.sender()
        if sder == self.checkBox_close:
            self.canvas.close = self.checkBox_close.isChecked()
        elif sder == self.checkBox_high:
            self.canvas.high = self.checkBox_high.isChecked()
        elif sder == self.checkBox_low:
            self.canvas.low = self.checkBox_low.isChecked()
        elif sder == self.checkBox_ma10:
            self.canvas.ma = self.checkBox_ma10.isChecked()
        elif sder == self.radioButton_origin_data:
            self.canvas.isOriginData = True
        elif sder == self.radioButton_pre_data:
            self.canvas.isOriginData = False
        elif sder == self.checkBox_5:
            self.canvas.trend5 = self.checkBox_5.isChecked()
        elif sder == self.checkBox_mid:
            self.canvas.mid5 = self.checkBox_mid.isChecked()
        elif sder == self.checkBox_wave:
            self.canvas.wave5 = self.checkBox_wave.isChecked()

        self.canvas.update_figure()
        print('over')

    def __init__(self, parent):
        self.setupUi(parent)
        from PyQt5.Qt import QIcon
        parent.setWindowIcon(QIcon('img/atm.ico'))

        self.canvas = MyMplCanvas(self.widget)
        #    self.canvas.setData()
        #   self.canvas.update_figure()

        self.checkBox_close.clicked.connect(self.updateDrawContent)
        self.checkBox_high.clicked.connect(self.updateDrawContent)
        self.checkBox_low.clicked.connect(self.updateDrawContent)
        self.checkBox_ma10.clicked.connect(self.updateDrawContent)

        self.radioButton_pre_data.clicked.connect(self.updateDrawContent)
        self.radioButton_origin_data.clicked.connect(self.updateDrawContent)
        self.checkBox_5.clicked.connect(self.updateDrawContent)
        self.checkBox_mid.clicked.connect(self.updateDrawContent)
        self.checkBox_wave.clicked.connect(self.updateDrawContent)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(719, 539)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4.addWidget(self.widget)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setMinimumSize(QtCore.QSize(100, 200))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_close = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_close.setChecked(True)
        self.checkBox_close.setObjectName("checkBox_close")
        self.verticalLayout_3.addWidget(self.checkBox_close)
        self.checkBox_high = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_high.setObjectName("checkBox_high")
        self.verticalLayout_3.addWidget(self.checkBox_high)
        self.checkBox_low = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_low.setObjectName("checkBox_low")
        self.verticalLayout_3.addWidget(self.checkBox_low)
        self.checkBox_ma10 = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_ma10.setObjectName("checkBox_ma10")
        self.verticalLayout_3.addWidget(self.checkBox_ma10)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_origin_data = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_origin_data.setChecked(True)
        self.radioButton_origin_data.setObjectName("radioButton_origin_data")
        self.verticalLayout.addWidget(self.radioButton_origin_data)
        self.radioButton_pre_data = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_pre_data.setObjectName("radioButton_pre_data")
        self.verticalLayout.addWidget(self.radioButton_pre_data)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout_5.addWidget(self.checkBox_5)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton.setMinimumSize(QtCore.QSize(25, 20))
        self.pushButton.setMaximumSize(QtCore.QSize(25, 20))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_mid = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_mid.setMaximumSize(QtCore.QSize(80, 16777215))
        self.checkBox_mid.setObjectName("checkBox_mid")
        self.horizontalLayout_2.addWidget(self.checkBox_mid)
        self.pBtn_mid_color = QtWidgets.QPushButton(self.groupBox_4)
        self.pBtn_mid_color.setMinimumSize(QtCore.QSize(25, 20))
        self.pBtn_mid_color.setMaximumSize(QtCore.QSize(25, 20))
        self.pBtn_mid_color.setText("")
        self.pBtn_mid_color.setObjectName("pBtn_mid_color")
        self.horizontalLayout_2.addWidget(self.pBtn_mid_color)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_wave = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_wave.setMaximumSize(QtCore.QSize(80, 16777215))
        self.checkBox_wave.setObjectName("checkBox_wave")
        self.horizontalLayout.addWidget(self.checkBox_wave)
        self.pBtn_wave_color = QtWidgets.QPushButton(self.groupBox_4)
        self.pBtn_wave_color.setMinimumSize(QtCore.QSize(25, 20))
        self.pBtn_wave_color.setMaximumSize(QtCore.QSize(25, 20))
        self.pBtn_wave_color.setText("")
        self.pBtn_wave_color.setObjectName("pBtn_wave_color")
        self.horizontalLayout.addWidget(self.pBtn_wave_color)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        spacerItem3 = QtWidgets.QSpacerItem(17, 98, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "预警股票走势可视化分析"))
        self.groupBox.setTitle(_translate("Form", "可视化"))
        self.groupBox_2.setTitle(_translate("Form", "控制台"))
        self.groupBox_3.setTitle(_translate("Form", "原始数据显示内容"))
        self.checkBox_close.setText(_translate("Form", "收盘价"))
        self.checkBox_high.setText(_translate("Form", "最高价"))
        self.checkBox_low.setText(_translate("Form", "最低价"))
        self.checkBox_ma10.setText(_translate("Form", "10天均值"))
        self.groupBox_5.setTitle(_translate("Form", "绘图模式"))
        self.radioButton_origin_data.setText(_translate("Form", "原始数据"))
        self.radioButton_pre_data.setText(_translate("Form", "预处理后数据"))
        self.groupBox_4.setTitle(_translate("Form", "5浪显示内容"))
        self.checkBox_5.setText(_translate("Form", "5浪走势"))
        self.checkBox_mid.setText(_translate("Form", "中枢区间"))
        self.checkBox_wave.setText(_translate("Form", "波动区间"))
