from PyQt5.QtCore           import QRect, Qt
from OpenGL.GL              import *
from OpenGL.GLU             import *
from PyQt5.QtWidgets        import *
from GL.source_gl   import gl_draw
from GL.react_gl    import eva_draw

class build_gl(QOpenGLWidget):
    left_mouse_press = False
    right_mouse_press = False
    trans_pos_x, trans_pos_y, trans_pos_z = (0, 0, 0)
    y_angle, z_angle = 1, 1

    # camera
    last_pos_x, last_pos_y, last_pos_z = 0.0, 5.0, -5.0

    # object move
    move_last_pos_x, move_last_pos_y, move_last_pos_z = 0.0, 0.0, 0.0
    trans_pos_x, trans_pos_y, trans_pos_z = 0, 0, 0

    def initializeGL(self):
        self.var_init()
        glPolygonMode(GL_FRONT, GL_FILL)
        glPolygonMode(GL_BACK, GL_FILL)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glShadeModel(GL_SMOOTH)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_NORMALIZE)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

    def ui_init(self, ui):
        self.ui = ui

    def var_init(self):
        self.setGeometry(QRect(20, 50, 831, 411))
        self.gl_draw = gl_draw()
        self.eva_draw = eva_draw()
        self.data = None
        self.ui.route_change_btn.clicked.connect(self.route_change)
        self.output = None

    def resizeGL(self, w, h):
        glGetError()

        aspect = w if (h == 0) else w / h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(45, aspect, 0.1, 1000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def mouseMoveEvent(self, event):
        if self.left_mouse_press == True:
            if abs(event.x() - self.move_last_pos_x) > abs(event.y() - self.move_last_pos_y):
                if event.x() < self.move_last_pos_x:
                    self.trans_pos_x -= 0.1
                else:
                    self.trans_pos_x += 0.1
            else:
                if event.y() < self.move_last_pos_y:
                    self.trans_pos_y += 0.1
                else:
                    self.trans_pos_y -= 0.1
        elif self.right_mouse_press == True:
            if abs(abs(event.x()) - abs(self.move_last_pos_x)) > abs(abs(event.y()) - abs(self.move_last_pos_y)):
                if event.x() < self.move_last_pos_x:
                    self.z_angle -= 2
                else:
                    self.z_angle += 2
            elif abs(abs(event.x()) - abs(self.move_last_pos_x)) == abs(abs(event.y()) - abs(self.move_last_pos_y)):
                pass
            else:
                if event.y() < self.move_last_pos_y:
                    self.y_angle -= 2
                else:
                    self.y_angle += 2
        self.move_last_pos_x = event.x()
        self.move_last_pos_y = event.y()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.trans_pos_z -= 0.5
        else:
            if self.trans_pos_z < 6.5:
                self.trans_pos_z += 0.5

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.right_mouse_press = True
            self.move_last_pos_x = event.x()
            self.move_last_pos_y = event.y()
        if event.button() == Qt.LeftButton:
            self.left_mouse_press = True
            self.move_last_pos_x = event.x()
            self.move_last_pos_y = event.y()

    def mouseReleaseEvent(self, event):
        self.left_mouse_press   = False
        self.right_mouse_press  = False

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(0.0, -8.0, 3,
                  0.0, 1.0, 0.9,
                  0.0, 0.0, 1.0)

        glTranslatef(self.trans_pos_x, self.trans_pos_z, self.trans_pos_y)
        glRotatef(self.y_angle, 1, 0, 0)
        glRotatef(self.z_angle, 0, 0, 1)

        glPushMatrix()

        self.gl_draw.build_draw()

        if self.output == 'Fire':
            self.eva_draw.draw_eva(self.data)
            self.eva_draw.obj_draw()
            self.gl_draw.start_filed()
            #self.eva_draw.create_site_set()
        glPopMatrix()
        glFinish()

        self.update()

    def route_change(self):
        if int(self.eva_draw.start_node[-2:]) >= 40:
            self.eva_draw.start_node = 'room01'
        else:
            self.eva_draw.start_node = 'room' + str(int(self.eva_draw.start_node[-2:]) + 1).zfill(2)

