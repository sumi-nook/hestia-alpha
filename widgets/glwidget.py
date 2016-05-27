# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.WGL import *

from qt import pyqtSignal
from qt import QGLWidget

from gl.context import DrawContext
from gl.environment import GlobalEnvironment


class OpenGLWidget(QGLWidget):

    ready = pyqtSignal(DrawContext)

    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.initialized = False
        self.objects = []
        self.ctx = DrawContext()

    def initializeGL(self):
        if not self.initialized:
            # set global env info
            self.ctx.genv = GlobalEnvironment()
            self.initialized = True
            self.ready.emit(self.ctx)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

    def resizeGL(self, width, height):
        w, h = width, height
        self.ctx.width = w
        self.ctx.height = h
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        for obj in self.objects:
            obj.draw(self.ctx)

    def appendObject(self, obj):
        self.objects.append(obj)

    def flush(self):
        self.updateGL()
