# -*- coding: utf-8 -*-

class DrawObject(object):
    def draw(self, ctx):
        raise NotImplementedError


class Rect(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
