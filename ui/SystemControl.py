# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SystemControl.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtCore import pyqtSignal,QObject
import  os
import threading,time
from algorithm.FiveWave import FiveWave
from ui.PredictTip import Ui_Form
from ui.StatisticPredict import Statistical_Form

import ui.images_qr
class Ui_MainWindow(QObject):

    appIconPath = 'img/atm.ico'

    def setWidgetIcon(self, widget):
         from PyQt5.Qt import QIcon
         widget.setWindowIcon(QIcon(self.appIconPath))

    dataDisplay = pyqtSignal()
    dataDisplayAddOne = pyqtSignal()
    updateStatus = pyqtSignal(str)

    # 自选股股票代码
    codes =[]

    # 安全关闭本程序 需要停止多线程 以及线程池
    def saftyCloseWindow(self):
        self.stopThread = True
        try:
            import  sys
            self.parent.close()
            self.widget2.close()
            self.widgetStatistical.close()
            self.widgetSetDay.close()
            self.widgeRemind.close()
        except:
            print('close error')

    ## 多线程获取数据
    from queue import Queue
    queueData = Queue()
    from concurrent.futures import ThreadPoolExecutor
    threadPool = ThreadPoolExecutor(100)

# kTypes = ['M','W','D','60','30','15','5']
    def handle(self, code, k_type ='5'):
        if self.stopThread:
            return
        import datetime
        now = datetime.datetime.now()
        if k_type == '5':
            day_ = self.params['day5']
        elif k_type == '15':
            day_ = self.params['day15']
        elif k_type == '30':
            day_ = self.params['day30']
        elif k_type == '60':
            day_ = self.params['day60']
        delta = datetime.timedelta(days=day_)  # 获取过去5天的数据
        n_days = now - delta
        n_days2 = now + datetime.timedelta(days=1)
        endTm = n_days2.strftime('%Y-%m-%d')
        startTm = n_days.strftime('%Y-%m-%d')
        import tushare as ts
        original_data = ts.get_hist_data(code, ktype=k_type, start=startTm, end=endTm )
        self.queueData.put((code,original_data, k_type))

    # 调用展示5浪查询预警界面
    firstUse = True
    displayCodeInfos ={}
    def showPredictTipWidget(self):
        if self.firstUse:
            self.firstUse = False
            self.widget2 = QtWidgets.QWidget(None)
            self.setWidgetIcon(self.widget2)
            self.displayForm = Ui_Form(self.widget2)
            self.displayForm.dirPath = self.dirPath
        if len(self.displayCodeInfos) != 0:
            self.displayForm.setTableDatas(self.displayCodeInfos)
     #   self.displayForm.openPaintWidget(0,1)
        # 判断是否需要弹窗
        # if len(self.displayCodeInfos) != 0 and self.params['popup']:
        #     self.widget2.hide()
        #     from PyQt5.QtCore import Qt
        #     self.widget2.setWindowFlags(Qt.WindowStaysOnTopHint)
        #     self.widget2.show()
        # else:
        #     self.widget2.setWindowFlags(Qt.Widget)
        self.widget2.show()

    displayStatisticalFormFirst = True
    def showStatistical_Form(self):
        if self.displayStatisticalFormFirst:
            self.displayStatisticalFormFirst = False
            self.widgetStatistical = QtWidgets.QWidget(None)
            self.setWidgetIcon(self.widgetStatistical)
            self.statisticalForm = Statistical_Form(self.widgetStatistical)
        self.widgetStatistical.show()


    #  从文件里面读取自选股代码
    def getMyShareCode(self, name = '/自选股.EBK'):
        if os.path.exists(self.dirPath+name):
            with open(self.dirPath+name, 'r') as f:
                for line in f.readlines():
                    if line !=  None and len(line) >=6:
                        self.codes.append(line[1:7])

    stopThread = False
    def timerToMonitor(self):

        self.codes.clear()
         # 判断是否需要自选股
        if self.params['my']:
            self.getMyShareCode('/自选股.EBK')
            self.updateStatus.emit('自选股代码读取完毕，'+str(len(self.codes))+' 支')
        import tushare as ts
        if self.params['002']:
            data = ts.get_sme_classified()
            self.codes.extend(data['code'])
            self.updateStatus.emit('002中小板股票代码读取完毕，'+str(len(data))+' 支')
        if self.params['300']:
            data = ts.get_gem_classified()
            self.codes.extend(data['code'])
            self.updateStatus.emit('300创业板股票代码读取完毕，'+str(len(data))+' 支')
        if self.params['600']:
            n = len(self.codes)
            self.getMyShareCode('/上证A股.EBK')
            self.updateStatus.emit('600上证50成份股票代码读取完毕，'+str(len(self.codes)-n)+' 支')
        if self.params['000']:
            data = ts.get_hs300s()
            self.codes.extend(data['code'])
            self.updateStatus.emit('000沪深300成份股票代码读取完毕，'+str(len(data))+' 支')
        self.displayCodeInfos = {}
        minute5Cnt = 0  # 记录经过了几次5分钟定时，用来处理全周期监控
        while True:
            if self.stopThread:
                return
            if self.params['5m']:
                self.checkShareTrend('5')

            if self.params['15m'] and minute5Cnt%3 == 0:
                self.checkShareTrend('15')

            if self.params['30m'] and minute5Cnt%6 == 0:
                self.checkShareTrend('30')

            if self.params['60m'] and minute5Cnt%12 == 0:
                self.checkShareTrend('60')

            # 执行完一次自动备份数据
            self.backup()
            import time
            n = len(self.codes)/ 60
            if n >5:
                n = 60
            elif n<5:
                n = (5-n)*60
            else:
                n = 60
            time.sleep(n)
            minute5Cnt += 1

    def backup(self):
        # 以当前日期为文件命名方式
        import datetime
        filePath = self.dirPath+'/backup'+ datetime.datetime.now().strftime('%Y-%m-%d')
        if os.path.exists(filePath) == False:
            # 写入配置文件
            import pickle
            with open(filePath, 'wb') as f:
                pickle.dump(self.displayCodeInfos, f)
        else:
            # 先读取数据  再更新
            import pickle
            with open(filePath, 'rb') as f:
                self.oldCodeInfos = pickle.load(f)
            for key in self.displayCodeInfos.keys():
                self.oldCodeInfos[key] = self.displayCodeInfos[key]
            with open(filePath, 'wb') as f:
                pickle.dump(self.oldCodeInfos, f)

    def outputData(self):
        with open(self.dirPath+'/codes.txt', 'w') as f:
            for code in self.displayCodeInfos.keys():
                f.write(code+'   '+ self.displayCodeInfos[code]['findTm']+'\n')

    # 执行对三千支股票的监测
    def checkShareTrend(self, k_type):
        finishedCnt = 0
        hasFindCnt = 0

      #  self.updateStatus.emit('正在执行检测，请稍等。。。')
        for code in self.codes: #['002311', '002311']:#
            self.threadPool.submit(self.handle, code, k_type)
        while True:
            self.updateStatus.emit('正在检测股票：'+code+'   进度：'+ str(finishedCnt)+'/'+ str(len(self.codes)) \
                        + '  已找到 '+ str(hasFindCnt)+' 支  '+ k_type+'分周期监控')

            if self.stopThread:
                self.updateStatus.emit('已停止检测...')
                return

            try:
                code, data, Ktype = self.queueData.get(timeout=10)
            except:
                print('url time out')
                break
            # 处理数据
            fw = FiveWave()
            if self.params['cnt_check']:
                cnt = self.params['cnt']
            else:
                cnt = -1
            if self.params['stand1']:
                stand = 1
            else:
                stand = 2

            result = fw.getCheckResult(code, data, cnt, stand)
            if result != None:
                result['Ktype'] = Ktype
                self.updateStatus.emit('股票'+ code+'符合条件！')
                self.displayCodeInfos[code] = result
                hasFindCnt += 1
                # 通知查询框显示结果
                self.dataDisplay.emit()

            finishedCnt += 1

        if len(self.displayCodeInfos) != 0:
            self.updateStatus.emit('当前检测轮询完毕！发现'+str(len(self.displayCodeInfos))+'支符合条件！')
        else:
            self.updateStatus.emit('当前检测轮询完毕！未发现符合条件的股票')

    def __init__(self, parent, path):
        super().__init__()
        self.setupUi(parent)
        self.dirPath = path
        self.parent = parent
        self.params = {}

        # 尝试读取配置文件
        self.readConfig()
        # 读取所有股票的代码信息
      #  self.getShareCode()

        self.dataDisplay.connect(self.showPredictTipWidget)
        # 配置槽函数
