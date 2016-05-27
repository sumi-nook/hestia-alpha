# -*- coding: utf-8 -*-

from OpenGL.GL import *

from .base import DrawObject


class Wrapper(DrawObject):
    def __init__(self, obj):
        self.object = obj

    def draw(self, ctx):
        self.object.draw(ctx)


class ColorWrapper(Wrapper):
    def __init__(self, r, g, b, obj):
        super(ColorWrapper, self).__init__(obj)
        self.r = r
        self.g = g
        self.b = b

    def draw(self, ctx):
        glColor3d(self.r, self.g, self.b)
        super(ColorWrapper, self).draw(ctx)

    def setColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @property
    def red(self):
        return self.r

    @red.setter
    def red(self, r):
        self.r = r

    @property
    def green(self):
        return self.g

    @green.setter
    def green(self, g):
        self.g = g

    @property
    def blue(self):
        return self.b

    @blue.setter
    def blue(self, b):
        self.b = b


class RasterPosWrapper(Wrapper):
    def __init__(self, x, y, obj):
        super(RasterPosWrapper, self).__init__(obj)
        self.x = x
        self.y = y

    def draw(self, ctx):
        glRasterPos(self.x, self.y)
        super(RasterPosWrapper, self).draw(ctx)

    def setPos(self, x, y):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y
