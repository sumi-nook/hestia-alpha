# -*- coding: utf-8 -*-

from qt import pyqtSlot
from qt import QString
from qt import QStringListModel
from qt import QAbstractButton
from qt import QDialog
from qt import QDialogButtonBox

from ui.errormessagedialog import Ui_ErrorMessageDialog


class ErrorMessageDialog(QDialog):
    def __init__(self, parent=None):
        super(ErrorMessageDialog, self).__init__(parent)
        self.ui = Ui_ErrorMessageDialog()
        self.ui.setupUi(self)

        self.model = QStringListModel(self)
        self.ui.listView.setModel(self.model)

    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        if button == self.ui.buttonBox.button(QDialogButtonBox.Close):
            self.close()
        elif button == self.ui.buttonBox.button(QDialogButtonBox.Reset):
            self.model.setStringList([])

    @pyqtSlot(QString)
    def appendMessage(self, msg):
        strs = self.model.stringList()
        strs.append(msg)
        self.model.setStringList(strs)
