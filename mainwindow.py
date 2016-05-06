# -*- coding: utf-8 -*-

from __future__ import division

import os

import qt
from qt import pyqtSlot, pyqtSignal
from qt import Qt
from qt import QModelIndex
from qt import QMainWindow
from qt import QDialog
from qt import QFileDialog
from qt import QMessageBox
from qt import QItemSelectionModel

from archive.file import ProjectFile
from archive.container import Scenario
from models.project import ProjectTreeModel
from models.project import FileItem
from highlighter import ScenarioHighlighter

from ui.mainwindow import Ui_MainWindow

from filenameeditdialog import FileNameEditDialog


DEFAULT_EXT = ".txt"
HESTIA_EXT = ".hax"


class MainWindow(QMainWindow):

    scenarioRestore = pyqtSignal(QModelIndex)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # constants
        self.HESTIA_ARCHIVE_FILTER = self.tr("Hestia Archive(*.hax)")

        width = self.ui.splitterScenario.width()
        w = width // 3
        m = width % 3
        self.ui.splitterScenario.setSizes([w, w*2+m])

        self.highlighter = ScenarioHighlighter(self.ui.textEditScenario.document())

        self.scenarioRestore.connect(self.scenarioRestored)

        self.initialize()

    def initialize(self):
        self.project = ProjectFile.create()

        self.projectModel = ProjectTreeModel(self)
        self.projectModel.projectUpdated.connect(self.projectModel_projectUpdated)

        self.ui.treeViewScenario.setModel(self.projectModel)
        self.ui.treeViewStructure.setModel(self.projectModel)
        self.scenarioSelection = self.ui.treeViewScenario.selectionModel()
        self.structureSelection = self.ui.treeViewStructure.selectionModel()

        self.scenarioSelection.currentRowChanged.connect(self.scenarioSelection_currentRowChanged, Qt.QueuedConnection)
        self.structureSelection.currentRowChanged.connect(self.structureSelection_currentRowChanged)

        self.setProject(ProjectFile.create())

        self.initializeScenario()

    def initializeScenario(self):
        self.currentScenario = Scenario.create()
        self.ui.textEditScenario.clear()
        self.scenarioSelection.setCurrentIndex(QModelIndex(), QItemSelectionModel.Clear)

    def currentIsChanged(self):
        text = qt.toUnicode(self.ui.textEditScenario.toPlainText())
        return not self.currentScenario.isSame(text)

    def open(self, filepath):
        """
        :type filepath: str
        """
        self.setProject(ProjectFile.open(filepath))

    def save(self, filepath):
        """
        :type filepath: str
        """
        assert(bool(filepath))
        filepath = self.hestiaArchiveName(filepath)
        self.project.setFilePath(filepath)
        self.project.save()
        self.setWindowModified(False)

    def setProject(self, project):
        self.project = project
        self.project.changed.connect(self.projectChanged)
        self.project.updated.connect(self.projectModel.projectUpdate)
        self.projectModel.setProject(self.project)
        self.projectModel.projectUpdate()

    def getOpenFileName(self, caption, path, filter):
        """
        :rtype: str
        """
        return qt.toUnicode(QFileDialog.getOpenFileName(self, caption, path, filter))

    def getSaveFileName(self, caption, path, filter):
        """
        :rtype: str
        """
        return qt.toUnicode(QFileDialog.getSaveFileName(self, caption, path, filter))

    def hestiaArchiveName(self, filepath):
        """
        :type filepath: str
        :rtype: str
        """
        root, ext = os.path.splitext(filepath)
        if ext != HESTIA_EXT:
            return root + HESTIA_EXT
        return filepath

    def closeEvent(self, event):
        if self.project.isChanged():
            ret = QMessageBox.warning(self,
                    self.tr("Project changed"),
                    self.tr("Do you want to continue?"),
                    QMessageBox.Cancel | QMessageBox.Discard)
            if ret == QMessageBox.Cancel:
                event.ignore()
                return

    @pyqtSlot()
    def projectChanged(self):
        self.setWindowModified(True)

    @pyqtSlot()
    def projectModel_projectUpdated(self):
        self.ui.treeViewScenario.setRootIndex(self.projectModel.index(0, 0))
        self.ui.treeViewStructure.setRootIndex(self.projectModel.index(0, 0))
        self.ui.treeViewScenario.expandAll()
        self.ui.treeViewStructure.expandAll()

    @pyqtSlot()
    def on_actionNew_triggered(self):
        self.initialize()

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        filepath = self.getOpenFileName(self.tr(""), self.tr(""), self.HESTIA_ARCHIVE_FILTER)
        if not filepath:
            return
        self.open(filepath)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        filepath = self.project.filePath()
        if not filepath:
            filepath = self.getSaveFileName(self.tr(""), self.tr(""), self.HESTIA_ARCHIVE_FILTER)
            if not filepath:
                return
            filepath = self.hestiaArchiveName(filepath)
        self.project.save(filepath)

    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        filepath = self.getSaveFileName(self.tr(""), self.tr(""), self.HESTIA_ARCHIVE_FILTER)
        if not filepath:
            return
        self.save(filepath)

    @pyqtSlot()
    def on_actionScenarioNew_triggered(self):
        if self.currentIsChanged():
            ret = QMessageBox.warning(self,
                self.tr("Text changed"),
                self.tr("Do you want to save it?"),
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                return
            elif ret == QMessageBox.Save:
                content = qt.toUnicode(self.ui.textEditScenario.toPlainText())
                self.currentScenario.setText(content)
        self.initializeScenario()
    
    @pyqtSlot()
    def on_actionScenarioSave_triggered(self):
        filename = self.currentScenario.filePath()
        if not filename:
            dialog = FileNameEditDialog(self)
            if dialog.exec_() != QDialog.Accepted:
                return
            filename = dialog.fileName()
            root, ext = os.path.splitext(filename)
            if ext not in [".txt", ".md"]:
                filename += DEFAULT_EXT
        # set content
        content = qt.toUnicode(self.ui.textEditScenario.toPlainText())
        self.currentScenario.setText(content)
        if self.currentScenario.filePath():
            # filename is already set
            return
        # set filepath & register
        self.currentScenario.setFilePath(filename)
        self.project.append(self.currentScenario)

    @pyqtSlot()
    def on_actionScenarioSaveAs_triggered(self):
        dialog = FileNameEditDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return
        filename = dialog.fileName()
        root, ext = os.path.splitext(filename)
        if ext not in [".txt", ".md"]:
            filename += DEFAULT_EXT
        # set content
        content = qt.toUnicode(self.ui.textEditScenario.toPlainText())
        self.currentScenario = Scenario.create()
        self.currentScenario.setText(content)
        # set filepath & register
        self.currentScenario.setFilePath(filename)
        self.project.append(self.currentScenario)

    @pyqtSlot(QModelIndex, QModelIndex)
    def scenarioSelection_currentRowChanged(self, current, previous):
        if not current.isValid():
            return
        currentItem = current.internalPointer()
        previousItem = previous.internalPointer()
        if not isinstance(currentItem, FileItem):
            return
        if currentItem == previousItem:
            return
        if currentItem.object == self.currentScenario:
            return
        if self.currentIsChanged():
            ret = QMessageBox.information(self,
                    self.tr("Text Changed"),
                    self.tr("Do you want to save it?"),
                    QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Discard)
            if ret == QMessageBox.Cancel:
                self.scenarioRestore.emit(previous)
                return
            elif ret == QMessageBox.Save:
                self.currentScenario.setText(qt.toUnicode(self.ui.textEditScenario.toPlainText()))
        self.currentScenario = currentItem.object
        self.ui.textEditScenario.setScenario(self.currentScenario)

    @pyqtSlot(QModelIndex, QModelIndex)
    def structureSelection_currentRowChanged(self, current, previous):
        if not current.isValid():
            return

    @pyqtSlot(QModelIndex)
    def scenarioRestored(self, index):
        self.ui.treeViewScenario.setCurrentIndex(index)
