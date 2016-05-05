#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from qt import QApplication
from qt import QTranslator
from qt import QLocale

from mainwindow import MainWindow

def main(argv):
    app = QApplication(argv)

    qtTr = QTranslator()
    if qtTr.load("qt_" + QLocale.system().name(), ":/i18n/"):
        app.installTranslator(qtTr)

    appTr = QTranslator()
    if appTr.load("hestia_" + QLocale.system().name(), ":/i18n/"):
        app.installTranslator(appTr)

    win = MainWindow()
    win.show()

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
