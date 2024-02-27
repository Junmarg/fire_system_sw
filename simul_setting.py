from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import re
import pandas as pd

simulation_setting_dialog = uic.loadUiType("ui/simulation_setting_form.ui")[0]

class simul_set(QDialog, simulation_setting_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui_init()
        self.var_init()
        self.event_init()

    def ui_init(self):
        self.buttonBox.setEnabled(False)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.graph_canvas.addWidget(self.canvas)

    def var_init(self):
        self.file_name = 0
        self.file_length = 0
        self.set_time = 180

        dic0 = {'x': []}
        dic1 = {'t' + str(x).zfill(2): [] for x in range(1, 41)}
        dic2 = {'g' + str(x).zfill(2): [] for x in range(1, 41)}
        dic0.update(dic1)
        dic0.update(dic2)
        self.dic = dic0

        self.t_colname = ['t' + str(x).zfill(2) for x in range(1, 41)]
        self.g_colname = ['g' + str(x).zfill(2) for x in range(1, 41)]
        self.data_colname = self.t_colname + self.g_colname

    def event_init(self):
        # 라디오 버튼 이벤트 Init
        self.data_load_btn.clicked.connect(self.data_load)

    def data_load(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", "D:/fire_system_sw/simulation_data", "csv file (*.csv)")

        if fname:
            print("-Data Load")
            self.simul_arg_set(fname)
        else:
            print("!Data Load Fail")
            self.buttonBox.setEnabled(False)

    def simul_arg_set(self, fname):
        # 파일 분석 및 세팅값 가져오기
        self.file_name = re.sub(r'[^0-9]', '', fname.split('/')[-1])

        data_frame = pd.read_csv(fname)

        if len(data_frame) < 180:
            self.message_box('length')
            self.buttonBox.setEnabled(False)
        elif len(data_frame.columns) != 80:
            self.message_box('column')
            self.buttonBox.setEnabled(False)
        else:
            data_frame.columns = self.data_colname  # column 이름 변경
            for k in self.dic:
                if k == 'x':
                    pass
                else:
                    self.dic[k] = data_frame[k].tolist()  # Dictionary에 데이터 삽입

            self.data_plot(data_frame)

    def data_plot(self, df):
        print("-Data Plot")

        self.fig.clear()

        ax1 = self.fig.add_subplot(121)
        ax1.set_title("Temperature (ºC)")
        ax1.plot(df[self.t_colname])

        ax2 = self.fig.add_subplot(122)
        ax2.set_title("Gas (%)")
        ax2.plot(df[self.g_colname])

        self.canvas.draw()

        self.buttonBox.setEnabled(True)

    def message_box(self, type):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error")
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Yes)
        msgBox.setDefaultButton(QMessageBox.Yes)

        if type == 'length':
            msgBox.setText("데이터 크기 오류")
            msgBox.setInformativeText("데이터의 최소 크기는 180이상입니다")
        if type == 'column':
            msgBox.setText("속성 오류")
            msgBox.setInformativeText("속성 개수는 80개가 필요합니다")

        self.buttonBox.setEnabled(False)
        msgBox.exec_()