# -*- coding: utf-8 -*-

from .base import DrawObject


class TextObject(DrawObject):
    def __init__(self, text, fontName=None):
        self.text = text
        self.fontName = fontName

    def draw(self, ctx):
        font = ctx.fontRegistry.font(self.fontName)
        bb = font.BBox(self.text)
        u = bb.Upper()
        l = bb.Lower()
        font.Render(self.text)
