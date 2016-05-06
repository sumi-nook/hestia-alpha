# -*- coding: utf-8 -*-

from qt import QTextEdit

class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())
