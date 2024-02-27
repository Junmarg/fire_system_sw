from OpenGL.GL import *

class gl_draw:
    def __init__(self):
        super().__init__()

    def build_draw(self):
        self.color()
        #self.bottom(-2.2, -1.1, 0.0)
        self.wall_unit(-2.2, -1.1, 0.0)
        self.floor_unit(-2.2, -1.1, 0.0)
        self.bottom_unit(-2.2, -1.1, 0.0)
        self.pillar_unit(-2.2, -1.1, 0.0)
        self.stair_unit(-2.2, -1.1, 0.0, 1)
        self.stair_unit(-2.2, -1.1, 0.0, -1)
    def wall_unit(self, x, y, z):
        ch = z
        for j in range(4):
            z = 0.6 * j + ch
            for i in range(5):
                self.wall_01_01(0.8 * i + x, 0.0 + y, 0.0 + z)      # 06 - 10번방 창문벽
            #for i in range(6):
            #    self.wall_01_02(0.8 * i + x, 0.0 + y, 0.0 + z)      # 06 - 10번방 옆벽
            self.wall_01_03(0.0 + x, 0.0 + y, 0.0 + z)              # 01 - 05번방 큰 창문벽
            self.wall_01_03(3.4 + x, 0.0 + y, 0.0 + z)              # 01 - 05번방 큰 창문벽
            for i in range(3):
                if j == 0 and i == 1:
                    pass
                else:
                    self.wall_01_04(0.8 * i + x, 0.0 + y, 0.0 + z)      # 01 - 05번방 큰 창문벽
            #self.wall_01_05(0 + x, 0 + y, 0 + z)                    # 01 - 05번방 짧은 옆벽
            #self.wall_01_06(0.8 * 4 + x + 0.2, 0.0 + y, 0.0 + z)
            #for i in range(5):
            #    if i == 4:
            #        self.wall_01_06(0.8 * i + x + 0.2, 0.0 + y, 0.0 + z)
            #    else:
            #        self.wall_01_06(0.8 * i + x, 0.0 + y, 0.0 + z)      # 01 - 05번방 긴 옆벽
    def floor_unit(self, x, y, z):
        ch = z
        for i in range(4):
            z = 0.6 * i + ch
            self.floor(0.0 + x, 0.0 + y, 0.0 + z)
    def bottom_unit(self, x, y, z):
        ch = z
        for i in range(4):
            z = 0.6 * i + ch
            for j in range(5):
                self.bottom_line_01_01(0.8 * j + x, 0.0 + y, 0.0 + z)
            self.bottom_line_01_03(0.0 + x, 0.0 + y, 0.0 + z)
            for j in range(3):
                self.bottom_line_01_04(0.8 * j + x, 0.0 + y, 0.0 + z)
            self.bottom_line_01_05(0.0 + x, 0.0 + y, 0.0 + z)
    def pillar_unit(self, x, y, z):
        ch = z
        for i in range(4):
            z = 0.6 * i + ch
            self.pillar_01(0.0 + x, 0.0 + y, 0.0 + z)
            self.pillar_02(0.0 + x, 0.0 + y, 0.0 + z)
            self.pillar_03(0.0 + x, 0.0 + y, 0.0 + z)
            self.pillar_04(0.0 + x, 0.0 + y, 0.0 + z)
    def stair_unit(self, x, y, z, r):
        #ch = z
        for i in range(3):
            #z = i0.6 *  + ch
            for j in range(11):
                self.stair_01(0.0 + x, 0.0 + y + (0.06 * j), 0.0 + z + (0.03 * j) + (0.6 * i), r)
            for k in range(11):
                self.stair_02(0.0 + x, 0.0 + y - (0.06 * k), 0.0 + z + (0.03 * k) + (0.6 * i), r)
            self.stair_03(0.0 + x, 0.0 + y, 0.0 + z + (0.6 * i), r)
    def color(self):
        self.wall_color = 0.7, 0.1, 0.1
    # OBJECT

    # BOTTOM

    def fire_zone(self, x, y, z):
        # 1층 06 - 10번방 바닥 라인
        fire_filed = [[0.2 + x, 2.2 + y, 0.61 + z],
                     [0.2 + x, 1.2 + y, 0.61 + z],
                     [1.0 + x, 1.2 + y, 0.61 + z],
                     [1.0 + x, 2.2 + y, 0.61 + z]]

        glBegin(GL_QUADS)
        glColor(1, 0, 0)
        for i in range(4):
            glVertex3fv(fire_filed[i])
        glEnd()

    def start_filed(self):
        self.fire_zone(-2.2, -1.1, 0.0)

    def bottom(self, x, y, z):
        # 건물 바닥
        bottom = [[0.0 + x, 2.2 + y, 0.0 + z],
                  [0.0 + x, 0.0 + y, 0.0 + z],
                  [4.4 + x, 0.0 + y, 0.0 + z],
                  [4.4 + x, 2.2 + y, 0.0 + z]]
        glColor3f(0.1, 0.1, 0.8)
        glBegin(GL_QUADS)
        for i in range(4):
            glVertex3fv(bottom[i])
        glEnd()

        bottom_02 = [[]]

    # WALL
    # 01_01 = 1층 06 - 10번방 창문벽
    # 01_02 = 1층 06 - 10번방 옆벽
    # 01_03 = 1층 01 - 05번방 큰 창문벽
    # 01_04 = 1층 01 - 05번방 창문벽
    # 01_05 = 1층 01 - 05번방 짧은 옆벽
    # 01_06 = 1층 01 - 05번방 옆벽
    # 01_07 = 1층 06 - 10번방 문 벽
    def wall_01_01(self, x, y, z):
        # 1층 06 - 10번방 창문벽
        wall_01_01  = [[0.2 + x, 0.0 + y, 0.6 + z],
                       [0.2 + x, 0.0 + y, 0.0 + z],
                       [1.0 + x, 0.0 + y, 0.0 + z],
                       [1.0 + x, 0.0 + y, 0.6 + z]]

        glBegin(GL_LINE_LOOP)
        glColor(0, 0, 0)
        for i in range(4):
            glVertex3fv(wall_01_01[i])
        glEnd()
    def wall_01_02(self, x, y, z):
        # 1층 06 - 10번방 옆벽
        wall_01_02  = [[0.2 + x, 0.8 + y, 0.6 + z],
                       [0.2 + x, 0.8 + y, 0.0 + z],
                       [0.2 + x, 0.0 + y, 0.0 + z],
                       [0.2 + x, 0.0 + y, 0.6 + z]]

        glBegin(GL_LINE_LOOP)
        glColor(0.7, 0.1, 0.1)
        for i in range(4):
            glVertex3fv(wall_01_02[i])
        glEnd()
    def wall_01_03(self, x, y, z):
        # 01_03 = 1층 01 - 05번방 큰 창문벽
        wall_01_03  = [[0.0 + x, 2.2 + y, 0.6 + z],
                       [0.0 + x, 2.2 + y, 0.0 + z],
                       [1.0 + x, 2.2 + y, 0.0 + z],
                       [1.0 + x, 2.2 + y, 0.6 + z]]

        glBegin(GL_QUADS)
        glColor(0.3, 0.3, 0.3)
        for i in range(4):
            glVertex3fv(wall_01_03[i])
        glEnd()
    def wall_01_04(self, x, y, z):
        # 1층 01 - 05번방 창문벽
        wall_01_04  = [[1.0 + x, 2.2 + y, 0.6 + z],
                       [1.0 + x, 2.2 + y, 0.0 + z],
                       [1.8 + x, 2.2 + y, 0.0 + z],
                       [1.8 + x, 2.2 + y, 0.6 + z]]

        glBegin(GL_QUADS)
        glColor(0.3, 0.3, 0.3)
        for i in range(4):
            glVertex3fv(wall_01_04[i])
        glEnd()
    def wall_01_05(self, x, y, z):
        # 1층 01 - 05번방 짧은 옆벽
        wall_01_05  = [[0.0 + x, 2.2 + y, 0.6 + z],
                       [0.0 + x, 2.2 + y, 0.0 + z],
                       [0.0 + x, 1.8 + y, 0.0 + z],
                       [0.0 + x, 1.8 + y, 0.6 + z]]

        glBegin(GL_QUADS)
        glColor(0.1, 0.4, 0.4)
        for i in range(4):
            glVertex3fv(wall_01_05[i])
        glEnd()
    def wall_01_06(self, x, y, z):
        # 1층 01 - 05번방 옆벽
        wall_01_06  = [[1.0 + x, 2.2 + y, 0.6 + z],
                       [1.0 + x, 2.2 + y, 0.0 + z],
                       [1.0 + x, 1.2 + y, 0.0 + z],
                       [1.0 + x, 1.2 + y, 0.6 + z]]

        glBegin(GL_QUADS)
        glColor(0.1, 0.4, 0.4)
        for i in range(4):
            glVertex3fv(wall_01_06[i])
        glEnd()
    def wall_01_07(self, x, y, z):
        # 1층 06 - 10번방 문 벽
        wall_01_01  = [[0.2 + x, 0.0 + y, 0.6 + z],
                       [0.2 + x, 0.0 + y, 0.0 + z],
                       [1.0 + x, 0.0 + y, 0.0 + z],
                       [1.0 + x, 0.0 + y, 0.6 + z]]

        glBegin(GL_LINE_LOOP)
        glColor(0.7, 0.1, 0.1)
        for i in range(4):
            glVertex3fv(wall_01_01[i])
        glEnd()
    # FLOOR
    # 2층부터
    def floor(self, x, y, z):
        # 공통 복도
        floor_01     = [[0.2 + x, 2.2 + y, 0.0 + z],
                        [0.2 + x, 0.0 + y, 0.0 + z],
                        [4.2 + x, 0.0 + y, 0.0 + z],
                        [4.2 + x, 2.2 + y, 0.0 + z]]
        floor_02    =  [[-0.1 + x, 1.2 + y, 0.0 + z],
                        [-0.1 + x, 0.8 + y, 0.0 + z],
                        [0.2 + x, 0.8 + y, 0.0 + z],
                        [0.2 + x, 1.2 + y, 0.0 + z]]
        floor_03    =  [[4.2 + x, 1.2 + y, 0.0 + z],
                        [4.2 + x, 0.8 + y, 0.0 + z],
                        [4.5 + x, 0.8 + y, 0.0 + z],
                        [4.5 + x, 1.2 + y, 0.0 + z]]

        glBegin(GL_QUADS)
        glColor(0.8, 0.8, 0.8)
        for j in range(4):
            glVertex3fv(floor_01[j])
        for j in range(4):
            glVertex3fv(floor_02[j])
        for j in range(4):
            glVertex3fv(floor_03[j])
        glEnd()
    # Window Wall
    # 01_01 = 1층 06 - 10번방 바닥 라인
    # 01_02 =
    # 01_03 = 1층 01 - 05번방 제일 왼쪽 큰 바닥 라인
    # 01_04 = 1층 01 - 05번방 가운데 세개 라인
    # 01_05 = 1층 01 - 05번방 제일 오른쪽 방 라인
    def bottom_line_01_01(self, x, y, z):
        # 1층 06 - 10번방 바닥 라인
        bottom_line_01_01 = [[0.2 + x, 0.8 + y, 0.0 + z],
                             [0.2 + x, 0.0 + y, 0.0 + z],
                             [1.0 + x, 0.0 + y, 0.0 + z],
                             [1.0 + x, 0.8 + y, 0.0 + z]]

        glBegin(GL_LINE_LOOP)
        glColor(0, 0, 0)
        for i in range(4):
            glVertex3fv(bottom_line_01_01[i])
        glEnd()
    def bottom_line_01_02(self, x, y, z):
        print("A")
    def bottom_line_01_03(self, x, y, z):
        # 1층 01 - 05번방 제일 왼쪽 큰 바닥 라인
        bottom_line_01_03 = [[0.2 + x, 2.2 + y, 0.0 + z],
                             [0.2 + x, 1.2 + y, 0.0 + z],
                             [1.0 + x, 1.2 + y, 0.0 + z],
                             [1.0 + x, 2.2 + y, 0.0 + z]]
        glBegin(GL_LINE_LOOP)
        glColor(0, 0, 0)
        for i in range(4):
            glVertex3fv(bottom_line_01_03[i])
        glEnd()
    def bottom_line_01_04(self, x, y, z):
        # 1층 01 - 05번방 가운데 세개 라인
        bottom_line_01_04 = [[1.0 + x, 2.2 + y, 0.0 + z],
                             [1.0 + x, 1.2 + y, 0.0 + z],
                             [1.8 + x, 1.2 + y, 0.0 + z],
                             [1.8 + x, 2.2 + y, 0.0 + z]]
        glBegin(GL_LINE_LOOP)
        glColor(0, 0, 0)
        for i in range(4):
            glVertex3fv(bottom_line_01_04[i])
        glEnd()
    def bottom_line_01_05(self, x, y, z):
        # 1층 01 - 05번방 제일 오른쪽 방 라인
        bottom_line_01_05 = [[3.4 + x, 2.2 + y, 0.0 + z],
                             [3.4 + x, 1.2 + y, 0.0 + z],
                             [4.2 + x, 1.2 + y, 0.0 + z],
                             [4.2 + x, 2.2 + y, 0.0 + z]]
        glBegin(GL_LINE_LOOP)
        glColor(0, 0, 0)
        for i in range(4):
            glVertex3fv(bottom_line_01_05[i])
        glEnd()

    # pillar
    # 01 = 좌하단
    # 02 = 좌상단
    # 03 = 우하단
    # 04 = 우상단
    def pillar_01(self, x, y, z):
        # 좌하단 기둥
        pillar_01_01 = [[0.0 + x, 0.2 + y, 0.0 + z],
                        [0.0 + x, 0.0 + y, 0.0 + z],
                        [0.2 + x, 0.0 + y, 0.0 + z],
                        [0.2 + x, 0.2 + y, 0.0 + z]]
        pillar_01_02 = [[0.0 + x, 0.2 + y, 0.6 + z],
                        [0.0 + x, 0.2 + y, 0.0 + z],
                        [0.0 + x, 0.0 + y, 0.0 + z],
                        [0.0 + x, 0.0 + y, 0.6 + z]]
        pillar_01_03 = [[0.0 + x, 0.0 + y, 0.6 + z],
                        [0.0 + x, 0.0 + y, 0.0 + z],
                        [0.2 + x, 0.0 + y, 0.0 + z],
                        [0.2 + x, 0.0 + y, 0.6 + z]]
        pillar_01_04 = [[0.2 + x, 0.2 + y, 0.6 + z],
                        [0.2 + x, 0.2 + y, 0.0 + z],
                        [0.2 + x, 0.0 + y, 0.0 + z],
                        [0.2 + x, 0.0 + y, 0.6 + z]]
        pillar_01_05 = [[0.0 + x, 0.2 + y, 0.6 + z],
                        [0.0 + x, 0.2 + y, 0.0 + z],
                        [0.2 + x, 0.2 + y, 0.0 + z],
                        [0.2 + x, 0.2 + y, 0.6 + z]]
        glBegin(GL_QUADS)
        glColor(0.4, 0.4, 0.4)
        for i in range(4):
            glVertex3fv(pillar_01_01[i])
        for i in range(4):
            glVertex3fv(pillar_01_02[i])
        for i in range(4):
            glVertex3fv(pillar_01_03[i])
        for i in range(4):
            glVertex3fv(pillar_01_04[i])
        for i in range(4):
            glVertex3fv(pillar_01_05[i])
        glEnd()
    def pillar_02(self, x, y, z):
        # 좌상단 기둥
        pillar_02_01 = [[0.0 + x, 2.2 + y, 0.0 + z],
                        [0.0 + x, 2.0 + y, 0.0 + z],
                        [0.2 + x, 2.0 + y, 0.0 + z],
                        [0.2 + x, 2.2 + y, 0.0 + z]]
        pillar_02_02 = [[0.0 + x, 2.2 + y, 0.6 + z],
                        [0.0 + x, 2.2 + y, 0.0 + z],
                        [0.0 + x, 2.0 + y, 0.0 + z],
                        [0.0 + x, 2.0 + y, 0.6 + z]]
        pillar_02_03 = [[0.0 + x, 2.0 + y, 0.6 + z],
                        [0.0 + x, 2.0 + y, 0.0 + z],
                        [0.2 + x, 2.0 + y, 0.0 + z],
                        [0.2 + x, 2.0 + y, 0.6 + z]]
        pillar_02_04 = [[0.2 + x, 2.2 + y, 0.6 + z],
                        [0.2 + x, 2.2 + y, 0.0 + z],
                        [0.2 + x, 2.0 + y, 0.0 + z],
                        [0.2 + x, 2.0 + y, 0.6 + z]]
        pillar_02_05 = [[0.0 + x, 2.2 + y, 0.6 + z],
                        [0.0 + x, 2.2 + y, 0.0 + z],
                        [0.2 + x, 2.2 + y, 0.0 + z],
                        [0.2 + x, 2.2 + y, 0.6 + z]]
        glBegin(GL_QUADS)
        glColor(0.4, 0.4, 0.4)
        for i in range(4):
            glVertex3fv(pillar_02_01[i])
        for i in range(4):
            glVertex3fv(pillar_02_02[i])
        for i in range(4):
            glVertex3fv(pillar_02_03[i])
        for i in range(4):
            glVertex3fv(pillar_02_04[i])
        for i in range(4):
            glVertex3fv(pillar_02_05[i])
        glEnd()
    def pillar_03(self, x, y, z):
        # 우하단
        pillar_03_01 = [[4.2 + x, 0.2 + y, 0.0 + z],
                        [4.2 + x, 0.0 + y, 0.0 + z],
                        [4.4 + x, 0.0 + y, 0.0 + z],
                        [4.4 + x, 0.2 + y, 0.0 + z]]
        pillar_03_02 = [[4.2 + x, 0.2 + y, 0.6 + z],
                        [4.2 + x, 0.2 + y, 0.0 + z],
                        [4.2 + x, 0.0 + y, 0.0 + z],
                        [4.2 + x, 0.0 + y, 0.6 + z]]
        pillar_03_03 = [[4.2 + x, 0.0 + y, 0.6 + z],
                        [4.2 + x, 0.0 + y, 0.0 + z],
                        [4.4 + x, 0.0 + y, 0.0 + z],
                        [4.4 + x, 0.0 + y, 0.6 + z]]
        pillar_03_04 = [[4.2 + x, 0.2 + y, 0.6 + z],
                        [4.2 + x, 0.2 + y, 0.0 + z],
                        [4.2 + x, 0.0 + y, 0.0 + z],
                        [4.2 + x, 0.0 + y, 0.6 + z]]
        pillar_03_05 = [[4.2 + x, 0.2 + y, 0.6 + z],
                        [4.2 + x, 0.2 + y, 0.0 + z],
                        [4.4 + x, 0.2 + y, 0.0 + z],
                        [4.4 + x, 0.2 + y, 0.6 + z]]
        glBegin(GL_QUADS)
        glColor(0.4, 0.4, 0.4)
        for i in range(4):
            glVertex3fv(pillar_03_01[i])
        for i in range(4):
            glVertex3fv(pillar_03_02[i])
        for i in range(4):
            glVertex3fv(pillar_03_03[i])
        for i in range(4):
            glVertex3fv(pillar_03_04[i])
        for i in range(4):
            glVertex3fv(pillar_03_05[i])
        glEnd()
    def pillar_04(self, x, y, z):
        # 좌상단 기둥
        pillar_04_01 = [[4.2 + x, 2.2 + y, 0.0 + z],
                        [4.2 + x, 2.0 + y, 0.0 + z],
                        [4.4 + x, 2.0 + y, 0.0 + z],
                        [4.4 + x, 2.2 + y, 0.0 + z]]
        pillar_04_02 = [[4.2 + x, 2.2 + y, 0.6 + z],
                        [4.2 + x, 2.2 + y, 0.0 + z],
                        [4.2 + x, 2.0 + y, 0.0 + z],
                        [4.2 + x, 2.0 + y, 0.6 + z]]
        pillar_04_03 = [[4.2 + x, 2.0 + y, 0.6 + z],
                        [4.2 + x, 2.0 + y, 0.0 + z],
                        [4.4 + x, 2.0 + y, 0.0 + z],
                        [4.4 + x, 2.0 + y, 0.6 + z]]
        pillar_04_04 = [[4.2 + x, 2.2 + y, 0.6 + z],
                        [4.2 + x, 2.2 + y, 0.0 + z],
                        [4.2 + x, 2.0 + y, 0.0 + z],
                        [4.2 + x, 2.0 + y, 0.6 + z]]
        pillar_04_05 = [[4.2 + x, 2.2 + y, 0.6 + z],
                        [4.2 + x, 2.2 + y, 0.0 + z],
                        [4.4 + x, 2.2 + y, 0.0 + z],
                        [4.4 + x, 2.2 + y, 0.6 + z]]
        glBegin(GL_QUADS)
        glColor(0.4, 0.4, 0.4)
        for i in range(4):
            glVertex3fv(pillar_04_01[i])
        for i in range(4):
            glVertex3fv(pillar_04_02[i])
        for i in range(4):
            glVertex3fv(pillar_04_03[i])
        for i in range(4):
            glVertex3fv(pillar_04_04[i])
        for i in range(4):
            glVertex3fv(pillar_04_05[i])
        glEnd()

    # stair
    # 01 = 오름 1 계단
    # 02 = 오름 2 계단
    # 03 = 중간 바닥
    # 높이 = 0.6, 가로 0.8
    # 높이 2.2, 1.2 = 2.0 ~ 1.4
    # 계단 10개
    def stair_01(self, x, y, z, r):
        # 오름 계단
        stair_01 = [[(4.5 + x) * r, 1.3 + y, 0.0 + z],
                    [(4.5 + x) * r, 1.2 + y, 0.0 + z],
                    [(4.35 + x) * r, 1.2 + y, 0.0 + z],
                    [(4.35 + x) * r, 1.3 + y, 0.0 + z]]

        glBegin(GL_QUADS)
        glColor(0.7, 0, 0)
        for i in range(4):
            glVertex3fv(stair_01[i])
        glEnd()
    def stair_02(self, x, y, z, r):
        # 오름 계단
        stair_02 = [[(4.2 + x) * r, 1.9 + y, 0.3 + z],
                    [(4.2 + x) * r, 1.8 + y, 0.3 + z],
                    [(4.35 + x) * r, 1.8 + y, 0.3 + z],
                    [(4.35 + x) * r, 1.9 + y, 0.3 + z]]

        glBegin(GL_QUADS)
        glColor(0.7, 0, 0)
        for i in range(4):
            glVertex3fv(stair_02[i])
        glEnd()
    def stair_03(self, x, y, z, r):
        # 중간 계단
        stair_03 = [[(4.2 + x) * r, 2.0 + y, 0.3 + z],
                    [(4.2 + x) * r, 1.9 + y, 0.3 + z],
                    [(4.5 + x) * r, 1.9 + y, 0.3 + z],
                    [(4.5 + x) * r, 2.0 + y, 0.3 + z]]

        glBegin(GL_QUADS)
        glColor(0.7, 0, 0)
        for i in range(4):
            glVertex3fv(stair_03[i])
        glEnd()

    def background(self):
        #MainWidget Transparency
        background_black = [[-15,  15, -15],
                            [-15, -15, -15],
                            [ 15, -15, -15],
                            [ 15,  15, -15],  #
                            [ 15,  15,  15],
                            [ 15,  15, -15],
                            [ 15, -15, -15],
                            [ 15, -15,  15],  #
                            [-15, -15,  15],
                            [-15, -15,  15],
                            [-15, -15,  15],
                            [-15, -15,  15],  #
                            [-15,  15,  15],
                            [-15,  15, -15],
                            [-15, -15, -15],
                            [-15, -15,  15],  #
                            [-15, -15,  15],
                            [-15, -15, -15],
                            [ 15, -15, -15],
                            [ 15, -15,  15],  #
                            [-15,  15,  15],
                            [-15,  15, -15],
                            [ 15,  15, -15],
                            [ 15,  15,  15]]

        glBegin(GL_QUADS)
        glColor(0,0,0)
        glVertex3fv(background_black[0])
        glVertex3fv(background_black[1])
        glVertex3fv(background_black[2])
        glVertex3fv(background_black[3])

        glVertex3fv(background_black[4])
        glVertex3fv(background_black[5])
        glVertex3fv(background_black[6])
        glVertex3fv(background_black[7])

        glVertex3fv(background_black[8])
        glVertex3fv(background_black[9])
        glVertex3fv(background_black[10])
        glVertex3fv(background_black[11])

        glVertex3fv(background_black[12])
        glVertex3fv(background_black[13])
        glVertex3fv(background_black[14])
        glVertex3fv(background_black[15])

        glVertex3fv(background_black[16])
        glVertex3fv(background_black[17])
        glVertex3fv(background_black[18])
        glVertex3fv(background_black[19])

        glVertex3fv(background_black[20])
        glVertex3fv(background_black[21])
        glVertex3fv(background_black[22])
        glVertex3fv(background_black[23])
        glEnd()