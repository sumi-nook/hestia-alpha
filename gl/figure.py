# -*- coding: utf-8 -*-

from OpenGL.GL import *

from .base import DrawObject


class RelativeQuad(DrawObject):
    def __init__(self, rect):
        self.rect = rect

    def draw(self, ctx):
        glBegin(GL_QUADS)
        # left, top
        glVertex2d(self.rect.x, self.rect.y)
        # right, top
        glVertex2d(self.rect.w, self.rect.y)
        # right, bottom
        glVertex2d(self.rect.w, self.rect.h)
        # left, bottom
        glVertex2d(self.rect.x, self.rect.h)
        glEnd()
