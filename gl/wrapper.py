# -*- coding: utf-8 -*-

from OpenGL.GL import *

from .base import DrawObject
from .base import Point
from .base import Point3D
from .context import BlendContext


class Wrapper(DrawObject):
    def __and__(self, rhs):
        if not isinstance(rhs, DrawObject):
            raise Exception("rhs is not DrawObject")
        return WrapperNode(self, rhs)


class WrapperNode(Wrapper):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def draw(self, ctx):
        self.lhs.draw(ctx)
        self.rhs.draw(ctx)


class BlendWrapper(Wrapper):
    def __init__(self, obj):
        self.obj = obj

    def draw(self, ctx):
        with BlendContext():
            self.obj.draw(ctx)


class Color(Wrapper):
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return "Color({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

    def draw(self, ctx):
        glColor4d(self.r, self.g, self.b, self.a)

    def setColor(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

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

    @property
    def alpha(self):
        return self.a

    @alpha.setter
    def alpha(self, a):
        self.a = a


class LoadIdentity(Wrapper):
    def draw(self, ctx):
        glLoadIdentity()
        ctx.raster = Point(0, 0)
        ctx.translated = Point3D(0, 0, 0)


class Ortho2DContext(Wrapper):
    def draw(self, ctx):
        ctx.ortho2D()


class RasterPos(Wrapper):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, ctx):
        glRasterPos(self.x, self.y)
        ctx.raster = Point(self.x, self.y)

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


class Translated(Wrapper):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def draw(self, ctx):
        glTranslated(self.x, self.y, self.z)
        ctx.translated = Point3D(self.x, self.y, self.z)

    def setPos(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

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

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, z):
        self.__z = z


class MatrixMode(Wrapper):
    def __init__(self, mode):
        self.mode = mode

    def draw(self, ctx):
        glMatrixMode(self.mode)


class ModelViewMode(MatrixMode):
    def __init__(self):
        super(ModelViewMode, self).__init__(GL_MODELVIEW)

class ProjectionMode(MatrixMode):
    def __init__(self):
        super(ProjectionMode, self).__init__(GL_PROJECTION)

class TextureMode(MatrixMode):
    def __init__(self):
        super(TextureMode, self).__init__(GL_TEXTURE)
