# -*- coding: utf-8 -*-

import enum

from qt import pyqtSignal
from qt import QObject

from gl.base import DrawObject


class Scene(enum.IntEnum):
    BackgroundImage = 0
    MessageWindow = 1000
    Message = 1001


class SceneObject(DrawObject):
    def __init__(self):
        self.objects = {}

    def clear(self):
        self.objects = {}

    def draw(self, ctx):
        for key in sorted(self.objects.keys()):
            self.objects[key].draw(ctx)

    def setBackgroundImage(self, img):
        self.objects[Scene.BackgroundImage] = img

    def setMessageWindow(self, window):
        self.objects[Scene.MessageWindow] = window

    def setMessage(self, msg):
        self.objects[Scene.Message] = msg


class DoubleBufferObject(DrawObject, QObject):

    updated = pyqtSignal()

    def __init__(self, parent=None):
        super(DoubleBufferObject, self).__init__(parent)
        self.scenes = [
            SceneObject(),
            SceneObject(),
        ]
        self.current = 0
        self.back = 1

    def clear(self):
        self.backBuffer().clear()
        self.flip()

    def flip(self):
        self.current = 0 if self.current else 1
        self.back = 0 if self.current else 1
        self.backBuffer().clear()
        self.updated.emit()

    def backBuffer(self):
        return self.scenes[self.back]

    def draw(self, ctx):
        self.scenes[self.current].draw(ctx)

    def setBackgroundImage(self, img):
        self.backBuffer().setBackgroundImage(img)

    def setMessageWindow(self, window):
        self.backBuffer().setMessageWindow(window)

    def setMessage(self, msg):
        self.backBuffer().setMessage(msg)
