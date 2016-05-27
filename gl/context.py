# -*- coding: utf-8 -*-

import os

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
