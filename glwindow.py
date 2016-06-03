# -*- coding: utf-8 -*-

from __future__ import division

from qt import pyqtSignal
from qt import Qt
from qt import QMainWindow
from qt import QSize

from ui.glwindow import Ui_GLWindow


class GLWindow(QMainWindow):

    ready = pyqtSignal()
    next = pyqtSignal()
    prev = pyqtSignal()

    def __init__(self, parent=None):
        super(GLWindow, self).__init__(parent)
        self.ui = Ui_GLWindow()
        self.ui.setupUi(self)

        self.ui.openGLWidget.ready.connect(self.ready)
        self.ui.openGLWidget.clicked.connect(self.next)

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Down]:
            self.next.emit()
        elif key in [Qt.Key_Up]:
            self.prev.emit()
        else:
            super(GLWindow, self).keyPressEvent(event)

    def context(self):
        return self.ui.openGLWidget.context()

    def setViewSize(self, width, height):
        maximum = QSize(16777215, 16777215)
        self.ui.openGLWidget.setMaximumSize(maximum)
        self.ui.openGLWidget.setMinimumSize(width, height)
        self.ui.openGLWidget.setMaximumSize(width, height)

    def setDoubleBufferObject(self, obj):
        self.ui.openGLWidget.appendObject(obj)
        obj.updated.connect(self.ui.openGLWidget.flush)
