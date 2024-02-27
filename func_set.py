from get_data           import get_data
from tcp_setting        import tcp_set
from simul_setting      import simul_set
from PyQt5.QtCore       import QTimer, QTime
from PyQt5.QtWidgets    import QHeaderView

class func_set:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.ui_init()
        self.func_init()
        self.event_init()

    def ui_init(self):
        self.ui.thread_start_btn.setEnabled(False)
        self.ui.get_data_mode_check.setChecked(False)
        self.ui.simulator_mode_check.setChecked(False)

        system_table = self.ui.system_log_table
        react_table = self.ui.react_log_table
        analysis_table = self.ui.analysis_log_table
        header = system_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header = react_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header = analysis_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def func_init(self):
        self.gd     = get_data(self.ui)
        self.gds    = tcp_set()
        self.sms    = simul_set()
        self.timer_event()

    def event_init(self):
        self.ui.get_data_mode_check.clicked.connect(self.event_print)
        self.ui.simulator_mode_check.clicked.connect(self.event_print)
        self.ui.thread_start_btn.clicked.connect(self.gd.worker_start)

    def event_print(self):
        if self.ui.get_data_mode_check.isChecked(): 
            print("-TCP/IP Mode Checked")
            if self.gds.exec_():
                self.gd.tcp_arg_input(self.gds.arg_list)
                self.ui.thread_start_btn.setEnabled(True)
            else:
                print("!REJECT")
                self.ui.thread_start_btn.setEnabled(False)
                self.ui.get_data_mode_check.setAutoExclusive(False)
                self.ui.get_data_mode_check.setChecked(False)
                self.ui.get_data_mode_check.setAutoExclusive(True)

        elif self.ui.simulator_mode_check.isChecked(): 
            print("-Simulator Mode Checked")
            if self.sms.exec_():
                self.gd.simul_arg_input(self.sms.dic)
                self.ui.thread_start_btn.setEnabled(True)
            else:
                print("!REJECT")
                self.ui.thread_start_btn.setEnabled(False)
                self.ui.simulator_mode_check.setAutoExclusive(False)
                self.ui.simulator_mode_check.setChecked(False)
                self.ui.simulator_mode_check.setAutoExclusive(True)

    def timer_event(self):
        self.clock = QTimer()
        self.clock.setInterval(1000)
        self.clock.timeout.connect(self.clock_text)
        self.clock.start()

    def clock_text(self):
        currentTime = QTime.currentTime().toString("hh:mm:ss")
        self.ui.time_label.setText(currentTime)
