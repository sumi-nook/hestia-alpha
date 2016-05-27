# -*- coding: utf-8 -*-

from OpenGL.GL import *

from .base import DrawObject


class TextureUnit(object):
    def __init__(self, unit_id):
        self.unit_id = unit_id
        self.prev_id = None

    def __enter__(self):
        # save previous texture unit
        self.prev_id = self.activeUnit()
        # set current texture unit
        glActivateTexture(self.unit_id)

    def __exit__(self, type, value, traceback):
        # set previous texture unit
        glActivateTexture(self.prev_id)
        if type:
            return False
        return True

    @classmethod
    def activeUnit(cls):
        return glGetInteger(GL_ACTIVE_TEXTURE)


class Texture(DrawObject):
    def __init__(self, texture_id=None):
        if texture_id is None:
            texture_id = glGenTextures(1)
        self.texture_id = texture_id
        self.unit = None

    def draw(self, ctx):
        raise NotImplementedError

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, unit):
        self.__unit = unit
