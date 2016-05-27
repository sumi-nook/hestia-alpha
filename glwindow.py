# -*- coding: utf-8 -*-

from __future__ import division

from qt import QMainWindow
from qt import QSize

from ui.glwindow import Ui_GLWindow


class GLWindow(QMainWindow):
    def __init__(self, parent=None):
        super(GLWindow, self).__init__(parent)
        self.ui = Ui_GLWindow()
        self.ui.setupUi(self)

    def setViewSize(self, width, height):
        maximum = QSize(16777215, 16777215)
        self.ui.openGLWidget.setMaximumSize(maximum)
        self.ui.openGLWidget.setMinimumSize(width, height)
        self.ui.openGLWidget.setMaximumSize(width, height)
