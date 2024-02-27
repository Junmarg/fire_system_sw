from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from pyModbusTCP.client import ModbusClient
from analy_data         import analy_data
from plot_data          import plot_data
from GL.build_gl        import build_gl
from node_weight        import weight_checker
from plot_panel         import plot_panel
import time
import datetime
import pyautogui
import serial

class simulation_thread(QThread):
    # Simulation Thread
    data_sig = pyqtSignal(object, object, object)
    end_sig = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.var_init()
    
    def var_init(self):
        self.working    = False
        self.speed      = 2
        self.arg_list   = {}

        dic0 = {'x': []}
        dic1 = {'t' + str(x).zfill(2): [] for x in range(1, 41)}
        dic2 = {'g' + str(x).zfill(2): [] for x in range(1, 41)}
        dic0.update(dic1)
        dic0.update(dic2)

        self.dic        = dic0      # Data Dictionary
        self.dic_backup = dic0      # Data Dictionary Backup
        self.last_dic = {'t': [], 'g': []}

    def run(self):

        index = 0

        while self.working:
            if index < len(self.arg_list['t01']):
                for k, v in self.arg_list.items():
                    if k == 'x':
                        self.dic[k].append(time.time())
                    else:
                        self.dic[k].append(v[index])

                self.last_dic['t'] = []
                self.last_dic['g'] = []

                for k, v in self.arg_list.items():
                    if k == 'x':
                        pass
                    elif k[0] == 't':
                        self.last_dic['t'].append(v[index])
                    else:
                        self.last_dic['g'].append(v[index])

                index += 1

                self.data_sig.emit(self.dic, self.last_dic, 'simulation')
                time.sleep(2)
            else:
                self.end_sig.emit(True)

