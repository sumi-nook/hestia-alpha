# -*- coding: utf-8 -*-

from .base import DrawObject

from OpenGL.GL import *

class TextObject(DrawObject):
    def __init__(self, text, fontName=None):
        self.text = text
        self.fontName = fontName

    def draw(self, ctx):
        font = ctx.fontRegistry.font(self.fontName)
        tmp = ""
        line = 0
        for ch in self.text:
            tmp += ch
            bb = font.BBox(tmp)
            u = bb.Upper()
            l = bb.Lower()
            if (ctx.raster.x * 2 + u.X - l.X) > ctx.width:
                font.Render(tmp[:-1])
                tmp = tmp[-1:]
                line += 1
                glRasterPos(ctx.raster.x, ctx.raster.y - font.LineHeight() * line)
        if tmp:
            font.Render(tmp)
