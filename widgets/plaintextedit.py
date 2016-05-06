# -*- coding: utf-8 -*-

from qt import QTextEdit

class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())

    def setScenario(self, scenario):
        """
        :type scenario: archive.container.Scenario
        """
        self.setPlainText(scenario.content.decode("utf-8"))
