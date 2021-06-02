import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

from transformations import Transformer
from objloader import *

class Camera:

    def __init__(self):
        pygame.init()
        self.viewport = (800,600)
        self.height = self.viewport[0]
        self.width =  self.viewport[1]
        self.hx = self.viewport[0]/2
        self.hy = self.viewport[1]/2
        self.srf = pygame.display.set_mode(self.viewport, OPENGL | DOUBLEBUF)
        pygame.display.set_caption("Projeto Prático 3")
        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        self.clock = pygame.time.Clock()
        glMatrixMode(GL_PROJECTION)
        gluPerspective(90.0, self.width/float(self.height), 1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def insert_obj(self, obj_name):
        self.obj = OBJ(obj_name, swapyz=True)

    def render(self):
        rx, ry = (0,0)
        tx, ty = (0,0)
        zpos = 5
        rotate = move = False
        while 1:
            self.clock.tick(30)
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    sys.exit()
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 4: zpos = max(1, zpos-1)
                    elif e.button == 5: zpos += 1
                    elif e.button == 1: rotate = True
                    elif e.button == 3: move = True
                elif e.type == MOUSEBUTTONUP:
                    if e.button == 1: rotate = False
                    elif e.button == 3: move = False
                elif e.type == MOUSEMOTION:
                    i, j = e.rel
                    if rotate:
                        rx += i
                        ry += j
                    if move:
                        tx += i
                        ty -= j

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            # RENDER OBJECT
            glTranslate(tx/20., ty/20., - zpos)
            glRotate(ry, 1, 0, 0)
            glRotate(rx, 0, 1, 0)
            glCallList(self.obj.gl_list)

            pygame.display.flip()

