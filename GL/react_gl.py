from OpenGL.GL import *
import heapq
import pywavefront
import random

######################################## Fucntion ###########################################

class route_search:
    node_data = None
    def __init__(self):
        super().__init__()
    def search_path(self, graph, first):
        distance = {node: [float('inf'), first] for node in graph}
        distance[first] = [0, first]
        queue = []

        heapq.heappush(queue, [distance[first][0], first])

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if distance[current_node][0] < current_distance:
                continue

            for next_node, weight in graph[current_node].items():
                total_distance = current_distance + weight

                if total_distance < distance[next_node][0]:
                    # 다음 노드까지 총 거리와 어떤 노드를 통해서 왔는지 입력
                    distance[next_node] = [total_distance, current_node]
                    heapq.heappush(queue, [total_distance, next_node])
        # 마지막 노드부터 첫번째 노드까지 순서대로 출력
        path_list = []

        min_distance = []
        min_distance.append(distance['escape01'])
        min_distance.append(distance['escape02'])
        min_distance.append(distance['escape03'])
        min_distance.append(distance['escape04'])

        min_escape_num = min_distance.index(min(min_distance))
        last = 'escape' + str(min_escape_num + 1).zfill(2)

        path = last
        # ++
        path_list.append(last)
        path_output = last + ' -> '
        while distance[path][1] != first:
            # ++
            path_list.append(distance[path][1])
            path_output += distance[path][1] + ' -> '
            path = distance[path][1]
        path_list.append(first)
        path_output += first
        path_list.reverse()
        #print("path list : ", path_list)
        #print("path output : ", path_output)
        #print(distance)
        #return distance

        return path_list
    def search(self, node, start_node):
        return self.search_path(node, start_node)

