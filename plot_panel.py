class plot_panel:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def value_change_event(self, data):
        if len(data['x']) >= 2:
            for k, v in data.items():
                if k == 'x':
                    continue
                exec("self.ui." + k + "_lb.setText(str('{:.1f}'.format(round(data['" + k + "'][-1], 1))))")
                if v[-2] > v[-1]:
                    exec("self.ui." + k + "_lb.setStyleSheet('background-color:None; border: None; color:rgb(0,0,255)')")
                elif v[-2] < v[-1]:
                    exec("self.ui." + k + "_lb.setStyleSheet('background-color:None; border: None; color:rgb(255,0,0)')")
                else:
                    exec("self.ui." + k + "_lb.setStyleSheet('background-color:None; border: None; color:rgb(0,0,0)')")
        else:
            for k, v in data.items():
                if k == 'x':
                    continue
                exec("self.ui." + k + "_lb.setText(str('{:.1f}'.format(round(data['" + k + "'][-1], 1))))")