#       self.pBtn_save.clicked.connect(self.saveConfig)
        self.pBtn_monitor_auto.clicked.connect(self.controlMonitorBtnState)
        self.updateStatus.connect(self.updatStatusBar)
        # 所有的配置信息按钮的槽函数统一指定
        self.checkBox_5m.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_15m.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_30m.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_60m.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_day.clicked.connect(self.saveCOnfigDynamic)

        self.checkBox_600.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_300.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_000.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_002.clicked.connect(self.saveCOnfigDynamic)
        self.checkBox_my.clicked.connect(self.saveCOnfigDynamic)

        self.checkBox_cnt.clicked.connect(self.saveCOnfigDynamic)
        self.spinBox_cnt.valueChanged.connect(self.saveCOnfigDynamic)
        self.radioButton_stand1.clicked.connect(self.saveCOnfigDynamic)
        self.radioButton_stand2.clicked.connect(self.saveCOnfigDynamic)

        # 更新状态栏信息
        self.updatStatusBar('欢迎使用自动预警系统！')
        self.pBtn_monitor_auto.setToolTip('按下开启自动预警！！')

        self.showPredictRemindWidget()
        self.showDaySetWidget()


    monitorBtnState = False
    def controlMonitorBtnState(self):
        if self.monitorBtnState == False:
            self.startMonitor()
        else:
            self.stopMonitor()

    def stopMonitor(self):
        # 停止线程的执行
        #self.tHread.setDaemon(False)
        self.monitorBtnState = False
        self.pBtn_monitor_auto.setStyleSheet(self.styleetBtnGreen)
        self.pBtn_monitor_auto.setToolTip('按下开启自动预警！！')
        self.stopThread = True

    def startMonitor(self):
        # 先检查用户是否保存了配置
        if not self.params['5m'] and not self.params['15m'] and not self.params['30m'] \
             and not self.params['60m'] and not self.params['day']:
            QtWidgets.QMessageBox.warning(self.parent, '提示', '请勾选预警级别！')
            return None

        if not self.params['002'] and not self.params['000'] and not self.params['300'] \
             and not self.params['600'] and not self.params['my']:
            QtWidgets.QMessageBox.warning(self.parent, '提示', '请勾选预警股票类型！')
            return None

        # 开起线程
        self.tHread = threading.Thread(target=self.timerToMonitor, name='timerToMonitor')
        self.tHread.start()

        self.monitorBtnState = True
        self.stopThread = False
        self.pBtn_monitor_auto.setStyleSheet(self.styleetBtnRed)
        self.pBtn_monitor_auto.setToolTip('按下关闭自动预警！！')

    # 更新状态栏信息
    def updatStatusBar(self, msg):
        self.statusBar.showMessage(msg)

    # 读取配置文件
    def readConfig(self):

        print(self.dirPath)
        if os.path.exists(self.dirPath+'/config.in') == False:
             # 初始化字典
            self.params['5m'] = False
            self.params['15m'] = False
            self.params['30m'] = False
            self.params['60m'] = False
            self.params['day'] = False

            self.params['002'] = False
            self.params['300'] = False
            self.params['600'] = False
            self.params['000'] = False
            self.params['my'] = False
            self.params['cnt_check'] = False
            self.params['cnt'] = 0
            self.params['stand1'] = True
            self.params['stand2'] = False
            self.params['popup'] = False
            self.params['music'] = False
            self.params['day5'] = 5
            self.params['day15'] = 10
            self.params['day30'] = 30
            self.params['day60'] = 90
            print(self.params)
            return None

        import pickle
        with open(self.dirPath+'/config.in', 'rb') as f:
            self.params = pickle.load(f)
        if self.params != None:
            self.checkBox_5m.setChecked(self.params['5m'])
            self.checkBox_15m.setChecked(self.params['15m'])
            self.checkBox_30m.setChecked(self.params['30m'])
            self.checkBox_60m.setChecked(self.params['60m'])
            self.checkBox_day.setChecked(self.params['day'])

            self.checkBox_cnt.setChecked(self.params['cnt_check'])
            self.spinBox_cnt.setValue(self.params['cnt'])
            self.radioButton_stand1.setChecked(self.params['stand1'])
            self.radioButton_stand2.setChecked(self.params['stand2'])

            self.checkBox_000.setChecked(self.params['000'])
            self.checkBox_002.setChecked(self.params['002'])
            self.checkBox_300.setChecked(self.params['300'])
            self.checkBox_600.setChecked(self.params['600'])
            self.checkBox_my.setChecked(self.params['my'])


    firstOpenDaySet = True
    def showDaySetWidget(self):
        if self.firstOpenDaySet:
            self.firstOpenDaySet = False
            from ui.FormSetDay import Ui_Form_setDay
            self.widgetSetDay = QtWidgets.QWidget(None)
            self.setWidgetIcon(self.widgetSetDay)
            self.setDayForm = Ui_Form_setDay(self.widgetSetDay)
            self.setDayForm.spinBox_5.valueChanged.connect(self.saveCOnfigDynamic)
            self.setDayForm.spinBox_15.valueChanged.connect(self.saveCOnfigDynamic)
            self.setDayForm.spinBox_30.valueChanged.connect(self.saveCOnfigDynamic)
            self.setDayForm.spinBox_60.valueChanged.connect(self.saveCOnfigDynamic)
            self.remindForm.setParam(self.params)
        else:
            self.setDayForm.setParams(self.params)
            self.widgetSetDay.show()

    firstOpenRemind = True
    def showPredictRemindWidget(self):
        if self.firstOpenRemind:
            self.firstOpenRemind = False
            from ui.FormRemind import Ui_Form_Remind
            self.widgeRemind = QtWidgets.QWidget(None)
            self.setWidgetIcon(self.widgeRemind)
            self.remindForm = Ui_Form_Remind(self.widgeRemind)
            self.remindForm.checkBox_popup.clicked.connect(self.saveCOnfigDynamic)
            self.remindForm.checkBox_music.clicked.connect(self.saveCOnfigDynamic)
            self.remindForm.setParam(self.params)
        else:
            self.remindForm.setParam(self.params)
            self.widgeRemind.show()

    def saveCOnfigDynamic(self, value = 0):
        # 动态保存用户每一次修改的配置信息  无需点击保存配置
        sder = self.sender()
        if sder == self.checkBox_5m:
            self.params['5m'] = self.checkBox_5m.isChecked()
        elif sder == self.checkBox_15m:
            self.params['15m'] = self.checkBox_15m.isChecked()
        elif sder == self.checkBox_30m:
            self.params['30m'] = self.checkBox_30m.isChecked()
        elif sder == self.checkBox_60m:
            self.params['60m'] = self.checkBox_60m.isChecked()
        elif sder == self.checkBox_day:
            self.params['day'] = self.checkBox_day.isChecked()
        elif sder == self.checkBox_002:
            self.params['002'] = self.checkBox_002.isChecked()
        elif sder == self.checkBox_000:
            self.params['000'] = self.checkBox_000.isChecked()
        elif sder == self.checkBox_300:
            self.params['300'] = self.checkBox_300.isChecked()
        elif sder == self.checkBox_600:
            self.params['600'] = self.checkBox_600.isChecked()
        elif sder == self.checkBox_my:
            self.params['my'] = self.checkBox_my.isChecked()
        elif sder == self.checkBox_cnt:
            self.params['cnt_check'] = self.checkBox_cnt.isChecked()
        elif sder == self.spinBox_cnt:
            self.params['cnt'] = value
        elif sder == self.remindForm.checkBox_popup:
            self.params['popup'] = self.remindForm.checkBox_popup.isChecked()
        elif sder == self.remindForm.checkBox_music:
            self.params['music'] = self.remindForm.checkBox_music.isChecked()
        elif sder == self.setDayForm.spinBox_5:
            self.params['day5'] = value
        elif sder == self.setDayForm.spinBox_15:
            self.params['day15'] = value
        elif sder == self.setDayForm.spinBox_30:
            self.params['day30'] = value
        elif sder == self.setDayForm.spinBox_60:
            self.params['day60'] = value

        # 写入配置文件
        import pickle
        with open(self.dirPath+'/config.in', 'wb') as f:
            pickle.dump(self.params, f)

        #QtWidgets.QMessageBox(self.parent, '提示', '配置信息保存成功！')
    # def saveConfig(self):
    #     result = {}
    #     # 读取预警级别信息 8个
    #     result['5m'] =  self.checkBox_5m.isChecked()
    #     result['15m'] =  self.checkBox_15m.isChecked()
    #     result['30m'] =  self.checkBox_30m.isChecked()
    #     result['60m'] =  self.checkBox_60m.isChecked()
    #     result['day'] =  self.checkBox_day.isChecked()
    #     # 读取5浪配置信息  8个
    #     result['cnt_check'] =  self.checkBox_cnt.isChecked()
    #     result['cnt'] =  self.spinBox_cnt.value()
    #     result['stand1'] = self.radioButton_stand1.isChecked()
    #     result['stand2'] = self.radioButton_stand2.isChecked()
    #     self.params = result
    #     print(result)
    #     # 写入配置文件
    #     import pickle
    #     with open(self.dirPath+'/config.in', 'wb') as f:
    #         pickle.dump(result, f)
    #     #QtWidgets.QMessageBox(self.parent, '提示', '配置信息保存成功！')

