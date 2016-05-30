# -*- coding: utf-8 -*-

class DrawObject(object):
    def draw(self, ctx):
        raise NotImplementedError


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))


class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return str((self.x, self.y, self.z))


class Rect(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return str((self.x, self.y, self.w, self.h))
