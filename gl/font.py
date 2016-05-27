# -*- coding: utf-8 -*-

import ftgl


class FontRegistry(object):
    def __init__(self):
        self.fonts = {}

    def installFont(self, name, font):
        """
        :type name: str
        :type font: ftgl.FTPixmapFont
        """
        self.fonts[name] = font

    def font(self, name):
        return self.fonts.get(name)
