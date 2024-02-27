from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem
import numpy as np
import matplotlib.pyplot as plt
import os, io
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

plt.rcParams.update({'figure.max_open_warning': 0})
model = tf.keras.models.load_model("model/model_gaussian.h5")

class classification_thread(QThread):
    analy_output = pyqtSignal(object, object)

    def __init__(self):
        super().__init__( )
        self.working = False

    def arg_(self, id):
        self.id = id
        self.data = None
        self.output = []

    def run(self):
            init_time = time.time()

            fig, ax = plt.subplots()
            ax.axis('off')

            self.output = []

            for i in range(1, 81):
                if self.working is True:
                    if i <= 40:
                        name = 't'
                        k = i
                    else:
                        name = 'g'
                        k = i - 40

                    # data plot xlim, ylim synchronization
                    if name == 't':
                        ax.set_ylim([10, 70])
                    else:
                        ax.set_ylim([-20, 40])

                    ax.plot(self.data[name + str(k).zfill(2)][-30:], 'b')
                    fig.savefig('model_input_image/now_data_' + str(self.id).zfill(2) + "_" + name + "_" + str(k).zfill(2) + '.png', transparent=True)
                    ax.lines.pop(0)
                    # self.f.seek(0)

                    img = tf.keras.preprocessing.image.load_img('model_input_image/now_data_' + str(self.id).zfill(2) + "_" + name + "_" + str(k).zfill(2) + '.png', target_size=(256, 256))
                    # os.remove('data_image/now_data_' + str(self.id).zfill(2) + "_" + name + "_" + str(k).zfill(2) + '.png')

                    img_array = tf.keras.preprocessing.image.img_to_array(img)
                    img_array = tf.expand_dims(img_array, 0)  # Create a batch

                    predictions = model.predict(img_array)
                    output = np.argmax(tf.nn.softmax(predictions[0]))
                    self.output.append(output)
                else:
                    print(str(self.id) + "_Thread is Dead")

            if self.working is True:
                print("ID : " + str(self.id) + ", Time : " + str(time.time()-init_time) + ", thread is END")
                self.analy_output.emit(self.output, str(time.strftime("%H:%M:%S", time.localtime(time.time()))))

class analy_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.init_value()

    def init_value(self):
        for i in range(1, 10):
            globals()['cf_thread_{}'.format(str(i).zfill(2))] = classification_thread()
            exec("cf_thread_" + str(i).zfill(2) + ".analy_output.connect(self.result)")
            exec("cf_thread_" + str(i).zfill(2) + ".arg_(" + str(i) + ")")

        self.alive_thread_number    = 0
        self.warning_start_point    = False
        self.warning_count          = 0
        self.fire_count             = 0
        self.savetime               = 'zero'
        self.output                 = 'Nomal'

    def start(self, data):
        if len(data['x']) >= 30:
            for i in range(1, 10):
                exec("self.alive = cf_thread_" + str(i).zfill(2) + ".isRunning()")

                if self.alive is False:
                    exec("cf_thread_" + str(i).zfill(2) + ".working = True")
                    exec("cf_thread_" + str(i).zfill(2) + ".data = data")
                    exec("cf_thread_" + str(i).zfill(2) + ".start()")
                    exec("print(str(cf_thread_" + str(i).zfill(2) + ".id) + 'ID thread start')")
                    self.alive_thread_number += 1
                    break

    def result(self, output, end_time):
        self.end_time = end_time
        if 1 in output and self.warning_start_point is False:
            self.warning_start_point = True
            self.warning_count += 1
            self.fire_count += 1
            print("이상 탐지")
            self.analysis_log(end_time, 'Start')
            self.savetime = end_time
            self.output = "Start"

        elif self.warning_start_point is True and self.warning_count < 5:
            self.warning_count += 1
            if 1 in output:
                self.fire_count += 1
            print("분석 중, ", self.warning_count)
            self.output = "Doing"

        elif self.warning_start_point is True and self.warning_count >= 5:
            # 분석 결과 비화재 인 경우 카운트 & 시작 위치 초기화 O
            # 분석 결과 화재인 경우 카운트 & 시작 위치 초기화 X
            self.warning_start_point is False
            self.warning_count = 0

            if self.fire_count >= 3:
                print("분석 종료, 화재 발생")
                self.analysis_log(end_time, 'Fire')
                self.output = "Fire"
            else:
                print("분석 종료, 이상치")
                self.analysis_log(end_time, "Outlier")
                self.output = "Outlier"
        else:
            self.output = "Nomal"

    def kill_thread(self):
        for i in range(1, 16):
            exec("self.now_alive = cf_thread_" + str(i).zfill(2) + ".isRunning()")
            if self.now_alive is True:
                exec("cf_thread_" + str(i).zfill(2) + ".working = False")

    def analysis_log(self, time, log):
        self.ui.analysis_log_table.setRowCount(self.ui.analysis_log_table.rowCount() + 1)
        for i in range(2):
            if i == 0:
                self.table_item = time
            if i == 1:
                self.table_item = log
            self.ui.analysis_log_table.setItem(self.ui.analysis_log_table.rowCount() - 1, i, QTableWidgetItem(self.table_item))
        self.ui.analysis_log_table.scrollToBottom()