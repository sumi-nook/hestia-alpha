# -*- coding: utf-8 -*-

from qt import QTextEdit

from archive.container import Scenario

class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())

    def setScenario(self, scenario):
        """
        :type scenario: archive.container.Scenario
        """
        assert(isinstance(scenario, Scenario))
        self.setPlainText(scenario.text())
