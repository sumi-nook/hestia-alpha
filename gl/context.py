# -*- coding: utf-8 -*-

import os

from OpenGL.GL import *
from OpenGL.GLU import *

from .base import Point
from .base import Point3D
from .font import FontRegistry


class DrawContext(object):
    def __init__(self):
        """
        @note OpenGL初期化後に呼び出す必要があります。
        """
        self.genv = None
        self.width = 0
        self.height = 0
        self.fontRegistry = FontRegistry()
        self.raster = Point(0, 0)
        self.translated = Point3D(0, 0, 0)

    def ortho2D(self):
        gluOrtho2D(0, self.width, 0, self.height)

    @property
    def genv(self):
        return self.__genv

    @genv.setter
    def genv(self, genv):
        self.__genv = genv

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height


class BlendContext(object):

    Alpha = (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    Reverse = (GL_ONE_MINUS_DST_COLOR, GL_ZERO)
    Add = (GL_ONE, GL_ONE)
    AddAlpha = (GL_SRC_ALPHA, GL_ONE)
    Screen = (GL_ONE_MINUS_DST_COLOR, GL_ONE)
    Multiplication = (GL_ZERO, GL_SRC_COLOR)

    def __init__(self, brends=Alpha):
        self.brends = brends

    def __enter__(self):
        glEnable(GL_BLEND)
        glBlendFunc(*self.brends)

    def __exit__(self, exc_type, exc_value, traceback):
        glDisable(GL_BLEND)
        return False if exc_type else True


class MatrixContext(object):
    def __enter__(self):
        glPushMatrix()

    def __exit__(self, exc_type, exc_value, traceback):
        glPopMatrix()
        return False if exc_type else True
