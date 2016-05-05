# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from qt import Qt
from qt import QColor
from qt import QFont
from qt import QRegExp
from qt import QSyntaxHighlighter
from qt import QTextCharFormat

class ScenarioHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)

        points = []

        reg = QRegExp("^(【[^】]+】)(「[^」]+(」?))$")
        index = reg.indexIn(text)
        while index != -1:
            length = reg.matchedLength()
            self.setFormat(index, length, fmt)
            self.setFormat(index, index+len(reg.cap(1)), QColor("#0000cd"))
            if reg.cap(3).isEmpty():
                self.setFormat(index+len(reg.cap(1)), index+len(reg.cap(2)), QColor(Qt.red))
            index = reg.indexIn(text, index+length)
