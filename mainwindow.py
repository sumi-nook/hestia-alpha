# -*- coding: utf-8 -*-

from __future__ import division

import os

import qt
from qt import pyqtSlot, pyqtSignal
from qt import QModelIndex
from qt import QMainWindow
from qt import QDialog
from qt import QFileDialog

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

        self.initialize()

    def initialize(self):
        self.project = ProjectFile.create()
        self.initializeScenario()

        self.projectModel = ProjectTreeModel(self)
        self.projectModel.projectUpdated.connect(self.projectModel_projectUpdated)

        self.ui.treeViewScenario.setModel(self.projectModel)
        self.ui.treeViewStructure.setModel(self.projectModel)
        self.scenarioSelection = self.ui.treeViewScenario.selectionModel()
        self.structureSelection = self.ui.treeViewStructure.selectionModel()

        self.scenarioSelection.currentRowChanged.connect(self.scenarioSelection_currentRowChanged)
        self.structureSelection.currentRowChanged.connect(self.structureSelection_currentRowChanged)

        self.projectModel.setProject(self.project)

    def initializeScenario(self):
        self.currentScenario = Scenario.create()
        self.ui.textEditScenario.clear()

    def open(self, filepath):
        """
        :type filepath: str
        """
        self.project = ProjectFile.open(filepath)
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
        root, ext = os.path.splitext(filepath)
        if ext != HESTIA_EXT:
            return root + HESTIA_EXT
        return filepath

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
        if self.project.filepath is None:
            filepath = self.getSaveFileName(self.tr(""), self.tr(""), self.HESTIA_ARCHIVE_FILTER)
            if not filepath:
                return
            filepath = self.hestiaArchiveName(filepath)
            self.project.setFilePath(filepath)
        self.project.save()

    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        filepath = self.getSaveFileName(self.tr(""), self.tr(""), self.HESTIA_ARCHIVE_FILTER)
        if not filepath:
            return
        filepath = self.hestiaArchiveName(filepath)
        self.project.setFilePath(filepath)
        self.project.save()

    @pyqtSlot()
    def on_actionScenarioNew_triggered(self):
        self.initializeScenario()
    
    @pyqtSlot()
    def on_actionScenarioSave_triggered(self):
        filename = None
        if self.currentScenario.filepath is None:
            dialog = FileNameEditDialog(self)
            if dialog.exec_() != QDialog.Accepted:
                return
            filename = dialog.fileName()
            root, ext = os.path.splitext(filename)
            if ext not in [".txt", ".md"]:
                filename += DEFAULT_EXT
        # set content
        content = qt.toUnicode(self.ui.textEditScenario.toPlainText())
        content = content.encode("utf-8")
        self.currentScenario.content = content
        if self.currentScenario.filepath is not None:
            # filename is already set
            return
        # set filepath & register
        self.currentScenario.filepath = filename
        self.project.append(self.currentScenario)
        self.projectModel.projectUpdate()

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
        content = content.encode("utf-8")
        self.currentScenario = Scenario.create()
        self.currentScenario.content = content
        # set filepath & register
        self.currentScenario.filepath = filename
        self.project.append(self.currentScenario)
        self.projectModel.projectUpdate()

    @pyqtSlot(QModelIndex, QModelIndex)
    def scenarioSelection_currentRowChanged(self, current, previous):
        if not current.isValid():
            return
        item = current.internalPointer()
        if not isinstance(item, FileItem):
            return
        self.currentScenario = item.object
        self.ui.textEditScenario.setScenario(self.currentScenario)

    @pyqtSlot(QModelIndex, QModelIndex)
    def structureSelection_currentRowChanged(self, current, previous):
        if not current.isValid():
            return
