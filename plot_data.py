import pyqtgraph as pg
import time
import numpy as np
from datetime import datetime
from PyQt5.QtGui    import QFont

class plot_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.var_init()
        #self.event_init()

    def var_init(self):
        self.start_label_counter = False
        self.fire_label_counter = False
        self.outlier_label_counter = False
        self.output = ''
        pg.setConfigOptions(antialias=True)
        pg.setConfigOptions(useOpenGL=True)

        # 화살표 추가
        self.arrow_01 = pg.ArrowItem(angle=-60, tipAngle=30, headLen=30, tailWidth=10, pen={'color': 'w', 'width': 3}, brush='r')

        # Line Graph 설정
        self.room_index = ['101', '102', '1C', '103', '104', '105', '106', '2C', '107', '108',
                           '201', '202', '3C', '203', '204', '205', '206', '4C', '207', '208',
                           '301', '302', '5C', '303', '304', '305', '306', '6C', '307', '308',
                           '401', '402', '7C', '403', '404', '405', '406', '8C', '407', '408']

        self.line_graph_name = '201'
        self.ui.gr_01.setAxisItems(axisItems={'bottom': TimeAxisItem(orientation='bottom')})    # axis x축 시간값으로 출력
        self.ui.gr_02.setAxisItems(axisItems={'bottom': TimeAxisItem(orientation='bottom')})    # axis x축 시간값으로 출력
        self.ui.gr_01.setMouseEnabled(x=False, y=False)                                         # mouse grab disable
        self.ui.gr_02.setMouseEnabled(x=False, y=False)                                         # mouse grab disable
        self.ui.gr_01.setBackground('w')                                                        # 배경 색 변경
        self.ui.gr_02.setBackground('w')                                                        # 배경 색 변경
        self.ui.gr_01.setTitle('%s T Sensor' % self.line_graph_name)
        self.ui.gr_02.setTitle('%s G Sensor' % self.line_graph_name)
        self.ui.gr_01.getAxis('left').setStyle(autoExpandTextSpace=False, textFillLimits=[(0, 0.7)])
        self.ui.gr_01.getAxis('left').setLabel('Temperature', units='°C')
        self.ui.gr_02.getAxis('left').setLabel('Gas', units='%')
        self.ui.gr_02.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.curve_01 = self.ui.gr_01.plot()                                                    # PlotDataItem 객체 생성
        self.curve_02 = self.ui.gr_02.plot()                                                    # PlotDataItem 객체 생성

        # Bar Graph 설정
        self.ui.bgr_01.setMouseEnabled(x=False, y=False)
        self.ui.bgr_02.setMouseEnabled(x=False, y=False)
        self.ui.bgr_01.setBackground('w')
        self.ui.bgr_02.setBackground('w')
        self.ui.bgr_01.setRange(xRange=(0, 41), disableAutoRange=True, padding=0)                  # axis Range 고정, AutoRange 설정, axis와 Bargraph 간 간격 제거
        self.ui.bgr_02.setRange(xRange=(0, 41), disableAutoRange=True, padding=0)                  # axis Range 고정, AutoRange 설정, axis와 Bargraph 간 간격 제거
        self.ui.bgr_02.setLimits(yMin=0)
        self.ui.bgr_01.setLimits(yMin=0)
        self.ui.bgr_01.showGrid(x=False, y=True)
        self.ui.bgr_02.showGrid(x=False, y=True)
        self.ui.bgr_01.setTitle('32세대, 공용부 Temperature (%s)' % datetime.now().strftime('%Y/%m/%d'))
        self.ui.bgr_02.setTitle('32세대, 공용부 Gas (%s)' % datetime.now().strftime('%Y/%m/%d'))

        bgr01_axis = self.ui.bgr_01.getAxis('bottom')                                                            # axis Bottom settings / https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/axisitem.html
        bgr02_axis = self.ui.bgr_02.getAxis('bottom')
        bgr01_axis.setStyle(tickTextOffset=8)
        bgr02_axis.setStyle(tickTextOffset=8)

        ticks = [list(zip(range(1, 41), ('101', '102', '1C', '103', '104', '105', '106', '2C', '107', '108',
                                         '201', '202', '3C', '203', '204', '205', '206', '4C', '207', '208',
                                         '301', '302', '5C', '303', '304', '305', '306', '6C', '307', '308',
                                         '401', '402', '7C', '403', '404', '405', '406', '8C', '407', '408')))]
        bgr01_axis.setTicks(ticks)
        bgr02_axis.setTicks(ticks)

    def event_init(self):
        #self.ui.pushButton_2.clicked.connect(self.change_tabWidget)
        self.ui.monitor_tabWidget.setCurrentIndex(0)

    def data_plot(self, data, last_data, mode):
        if mode == 'real' or mode == 'simulation':
            t = time.time()
            if "00:00:00" == time.strftime("%H:%M:%S", time.localtime(t)):
                self.ui.gr_01.setXRange(int(time.time()), int(time.time()) + 60)
                self.ui.gr_02.setXRange(int(time.time()), int(time.time()) + 60)

            if self.line_graph_name in self.room_index:
                self.ui.gr_01.setYRange(0, 200)
                self.ui.gr_02.setYRange(0, 200)

                i = self.room_index.index(self.line_graph_name) + 1
                self.ui.gr_01.setTitle('%s T_Sensor' % self.line_graph_name)
                self.ui.gr_02.setTitle('%s G_Sensor' % self.line_graph_name)

                self.curve_01.setData(data['x'], data['t'+str(i).zfill(2)], pen='r', connect='finite')
                self.curve_02.setData(data['x'], data['g'+str(i).zfill(2)], pen='b', connect='finite')

                if self.output == 'Start' and self.start_label_counter == False:
                    self.start_label_counter = True

                    self.text_01 = pg.TextItem(text='분석 시작', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
                                               angle=-30, rotateAxis=(1, 0))
                    self.text_01.setPos(data['x'][-1], data['t'+str(i).zfill(2)][-1] + 0.05)
                    self.ui.gr_01.addItem(self.text_01)

                    self.text_02 = pg.TextItem(text='분석 시작', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
                                               angle=-30, rotateAxis=(1, 0))
                    self.text_02.setPos(data['x'][-1], data['g'+str(i).zfill(2)][-1] + 0.05)
                    self.ui.gr_02.addItem(self.text_02)

                elif self.output == 'Fire' and self.fire_label_counter == False:
                    self.fire_label_counter = True
                    self.text_01 = pg.TextItem(text='화재 발생', fill=(255, 0, 0), color=(255, 255, 255), anchor=(1, 1),
                                               angle=-30, rotateAxis=(1, 0))
                    self.text_01.setPos(data['x'][-1], data['t'+str(i).zfill(2)][-1] + 0.05)
                    self.ui.gr_01.addItem(self.text_01)

                    self.text_02 = pg.TextItem(text='화재 발생', fill=(255, 0, 0), color=(255, 255, 255), anchor=(1, 1),
                                               angle=-30, rotateAxis=(1, 0))
                    self.text_02.setPos(data['x'][-1], data['g'+str(i).zfill(2)][-1] + 0.05)
                    self.ui.gr_02.addItem(self.text_02)

                elif self.output == 'Outlier' and self.outlier_label_counter == False:
                    self.outlier_label_counter = False
                    self.text_01 = pg.TextItem(text='이상치', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
                                               angle=-30, rotateAxis=(1, 0))
                    self.text_01.setPos(data['x'][-1], data['t'+str(i).zfill(2)][-1] + 0.05)
                    self.ui.gr_01.addItem(self.text_01)

                    self.text_02 = pg.TextItem(text='이상치', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
                                               angle=-30, rotateAxis=(1, 0))
                    self.text_02.setPos(data['x'][-1], data['g'+str(i).zfill(2)][-1] + 0.05)
                    self.ui.gr_02.addItem(self.text_02)


            self.ui.bgr_01.clear()
            self.ui.bgr_02.clear()
            t_barChar = pg.BarGraphItem(x=np.arange(1, 41), height=last_data['t'], width=0.6, brush=(255, 0, 0))
            g_barChar = pg.BarGraphItem(x=np.arange(1, 41), height=last_data['g'], width=0.6, brush=(0, 97, 158))
            self.ui.bgr_01.addItem(t_barChar)
            self.ui.bgr_02.addItem(g_barChar)

            print(time.time() - t)

class TimeAxisItem(pg.AxisItem): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        """
        override 하여, tick 옆에 써지는 문자를 원하는대로 수정함. values --> x축 값들
        숫자로 이루어진 Itarable data --> ex) List[int]
        """
        # print("--tickStrings valuse ==>", values)
        return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values]