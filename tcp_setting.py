from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox

tcp_setting_dialog = uic.loadUiType("ui/tcp_setting_form.ui")[0]

class tcp_set(QDialog, tcp_setting_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui_init()
        self.var_init()
        self.event_init()

    def ui_init(self):
        self.buttonBox.setEnabled(False)

    def var_init(self):
        #기본 설정 이름 = 'Auto'
        self.now_set_num    = 0
        self.set_list       = []

    def event_init(self):
        #라디오 버튼 이벤트 Init
        self.auto_setting_btn.clicked.connect(self.tcp_arg_set)
        self.A_setting_btn.clicked.connect(self.tcp_arg_set)
        self.B_setting_btn.clicked.connect(self.tcp_arg_set)
        self.C_setting_btn.clicked.connect(self.tcp_arg_set)

    def tcp_arg_set(self):
        #라디오 버튼에 따른 세팅값 가져오기
        if self.auto_setting_btn.isChecked(): self.now_set_num = 0
        if self.A_setting_btn.isChecked():    self.now_set_num = 1
        if self.B_setting_btn.isChecked():    self.now_set_num = 2
        if self.C_setting_btn.isChecked():    self.now_set_num = 3

        self.ip         = self.setting_table.item(self.now_set_num, 0)
        self.buf        = self.setting_table.item(self.now_set_num, 1)
        self.port       = self.setting_table.item(self.now_set_num, 2)
        self.master_id  = self.setting_table.item(self.now_set_num, 3)
        self.slave_id   = self.setting_table.item(self.now_set_num, 4)
        self.serial_num = self.setting_table.item(self.now_set_num, 5)

        # 세팅값 리스트
        self.arg_list = [self.ip.text(), self.buf.text(), self.port.text(), self.master_id.text(), self.slave_id.text(), self.serial_num.text()]        
        print("ModbusTCP 세팅값 : ", self.arg_list)
        if '' in self.arg_list:
            self.buttonBox.setEnabled(False)
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("텍스트 오류")
            msgBox.setInformativeText("빈칸을 채워주세요")
            msgBox.setStandardButtons(QMessageBox.Yes)
            msgBox.setDefaultButton(QMessageBox.Yes)
            msgBox.exec_()
        else:
            self.buttonBox.setEnabled(True)
    
