# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from qt import Qt
from qt import QColor
from qt import QFont
from qt import QRegExp
from qt import QSyntaxHighlighter
from qt import QTextCharFormat

class ScenarioHighlighter(QSyntaxHighlighter):

    SPEECH_RE = "^(【[^】]+】)(「[^」]+(」?))$"
    COMMENT_RE = "^※(.*)$"

    STATE_EMPTY = -1
    STATE_SPEECH = 1
    STATE_DESCRIPTION = 2
    STATE_COMMENT = 3

    def highlightBlock(self, text):
        if text.isEmpty():
            self.setCurrentBlockState(self.STATE_EMPTY)
            return

        matched = False

        speechReg = QRegExp(self.SPEECH_RE)
        if speechReg.indexIn(text) != -1:
            self.applySpeechStyle(text, speechReg)
            matched = True

        commentReg = QRegExp(self.COMMENT_RE)
        if commentReg.indexIn(text) != -1:
            self.applyCommentStyle(text, commentReg)
            matched = True

        if not matched:
            self.applyDescriptionStyle(text)

    def applySpeechStyle(self, text, reg):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)

        self.setFormat(0, len(text), fmt)
        self.setFormat(0, len(reg.cap(1)), QColor("#0000cd"))
        if reg.cap(3).isEmpty():
            self.setFormat(len(reg.cap(1)), len(reg.cap(2)), QColor(Qt.red))
        self.setCurrentBlockState(self.STATE_SPEECH)

    def applyCommentStyle(self, text, reg):
        self.setFormat(0, len(text), QColor("#228b22"))
        self.setCurrentBlockState(self.STATE_COMMENT)

    def applyDescriptionStyle(self, text):
        if self.previousBlockState() not in [self.STATE_EMPTY, self.STATE_DESCRIPTION]:
            self.setFormat(0, len(text), QColor(Qt.red))
            self.setCurrentBlockState(self.previousBlockState())
            return
        self.setFormat(0, len(text), QColor("#191970"))
        self.setCurrentBlockState(self.STATE_DESCRIPTION)