class tcp_thread(QThread):
    # ModbusTCP Thread
    data_sig = pyqtSignal(object, object, object)
    end_sig = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.var_init()

    def var_init(self):
        self.working    = False
        self.speed      = 1         # Seconds
        self.arg_list   = []
        self.sensor_stack = 30

        dic0 = {'x': []}
        dic1 = {'t' + str(x).zfill(2): [] for x in range(1, 41)}
        dic2 = {'g' + str(x).zfill(2): [] for x in range(1, 41)}
        dic0.update(dic1)
        dic0.update(dic2)

        self.dic        = dic0      # Data Dictionary
        self.dic_backup = dic0      # Data Dictionary Backup
        self.last_dic   = {'t': [], 'g': []}

    def run(self):
        clientSocket = ModbusClient(host=self.arg_list[0], port=self.arg_list[2], unit_id=self.arg_list[3], debug=False)

        while self.working:
            if clientSocket.open():
                pass
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Error")
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setStandardButtons(QMessageBox.Yes)
                msgBox.setDefaultButton(QMessageBox.Yes)
                msgBox.setText("TCP 연결 오류")
                msgBox.setInformativeText("ModBusTCP 연결 실패")
                msgBox.exec_()
                break

            if clientSocket.is_open():
                real_data = clientSocket.read_input_registers(1000, 80)
                
                index = 0 
                for i in real_data:
                    if index % 4 == 0:
                        sensor_data = int(bin(i & 4095),2 )
                        real_data[index//4] = sensor_data / 10
                    index += 1
                
                if time.strftime('%H:%M:%S') == '00:00:00':
                    self.dic = self.dic_backup  # 00:00:00시 딕셔너리 초기화

                index = 0
                self.last_dic['t'] = []
                self.last_dic['g'] = []

                for i in range(1, 41):
                    if i % 4 == 0 and i <= 40:
                        self.dic['g' + str(i).zfill(2)].append(real_data[index])
                        self.last_dic['g'].append(real_data[index])
                        self.dic['t' + str(i).zfill(2)].append(real_data[index + 10])
                        self.last_dic['t'].append(real_data[index + 10])
                        index += 1

                    else:
                        if i == 1:
                            self.dic['x'].append(time.time())
                        self.dic['g' + str(i).zfill(2)].append(0)
                        self.last_dic['g'].append(0)
                        self.dic['t' + str(i).zfill(2)].append(30)
                        self.last_dic['t'].append(30)

                self.data_sig.emit(self.dic, self.last_dic, 'real')
            time.sleep(2)

        self.end_sig.emit(True)

class get_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.func_init()
        self.var_init()
        #self.serial_init()
        self.event_init()
       

    def func_init(self):
        self.pd     = plot_data(self.ui)
        self.ad     = analy_data(self.ui)
        self.bg     = build_gl(self.ui.centralwidget)
        self.bg.ui_init(self.ui)
        self.wc     = weight_checker()
        self.pp     = plot_panel(self.ui)

    def var_init(self): 
        self.tcp_worker     = tcp_thread()
        self.simul_worker   = simulation_thread()

    def event_init(self):   
        self.tcp_worker.data_sig.connect(self.data_analy)
        self.tcp_worker.end_sig.connect(self.thread_end)
        self.simul_worker.data_sig.connect(self.data_analy)
        self.simul_worker.end_sig.connect(self.thread_end)
        self.ui.route_comboBox.currentIndexChanged.connect(self.room_chagne_event)

    def serial_init(self):
       self.port = "COM9" 
       self.baud = 19200 
       self.ser = serial.Serial(self.port, self.baud, timeout=3)
       xdata = '[OFF]'
       self.ser.write(xdata.encode())
       self.bolck = 3

    def tcp_arg_input(self, arg_list):
        self.tcp_worker.arg_list = arg_list
        print("-tcp_arg_list ", self.tcp_worker.arg_list)
    
    def simul_arg_input(self, arg_list):
        self.simul_worker.arg_list = arg_list
        print("-sm_arg_dic ", self.simul_worker.arg_list)

    def worker_start(self):
        if self.ui.get_data_mode_check.isChecked():
            if self.tcp_worker.isRunning():
                self.thread_event_set_ui(False)
                self.tcp_worker.working = False
                self.system_log("TCP End")
                print("-tcp_worker End")
            else:
                self.thread_event_set_ui(True)
                self.tcp_worker.working = True
                self.tcp_worker.start()
                self.system_log("TCP start")
                print("-tcp_worker start")
        if self.ui.simulator_mode_check.isChecked():
            if self.simul_worker.isRunning():
                self.thread_event_set_ui(False)
                self.simul_worker.working = False
                self.system_log("Simulation end")
                print("-simul_worker End")
            else:
                self.thread_event_set_ui(True)
                self.simul_worker.working = True
                self.simul_worker.start()
                self.system_log("Simulation start")
                print("-simul_worker start")

    def thread_event_set_ui(self, state):
        if state == True:
            self.ui.thread_start_btn.setText("END")
            self.ui.get_data_mode_check.setEnabled(False)
            self.ui.simulator_mode_check.setEnabled(False)
        if state == False:
            self.ui.thread_start_btn.setText("START")
            self.ui.get_data_mode_check.setEnabled(True)
            self.ui.simulator_mode_check.setEnabled(True)

    def data_analy(self, data, last_data, mode):
        self.data_log(data)
        self.pp.value_change_event(data)
        self.ad.start(data)
        self.bg.data = self.wc.danger_check(data)

        if self.ad.output == 'Start':
            self.pd.output = 'Start'
        if self.ad.output == 'Fire':
            self.bg.output = 'Fire'
            self.pd.output = 'Fire'
            self.react_log()
        if self.ad.output == 'Outlier':
            self.pd.output = 'Outlier'
        self.pd.data_plot(data, last_data, mode)
        
    def thread_end(self, object):
        if object:
            self.thread_event_set_ui(False)
            self.ui.thread_start_btn.setEnabled(False)
            self.ui.get_data_mode_check.setAutoExclusive(False)
            self.ui.get_data_mode_check.setChecked(False)
            self.ui.get_data_mode_check.setAutoExclusive(True)

    def room_chagne_event(self):
        self.pd.line_graph_name = self.ui.route_comboBox.currentText()

    def data_log(self, log):
        self.ui.data_log_table.setRowCount(self.ui.data_log_table.rowCount() + 1)
        log_data = []
        for i in range(2):
            if i == 0:
                self.table_item = str(time.strftime("%H:%M:%S", time.localtime(time.time())))
            if i == 1:
                for k in log:
                    if k[0] == 'x':
                        continue
                    if k[0] == 't':
                        log_data.append(str(log[k][-1]))
                    if k[0] == 'g':
                        log_data.append(str(log[k][-1]))

                self.table_item = ','.join(log_data)
            self.ui.data_log_table.setItem(self.ui.data_log_table.rowCount() - 1, i, QTableWidgetItem(self.table_item))
        self.ui.data_log_table.scrollToBottom()

    def system_log(self, log):
        self.ui.system_log_table.setRowCount(self.ui.system_log_table.rowCount() + 1)
        for i in range(3):
            if i == 0:
                self.table_item = str(time.strftime("%H:%M:%S", time.localtime(time.time())))
            if i == 1:
                self.table_item = log
            self.ui.system_log_table.setItem(self.ui.system_log_table.rowCount() - 1, i, QTableWidgetItem(self.table_item))
        self.ui.system_log_table.scrollToBottom()

    def react_log(self):
        self.ui.react_log_table.setRowCount(self.ui.react_log_table.rowCount() + 1)
        for i in range(3):
            if i == 0:
                nowtime = str(time.strftime("%H:%M:%S", time.localtime(time.time())))
                self.table_item = nowtime
            if i == 1:
                self.table_item = "방화문 동작"
                data = '[ON]'
                self.ser.write(data.encode())
            if i == 2:
                self.table_item = str(datetime.datetime.strptime(nowtime, "%H:%M:%S") - datetime.datetime.strptime(self.ad.savetime, "%H:%M:%S")) + "초"
            self.ui.react_log_table.setItem(self.ui.react_log_table.rowCount() - 1, i, QTableWidgetItem(self.table_item))
        self.ui.react_log_table.setRowCount(self.ui.react_log_table.rowCount() + 1)

        for i in range(3):
            if i == 0:
                nowtime = str(time.strftime("%H:%M:%S", time.localtime(time.time())))
                self.table_item = nowtime
            if i == 1:
                self.table_item = "피난 경로 분석"
            if i == 2:
                self.table_item = str(datetime.datetime.strptime(nowtime, "%H:%M:%S") - datetime.datetime.strptime(self.ad.savetime, "%H:%M:%S")) + "초"
            self.ui.react_log_table.setItem(self.ui.react_log_table.rowCount() - 1, i, QTableWidgetItem(self.table_item))
        self.ui.react_log_table.scrollToBottom()
        pyautogui.screenshot('C:/Users/hbrain/PycharmProjects/pythonProject1/static/image/my_screenshot.png', region=(70, 100, 750, 350))