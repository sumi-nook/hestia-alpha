# -*- coding: utf-8 -*-

import six

from qt import QDialog

from ui.filenameeditdialog import Ui_FileNameEditDialog

class FileNameEditDialog(QDialog):
    def __init__(self, parent=None):
        super(FileNameEditDialog, self).__init__(parent)
        self.ui = Ui_FileNameEditDialog()
        self.ui.setupUi(self)

    def fileName(self):
        filename = self.ui.lineEdit.text()
        if six.PY2:
            filename = six.text_type(filename)
        return filename
