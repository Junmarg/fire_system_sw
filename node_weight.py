class weight_checker:
    def __init__(self):
        super().__init__()
        self.var_init()
    def var_init(self):
        self.node = {
            # Escape Node
            'escape01': {},
            'escape02': {},
            'escape03': {},
            'escape04': {},

            # 1 Floor room
            'room01': {'middle01': 2},
            'room02': {'middle02': 2},
            'room03': {'middle03': 2, 'escape03': 1},
            'room04': {'middle04': 2},
            'room05': {'middle05': 2},
            'room06': {'middle01': 2},
            'room07': {'middle02': 2},
            'room08': {'middle03': 2, 'escape04': 1},
            'room09': {'middle04': 2},
            'room10': {'middle05': 2},

            # 1 Floor middle
            'middle01': {'room01': 3, 'room06': 3, 'middle02': 2, 'stair01': 1},
            'middle02': {'room02': 3, 'room07': 3, 'middle01': 2, 'middle03': 2},
            'middle03': {'room03': 3, 'room08': 3, 'middle02': 2, 'middle04': 2},
            'middle04': {'room04': 3, 'room09': 3, 'middle03': 2, 'middle05': 2},
            'middle05': {'room05': 3, 'room10': 3, 'middle04': 2, 'stair02': 1},

            # 1 Floor Stair
            'stair01': {'escape01': 1, 'middle01': 3, 'stair03': 5},
            'stair02': {'escape02': 1, 'middle05': 3, 'stair04': 5},

            ###########################################################################################
            ###########################################################################################

            # 2 Floor room
            'room11': {'middle06': 2},
            'room12': {'middle07': 2},
            'room13': {'middle08': 2},
            'room14': {'middle09': 2},
            'room15': {'middle10': 2},
            'room16': {'middle06': 2},
            'room17': {'middle07': 2},
            'room18': {'middle08': 2},
            'room19': {'middle09': 2},
            'room20': {'middle10': 2},

            # 2 Floor middle
            'middle06': {'room11': 3, 'room16': 3, 'middle07': 2, 'stair03': 1},
            'middle07': {'room12': 3, 'room17': 3, 'middle06': 2, 'middle08': 2},
            'middle08': {'room13': 3, 'room18': 3, 'middle07': 2, 'middle09': 2},
            'middle09': {'room14': 3, 'room19': 3, 'middle08': 2, 'middle10': 2},
            'middle10': {'room15': 3, 'room20': 3, 'middle09': 2, 'stair04': 1},

            # 2 Floor Stair
            'stair03': {'middle06': 2, 'stair01': 1, 'stair05': 3},
            'stair04': {'middle10': 2, 'stair02': 1, 'stair06': 3},

            ###########################################################################################
            ###########################################################################################

            # 3 Floor room
            'room21': {'middle11': 2},
            'room22': {'middle12': 2},
            'room23': {'middle13': 2},
            'room24': {'middle14': 2},
            'room25': {'middle15': 2},
            'room26': {'middle11': 2},
            'room27': {'middle12': 2},
            'room28': {'middle13': 2},
            'room29': {'middle14': 2},
            'room30': {'middle15': 2},

            # 3 Floor middle
            'middle11': {'room21': 3, 'room26': 3, 'middle12': 2, 'stair05': 1},
            'middle12': {'room22': 3, 'room27': 3, 'middle11': 2, 'middle13': 2},
            'middle13': {'room23': 3, 'room28': 3, 'middle12': 2, 'middle14': 2},
            'middle14': {'room24': 3, 'room29': 3, 'middle13': 2, 'middle15': 2},
            'middle15': {'room25': 3, 'room30': 3, 'middle14': 2, 'stair06': 1},

            # 3 Floor Stair
            'stair05': {'middle11': 2, 'stair03': 1, 'stair07': 3},
            'stair06': {'middle15': 2, 'stair04': 1, 'stair08': 3},

            ###########################################################################################
            ###########################################################################################

            # 4 Floor room
            'room31': {'middle16': 2},
            'room32': {'middle17': 2},
            'room33': {'middle18': 2},
            'room34': {'middle19': 2},
            'room35': {'middle20': 2},
            'room36': {'middle16': 2},
            'room37': {'middle17': 2},
            'room38': {'middle18': 2},
            'room39': {'middle19': 2},
            'room40': {'middle20': 2},

            # 4 Floor middle
            'middle16': {'room31': 3, 'room36': 3, 'middle17': 2, 'stair07': 1},
            'middle17': {'room32': 3, 'room37': 3, 'middle16': 2, 'middle18': 2},
            'middle18': {'room33': 3, 'room38': 3, 'middle17': 2, 'middle19': 2},
            'middle19': {'room34': 3, 'room39': 3, 'middle18': 2, 'middle20': 2},
            'middle20': {'room35': 3, 'room40': 3, 'middle19': 2, 'stair08': 1},

            # 4 Floor Stair
            'stair07': {'middle16': 2, 'stair05': 1},
            'stair08': {'middle20': 2, 'stair06': 1},
        }

        # default None
        # Temp caution -> 50, Warnning -> 70
        # Gas  caution -> 5 , Warnning -> 15
        self.node_danger_level = {'Stair01': None, 'Stair02': None, 'Stair03': None, 'Stair04': None,
                                  'Stair05': None, 'Stair06': None, 'Stair07': None, 'Stair08': None,
                                  'Stair09': None, 'Stair10': None, 'Stair11': None, 'Stair12': None,
                                  'Stair13': None, 'Stair14': None, 'Stair15': None, 'Stair16': None}
    def danger_check(self, data):
        for key, value in data.items():
            if key[0] == 't':
                if value[-1] >= 50.0:
                    self.weight_change(key[1:3], value[-1])
                    #self.fire_door_level(key, 'caution')
                if value[-1] >= 80.0:
                    self.weight_change(key[1:3], value[-1])
                    #self.fire_door_level(key, 'warning')
            if key[0] == 'g':
                if value[-1] >= 5.0:
                    self.weight_change(key[1:3], value[-1])
                    #self.fire_door_level(key, 'caution')
                if value[-1] >= 15.0:
                    self.weight_change(key[1:3], value[-1])
                    #self.fire_door_level(key, 'warning')
        return self.node

    def weight_change(self, node_number, value):
        # node_number is Room Start number
        if int(node_number) <= 10:
            set_node = 'middle' + str(int(node_number) % 5).zfill(2)
        elif int(node_number) <= 20:
            set_node = 'middle' + str(int(node_number) % 5 + 5).zfill(2)
        elif int(node_number) <= 30:
            set_node = 'middle' + str(int(node_number) % 5 + 10).zfill(2)
        else:
            set_node = 'middle' + str(int(node_number) % 5 + 15).zfill(2)

        for key, value in self.node.items():
            if key == set_node:
                for fire_node, weight in self.node[key].items():
                    self.node[key][fire_node] = 10
            for k, v in value.items():
                if k == set_node:
                    self.node[key][k] = 10

    def fire_door(self, key, level):
        print(key, level)