class eva_draw:
    def __init__(self):
        super().__init__()
        self.var_init()
        self.obj_load()

    def var_init(self):
        self.rs = route_search()
        self.start_node = 'room12'
        self.path_floor = None
        self.door_counter = 0

    def eva_color(self, case):
        if case == 1:  # White
            glColor3f(0, 0, 1)

    def route_set(self, case, x, y, z, x_t=1, y_s=0, z_t=1, t='None'):
        # x_t = x 좌표 뒤집기
        # y_s = y 좌표 쉬프트
        # z_t = None
        # t = 화살표 방향 세팅

        x -= 2.2  # 전체 Object 중앙 정렬
        y -= 1.1  # 전체 Object 중앙 정렬

        # ROOM TO MIDDLE
        if case == 1:
            room_to_middle = [[0.55 + x, 0.9 + y + y_s, 0.01 + z],
                              [0.55 + x, 0.5 + y + y_s, 0.01 + z],
                              [0.65 + x, 0.5 + y + y_s, 0.01 + z],
                              [0.65 + x, 0.9 + y + y_s, 0.01 + z]]

            self.eva_color(1)
            glBegin(GL_QUADS)
            for i in range(4):
                glVertex3fv(room_to_middle[i])
            glEnd()

            if t == 'up':
                triangle = [[0.6 + x, 1.0 + y + y_s, 0.01 + z],
                            [0.5 + x, 0.9 + y + y_s, 0.01 + z],
                            [0.7 + x, 0.9 + y + y_s, 0.01 + z]]
            if t == 'down':
                triangle = [[0.6 + x, 0.4 + y + y_s, 0.01 + z],
                            [0.5 + x, 0.5 + y + y_s, 0.01 + z],
                            [0.7 + x, 0.5 + y + y_s, 0.01 + z]]
            glBegin(GL_TRIANGLES)
            for i in range(3):
                glVertex3fv(triangle[i])
            glEnd()
        # MIDDLE TO MIDDLE
        if case == 2:
            middle_to_middel = [[0.8 + x, 1.05 + y, 0.01 + z],
                                [0.8 + x, 0.95 + y, 0.01 + z],
                                [1.2 + x, 0.95 + y, 0.01 + z],
                                [1.2 + x, 1.05 + y, 0.01 + z]]
            self.eva_color(1)
            glBegin(GL_QUADS)
            for i in range(4):
                glVertex3fv(middle_to_middel[i])
            glEnd()

            if t == 'right':
                triangle = [[1.3 + x, 1.0 + y, 0.01 + z],
                            [1.2 + x, 1.1 + y, 0.01 + z],
                            [1.2 + x, 0.9 + y, 0.01 + z]]

            if t == 'left':
                triangle = [[0.7 + x, 1.0 + y, 0.01 + z],
                            [0.8 + x, 1.1 + y, 0.01 + z],
                            [0.8 + x, 0.9 + y, 0.01 + z]]
            glBegin(GL_TRIANGLES)
            for i in range(3):
                glVertex3fv(triangle[i])
            glEnd()
        # STAIR TO STAIR
        if case == 3:
            stair2stair_01 = [[(-0.075 + x) * x_t, 1.8 + y, 0.31 + z],
                              [(-0.075 + x) * x_t, 1.2 + y, 0.01 + z],
                              [(0.025 + x) * x_t, 1.2 + y, 0.01 + z],
                              [(0.025 + x) * x_t, 1.8 + y, 0.31 + z]]
            stair2stair_02 = [[(0.07 + x) * x_t, 1.8 + y, 0.35 + z],
                              [(0.07 + x) * x_t, 1.2 + y, 0.65 + z],
                              [(0.17 + x) * x_t, 1.2 + y, 0.65 + z],
                              [(0.17 + x) * x_t, 1.8 + y, 0.35 + z]]
            self.eva_color(1)
            glBegin(GL_QUADS)
            for i in range(4):
                glVertex3fv(stair2stair_01[i])
            for i in range(4):
                glVertex3fv(stair2stair_02[i])
            glEnd()

            if t == 'up':
                triangle_01 = [[(-0.025 + x) * x_t, 1.9 + y, 0.31 + z],
                               [(-0.125 + x) * x_t, 1.8 + y, 0.31 + z],
                               [(0.075 + x) * x_t, 1.8 + y, 0.31 + z]]
                triangle_02 = [[(0.12 + x) * x_t, 1.1 + y, 0.65 + z],
                               [(0.02 + x) * x_t, 1.2 + y, 0.65 + z],
                               [(0.22 + x) * x_t, 1.2 + y, 0.65 + z]]
            if t == 'down':
                triangle_01 = [[(-0.025 + x) * x_t, 1.1 + y, 0.01 + z],
                               [(-0.125 + x) * x_t, 1.2 + y, 0.01 + z],
                               [(0.075 + x) * x_t, 1.2 + y, 0.01 + z]]
                triangle_02 = [[(0.12 + x) * x_t, 1.9 + y, 0.35 + z],
                               [(0.02 + x) * x_t, 1.8 + y, 0.35 + z],
                               [(0.22 + x) * x_t, 1.8 + y, 0.35 + z]]

            glBegin(GL_TRIANGLES)
            for i in range(3):
                glVertex3fv(triangle_01[i])
            for i in range(3):
                glVertex3fv(triangle_02[i])
            glEnd()
        # MIDDLE TO STAIR
        if case == 4:
            middle_to_stair = [[(0.2 + x) * x_t, 1.05 + y, 0.01 + z],
                               [(0.2 + x) * x_t, 0.95 + y, 0.01 + z],
                               [(0.5 + x) * x_t, 0.95 + y, 0.01 + z],
                               [(0.5 + x) * x_t, 1.05 + y, 0.01 + z]]
            self.eva_color(1)
            glBegin(GL_QUADS)
            for i in range(4):
                glVertex3fv(middle_to_stair[i])
            glEnd()

            if t == 'right':
                triangle = [[(0.6 + x) * x_t, 1.0 + y, 0.01 + z],
                            [(0.5 + x) * x_t, 1.1 + y, 0.01 + z],
                            [(0.5 + x) * x_t, 0.9 + y, 0.01 + z]]
            if t == 'left':
                triangle = [[(0.1 + x) * x_t, 1.0 + y, 0.01 + z],
                            [(0.2 + x) * x_t, 1.1 + y, 0.01 + z],
                            [(0.2 + x) * x_t, 0.9 + y, 0.01 + z]]
            glBegin(GL_TRIANGLES)
            for i in range(3):
                glVertex3fv(triangle[i])
            glEnd()
        # STAIR TO ESCAPE(OUT)
        if case == 5:
            stair2out = [[(-0.3 + x) * x_t, 1.05 + y, 0.01 + z],
                         [(-0.3 + x) * x_t, 0.95 + y, 0.01 + z],
                         [(-0.1 + x) * x_t, 0.95 + y, 0.01 + z],
                         [(-0.1 + x) * x_t, 1.05 + y, 0.01 + z]]
            self.eva_color(1)
            glBegin(GL_QUADS)
            for i in range(4):
                glVertex3fv(stair2out[i])
            glEnd()
            if t == 'left':
                triangle = [[(-0.4 + x) * x_t, 1.0 + y, 0.01 + z],
                            [(-0.3 + x) * x_t, 1.1 + y, 0.01 + z],
                            [(-0.3 + x) * x_t, 0.9 + y, 0.01 + z]]
            glBegin(GL_TRIANGLES)
            for i in range(3):
                glVertex3fv(triangle[i])
            glEnd()
        # ROOM TO ESCAPE(OUT)
        if case == 6:
            room2out = [[2.15 + x,  0.0 + y + y_s, 0.01 + z],
                        [2.15 + x, -0.3 + y + y_s, 0.01 + z],
                        [2.25 + x, -0.3 + y + y_s, 0.01 + z],
                        [2.25 + x,  0.0 + y + y_s, 0.01 + z]]
            self.eva_color(1)
            glBegin(GL_QUADS)
            for i in range(4):
                glVertex3fv(room2out[i])
            glEnd()

            if t == 'up':
                triangle = [[2.20 + x, 2.6 + y, 0.01 + z],
                            [2.05 + x, 2.5 + y, 0.01 + z],
                            [2.35 + x, 2.5 + y, 0.01 + z]]
            if t == 'down':
                triangle = [[2.20 + x, -0.4 + y, 0.01 + z],
                            [2.05 + x, -0.3 + y, 0.01 + z],
                            [2.35 + x, -0.3 + y, 0.01 + z]]

            glBegin(GL_TRIANGLES)
            for i in range(3):
                glVertex3fv(triangle[i])
            glEnd()

    def test_draw(self):
        self.route_set(1, 0, 0, 0, t='up')
        self.route_set(1, 0, 0, 0, y_s=0.6, t='down')
        self.route_set(1, 0.8, 0, 0, t='up')
        self.route_set(2, 0, 0, 0, t='left')
        self.route_set(3, 0, 0, 0, t='up')
        self.route_set(3, 0, 0, 0, t='down')
        self.route_set(3, 0, 0, 0, x_t=-1, t='up')
        self.route_set(3, 0, 0, 0, x_t=-1, t='down')
        self.route_set(4, 0, 0, 0, t='left')
        self.route_set(5, 0, 0, 0, t='left')
        self.route_set(4, 0, 0, 0, x_t=-1, t='left')
        self.route_set(5, 0, 0, 0, x_t=-1, t='left')

    def draw_eva(self, node):
        if node is not None:
            path = self.rs.search(node, self.start_node)
            self.path_floor = []

            # 피난 경로 층 판단
            for k in path:
                if k[0] == 'r':  # Room
                    if int(k[-2:]) <= 10:
                        self.path_floor.append(1)
                    if 11 <= int(k[-2:]) <= 20:
                        self.path_floor.append(2)
                    if 21 <= int(k[-2:]) <= 30:
                        self.path_floor.append(3)
                    if 31 <= int(k[-2:]) <= 40:
                        self.path_floor.append(4)
                elif k[0] == 'm':  # Middle
                    if int(k[-2:]) <= 5:
                        self.path_floor.append(1)
                    if 6 <= int(k[-2:]) <= 10:
                        self.path_floor.append(2)
                    if 11 <= int(k[-2:]) <= 15:
                        self.path_floor.append(3)
                    if 16 <= int(k[-2:]) <= 20:
                        self.path_floor.append(4)
                elif k[0] == 's':  # Stair
                    if int(k[-2:]) <= 2:
                        self.path_floor.append(1)
                    if 3 <= int(k[-2:]) <= 4:
                        self.path_floor.append(2)
                    if 5 <= int(k[-2:]) <= 6:
                        self.path_floor.append(3)
                    if 7 <= int(k[-2:]) <= 8:
                        self.path_floor.append(4)
                elif k[0] == 'e':  # Escape
                    self.path_floor.append(1)

            for r in range(len(path) - 1):
                if path[r][0] == 'r':
                    if path[r + 1][0] == 'm':  # Room to Middle
                        if self.path_floor[r] == self.path_floor[r + 1]:
                            # Room 숫자에 따른 경로 표시
                            # room to middle == case 1
                            if int(path[r][-2:]) % 10 in (1, 2, 3, 4, 5):
                                if int(path[r][-2:]) % 5 == 0:
                                    self.route_set(1, 0.8 * 4, 0, 0.6 * (self.path_floor[r] - 1), y_s=0.6, t='down')
                                else:
                                    self.route_set(1, 0.8 * (int(path[r][-2:]) % 5 - 1), 0, 0.6 * (self.path_floor[r] - 1), y_s=0.6, t='down')
                            elif int(path[r][-2:]) % 10 in (6, 7, 8, 9):
                                self.route_set(1, 0.8 * (int(path[r][-2:]) % 5 - 1), 0, 0.6 * (self.path_floor[r] - 1), t='up')
                            elif int(path[r][-2:]) % 10 == 0:
                                self.route_set(1, 0.8 * 4, 0, 0.6 * (self.path_floor[r] - 1), t='up')
                    if path[r + 1][0] == 'e':  # Room to Escape
                        if path[r + 1][-2:] == '03':
                            self.route_set(6, 0, 0, 0, y_s=2.6, t='up')
                        elif path[r + 1][-2:] == '04':
                            self.route_set(6, 0, 0, 0, t='down')
                elif path[r][0] == 'm':
                    if path[r + 1][0] == 'm':  # Middle to Middle
                        if self.path_floor[r] == self.path_floor[r + 1]:
                            # Middle 숫자에 따른 경로 표시
                            # room to middle == case 2
                            if int(path[r][-2:]) > int(path[r + 1][-2:]):
                                self.route_set(2, 0.8 * (int(path[r][-2:]) % 5 - 2), 0, 0.6 * (self.path_floor[r] - 1), t='left')
                            elif int(path[r][-2:]) < int(path[r + 1][-2:]):
                                self.route_set(2, 0.8 * (int(path[r][-2:]) % 5 - 1), 0, 0.6 * (self.path_floor[r] - 1), t='right')
                    if path[r + 1][0] == 'r':  # Middle to Middle
                        print("None")  # Middle to Room , 창문 탈출 추가 필요
                    if path[r + 1][0] == 's':  # Middle to Stair
                        # Middle to Start == case 4
                        if self.path_floor[r] == self.path_floor[r + 1]:
                            if int(path[r + 1][-2:]) % 2 != 0:  # 중앙에서 좌측 계단
                                self.route_set(4, 0, 0, 0.6 * (self.path_floor[r] - 1), t='left')
                            elif int(path[r + 1][-2:]) % 2 == 0:  # 중앙에서 우측 계단
                                self.route_set(4, 0, 0, 0.6 * (self.path_floor[r] - 1), x_t=-1, t='left')
                elif path[r][0] == 's':
                    if path[r + 1][0] == 'm':  # Stair to Middle
                        if self.path_floor[r] == self.path_floor[r + 1]:
                            if int(path[r][-2:]) % 2 != 0:  # 좌측 계단에서 중앙으로
                                self.route_set(4, 0, 0, 0.6 * (self.path_floor[r] - 1), t='right')
                            elif int(path[r][-2:]) % 2 == 0:  # 우측 계단에서 중앙으로
                                self.route_set(4, 0, 0, 0.6 * (self.path_floor[r] - 1), x_t=-1, t='right')
                    if path[r + 1][0] == 'e':  # Stair to Escape(out)
                        if self.path_floor[r] == self.path_floor[r + 1]:
                            if int(path[r][-2:]) % 2 != 0:  # 좌측 계단에서 탈출구로
                                self.route_set(5, 0, 0, 0, t='left')
                            elif int(path[r][-2:]) % 2 == 0:  # 우측 계단에서 탈출구로
                                self.route_set(5, 0, 0, 0, x_t=-1, t='left')
                    if path[r + 1][0] == 's':  # Stair to Stair
                        if int(path[r][-2:]) % 2 != 0:  # 좌측 계단
                            if self.path_floor[r] > self.path_floor[r + 1]:  # 계단 내려갈 때
                                self.route_set(3, 0, 0, 0.6 * (self.path_floor[r + 1] - 1), t='down')
                            elif self.path_floor[r] < self.path_floor[r + 1]:  # 계단 올라갈 때
                                self.route_set(3, 0, 0, 0.6 * (self.path_floor[r + 1] - 1), t='up')
                        if int(path[r][-2:]) % 2 == 0:  # 우측 계단
                            if self.path_floor[r] > self.path_floor[r + 1]:  # 계단 내려갈 때
                                self.route_set(3, 0, 0, 0.6 * (self.path_floor[r + 1] - 1), x_t=-1, t='down')
                            elif self.path_floor[r] < self.path_floor[r + 1]:  # 계단 올라갈 때
                                self.route_set(3, 0, 0, 0.6 * (self.path_floor[r + 1] - 1), x_t=-1, t='up')

    def obj_load(self):
        global scene, scene_scale
        scene = pywavefront.Wavefront('obj/Realistic_White_Male_Low_Poly/Realistic_White_Male_Low_Poly.obj',
                                      collect_faces=True)
        scene_box = (scene.vertices[0], scene.vertices[0])

        for vertex in scene.vertices:
            min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
            max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
            scene_box = (min_v, max_v)

        scene_trans = [-(scene_box[1][i] + scene_box[0][i]) / 2 for i in range(3)]
        scaled_size = 0.4
        scene_size = [scene_box[1][i] - scene_box[0][i] for i in range(3)]
        max_scene_size = max(scene_size)
        scene_scale = [scaled_size / max_scene_size for i in range(3)]

    def obj_draw(self):
        if self.path_floor is not None:
            glTranslatef(0, 0, 0)
            glTranslatef(-1.6, -0.8, 0)

            if int(self.start_node[-2:]) % 10 in (1, 2, 3, 4, 5):
                glTranslatef(0.8 * ((int(self.start_node[-2:]) % 10) - 1), 1.6, 0.6 * (self.path_floor[0] - 1))
            else:
                if int(self.start_node[-2:]) % 10 != 0:
                    glTranslatef(0.8 * ((int(self.start_node[-2:]) % 5) - 1), 0, 0.6 * (self.path_floor[0] - 1))
                elif int(self.start_node[-2:]) % 10 == 0:
                    glTranslatef(0.8 * 4, 0, 0.6 * (self.path_floor[0] - 1))
            glScalef(*scene_scale)

            if int(self.start_node[-2:]) % 10 in (1, 2, 3, 4, 5):
                glRotatef(180.0, 0.0, 0.0, 1.0)
            glRotatef(90.0, 1.0, 0.0, 0.0)
            glRotatef(180.0, 0.0, 1.0, 0.0)



            for mesh in scene.mesh_list:
                glBegin(GL_TRIANGLES)
                glColor(0.5, 0, 0)

                for face in mesh.faces:
                    for vertex_i in face:
                        glVertex3f(*scene.vertices[vertex_i])

                glEnd()

    def fire_wall(self, a, b, c, color):
        x = -2.2
        y = -1.1
        z =  0.0
        fire_door = [[0.95 + x + a, 1.2 + y,  0.6 + z + c],
                     [0.95 + x + a, 1.2 + y,  0.5 + z + c],
                     [0.95 + x + a, 0.8 + y,  0.5 + z + c],
                     [0.95 + x + a, 0.8 + y,  0.6 + z + c]]

        glBegin(GL_QUADS)
        if color % random.randint(1, 3) == 0:
            glColor(0.55, 0.55, 0.55)                         # Light Slate Gray
        else:
            glColor(0.33, 0.33, 0.33)
        glVertex3fv(fire_door[0])
        glVertex3fv(fire_door[1])
        glVertex3fv(fire_door[2])
        glVertex3fv(fire_door[3])
        glEnd()

    def create_site_set(self):
        self.create_tmp = self.create(self.door_counter)
        if self.door_counter < 6:
            self.door_counter += 1

    def create(self, loop):
        for i in range(16):
            if i % 4 != 0:
                shirter_num = i % 4 - 1
                floor       = i // 4
            else:
                floor       = i // 4
                shirter_num = 3
            for k in range(0, loop):
                self.fire_wall(0.8 * shirter_num, 0.0, (0.6 * floor) - k * 0.1, i)