#######################   以下为qt ui文件自动转换成py文件的代码    ####################################



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 309)
        MainWindow.setMinimumSize(QtCore.QSize(510, 309))
        MainWindow.setMaximumSize(QtCore.QSize(510, 309))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_5m = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_5m.sizePolicy().hasHeightForWidth())
        self.checkBox_5m.setSizePolicy(sizePolicy)
        self.checkBox_5m.setMinimumSize(QtCore.QSize(50, 0))
        self.checkBox_5m.setMaximumSize(QtCore.QSize(50, 16777215))
        self.checkBox_5m.setObjectName("checkBox_5m")
        self.horizontalLayout.addWidget(self.checkBox_5m)
        self.checkBox_15m = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_15m.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_15m.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_15m.setObjectName("checkBox_15m")
        self.horizontalLayout.addWidget(self.checkBox_15m)
        self.checkBox_30m = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_30m.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_30m.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_30m.setObjectName("checkBox_30m")
        self.horizontalLayout.addWidget(self.checkBox_30m)
        self.checkBox_60m = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_60m.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_60m.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_60m.setObjectName("checkBox_60m")
        self.horizontalLayout.addWidget(self.checkBox_60m)
        self.checkBox_day = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_day.setMinimumSize(QtCore.QSize(45, 0))
        self.checkBox_day.setMaximumSize(QtCore.QSize(45, 16777215))
        self.checkBox_day.setObjectName("checkBox_day")
        self.horizontalLayout.addWidget(self.checkBox_day)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_600 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_600.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_600.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_600.setObjectName("checkBox_600")
        self.horizontalLayout_2.addWidget(self.checkBox_600)
        self.checkBox_300 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_300.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_300.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_300.setObjectName("checkBox_300")
        self.horizontalLayout_2.addWidget(self.checkBox_300)
        self.checkBox_000 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_000.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_000.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_000.setObjectName("checkBox_000")
        self.horizontalLayout_2.addWidget(self.checkBox_000)
        self.checkBox_002 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_002.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_002.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_002.setObjectName("checkBox_002")
        self.horizontalLayout_2.addWidget(self.checkBox_002)
        self.checkBox_my = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_my.setMinimumSize(QtCore.QSize(60, 0))
        self.checkBox_my.setMaximumSize(QtCore.QSize(60, 16777215))
        self.checkBox_my.setObjectName("checkBox_my")
        self.horizontalLayout_2.addWidget(self.checkBox_my)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_2.setMinimumSize(QtCore.QSize(100, 100))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_cnt = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_cnt.setObjectName("checkBox_cnt")
        self.horizontalLayout_3.addWidget(self.checkBox_cnt)
        self.spinBox_cnt = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_cnt.setObjectName("spinBox_cnt")
        self.horizontalLayout_3.addWidget(self.spinBox_cnt)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.radioButton_stand1 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_stand1.setChecked(True)
        self.radioButton_stand1.setObjectName("radioButton_stand1")
        self.verticalLayout.addWidget(self.radioButton_stand1)
        self.radioButton_stand2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_stand2.setObjectName("radioButton_stand2")
        self.verticalLayout.addWidget(self.radioButton_stand2)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.pBtn_monitor_auto = QtWidgets.QPushButton(self.groupBox_2)
        self.pBtn_monitor_auto.setMinimumSize(QtCore.QSize(60, 60))
        self.pBtn_monitor_auto.setMaximumSize(QtCore.QSize(60, 60))
        self.pBtn_monitor_auto.setStyleSheet(self.styleetBtnGreen)
        self.pBtn_monitor_auto.setText("")
        self.pBtn_monitor_auto.setObjectName("pBtn_monitor_auto")
        self.horizontalLayout_7.addWidget(self.pBtn_monitor_auto)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_9.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #### 添加工具栏信息
        from PyQt5.Qt import Qt
        from PyQt5.Qt import QIcon
        from PyQt5.QtWidgets import QToolButton
        listToolBtn = QToolButton()
        listToolBtn.setIcon(QIcon(':/img/list.png'))
        listToolBtn.setText('预警列表')
        listToolBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        listToolBtn.clicked.connect(self.showPredictTipWidget)
        self.toolBar.addWidget(listToolBtn)

        statisticToolBtn = QToolButton()
        statisticToolBtn.setIcon(QIcon(':/img/rise.png'))
        statisticToolBtn.setText('统计历史盈亏')
        statisticToolBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        statisticToolBtn.clicked.connect(self.showStatistical_Form)
        self.toolBar.addWidget(statisticToolBtn)

        kToolBtn = QToolButton()
        kToolBtn.setIcon(QIcon(':/img/k.png'))
        kToolBtn.setText('K线个数')
        kToolBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        kToolBtn.clicked.connect(self.showDaySetWidget)
        self.toolBar.addWidget(kToolBtn)

        remindToolBtn = QToolButton()
        remindToolBtn.setIcon(QIcon(':/img/alarm.png'))
        remindToolBtn.setText('消息提醒')
        remindToolBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        remindToolBtn.clicked.connect(self.showPredictRemindWidget)
        self.toolBar.addWidget(remindToolBtn)

        quitToolBtn = QToolButton()
        quitToolBtn.setIcon(QIcon(':/img/close.png'))
        quitToolBtn.setText('安全退出')
        quitToolBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        quitToolBtn.clicked.connect(self.saftyCloseWindow)
        self.toolBar.addWidget(quitToolBtn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "股票实时监测系统"))
        self.groupBox.setTitle(_translate("MainWindow", "选择预警级别"))
        self.checkBox_5m.setText(_translate("MainWindow", "5分钟"))
        self.checkBox_15m.setText(_translate("MainWindow", "15分钟"))
        self.checkBox_30m.setText(_translate("MainWindow", "30分钟"))
        self.checkBox_60m.setText(_translate("MainWindow", "60分钟"))
        self.checkBox_day.setText(_translate("MainWindow", "日线"))
        self.groupBox_4.setTitle(_translate("MainWindow", "预警类别"))
        self.checkBox_600.setText(_translate("MainWindow", "600开头"))
        self.checkBox_300.setText(_translate("MainWindow", "300开头"))
        self.checkBox_000.setText(_translate("MainWindow", "000开头"))
        self.checkBox_002.setText(_translate("MainWindow", "002开头"))
        self.checkBox_my.setText(_translate("MainWindow", "自选股"))
        self.groupBox_2.setTitle(_translate("MainWindow", "5浪模式参数"))
        self.checkBox_cnt.setText(_translate("MainWindow", "设置大5浪最大播波动次数(>2)"))
        self.radioButton_stand1.setText(_translate("MainWindow", "标准1：中枢区间与振幅区间均不重叠"))
        self.radioButton_stand2.setText(_translate("MainWindow", "标准2：中枢区间不重叠，振幅区间重叠"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))



    styleetBtnRed = '''
    QPushButton{
        background-color: rgb(220, 60, 0);
        color: rgb(255, 255, 255);
        font: 12pt \"Adobe Arabic\";
        border-radius:30px;
        border:2px groove gray;
    }
    QPushButton:hover{
        background-color: rgb(170, 0, 0);
        color: rgb(255, 255, 255);
        font: 12pt \"Adobe Arabic\";
    }
    QPushButton:pressed{
        background-color: rgb(220, 60, 0);
        color: rgb(255, 255, 255);"
        font: 12pt \"Adobe Arabic\";
    }'''

    styleetBtnGreen = '''
    QPushButton{
        background-color: rgb(76, 229, 0);
        color: rgb(255, 255, 255);
        font: 12pt \"Adobe Arabic\";
        border-radius:30px;
        border:2px groove gray;
    }
    QPushButton:hover{
        background-color: rgb(44, 173, 44);
        color: rgb(255, 255, 255);
        font: 12pt \"Adobe Arabic\";
    }
    QPushButton:pressed{
        background-color: rgb(60, 86, 48);
        color: rgb(255, 255, 255);"
        font: 12pt \"Adobe Arabic\";
    }'''

############################# 直接从这里开始运行 ############################################

def justForPackage():
    from ui.StatisticPredict import Statistical_Form
    from ui.FormSetDay import Ui_Form_setDay
    from ui.Paint import Ui_Paint
    from ui.PredictTip import Ui_Form
    from ui.FormRemind import Ui_Form_Remind
    from algorithm.FiveWave import FiveWave

import  sys
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),".")) # .. 表示上一级 .表示当前目录
    print(path)
    ui= Ui_MainWindow(widget, path)
    from PyQt5.Qt import Qt, QIcon
    widget.setWindowIcon(QIcon(':/img/atm.ico'))
    widget.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint )
    widget.show()
    sys.exit(app.exec_())