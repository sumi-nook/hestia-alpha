# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

import ftgl
from lxml import etree
import six

import qt
from qt import pyqtSlot, pyqtSignal
from qt import Qt
from qt import QCoreApplication
from qt import QModelIndex
from qt import QAction
from qt import QMainWindow
from qt import QDialog
from qt import QFileDialog
from qt import QMessageBox
from qt import QItemSelectionModel

from archive.file import ProjectFile
from archive.container import ContainerBase
from archive.container import Scenario
from models.project import ProjectTreeModel
from models.project import FileItem
from models.structure import StructureListModel
from highlighter import ScenarioHighlighter
import converter

from emulator.scene import DoubleBufferObject
from gl.figure import RelativeQuad
from gl.text import TextObject
from gl.base import Rect
from gl.image import PILImageTexture
from gl.wrapper import *

from ui.mainwindow import Ui_MainWindow

from filenameeditdialog import FileNameEditDialog
from glwindow import GLWindow


DEFAULT_ENCODING = "utf-8"
if os.name == "nt":
    DEFAULT_ENCODING = "cp932"
DEFAULT_FONT = "fonts/ipag.ttc"

DEFAULT_EXT = ".txt"
HESTIA_EXT = ".hax"

XSLT_MARKDOWN = "transforms/Markdown.xsl"
XSLT_KAG3 = "transforms/KAG3.xsl"
XSLT_NSCRIPTER = "transforms/NScripter.xsl"


class MainWindow(QMainWindow):

    scenarioRestore = pyqtSignal(QModelIndex)
    scriptUpdate = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.targetActions = [
            self.ui.actionMarkdown,
            self.ui.actionKAG3,
            self.ui.actionNScripter,
        ]

        # constants
        self.HESTIA_ARCHIVE_FILTER = self.tr("Hestia Archive(*.hax)")

        width = self.ui.splitterScenario.width()
        w = width // 3
        m = width % 3
        self.ui.splitterScenario.setSizes([w, w*2+m])
        self.ui.splitterScript.setSizes([w, w*2+m])

        self.highlighter = ScenarioHighlighter(self.ui.textEditScenario.document())

        self.scenarioRestore.connect(self.scenarioRestored)

        self.previewHasReady = False
        self.glWindow = GLWindow(self)
        self.glWindow.setViewSize(1280, 720)
        self.glWindow.ready.connect(self.previewWindow_ready)

        self.doubleBufferObject = DoubleBufferObject()
        self.glWindow.setDoubleBufferObject(self.doubleBufferObject)

        self.initialize()

    def initialize(self):
        self.project = ProjectFile.create()

        self.projectModel = ProjectTreeModel(self)
        self.projectModel.projectUpdated.connect(self.projectModel_projectUpdated)

        # file selection view
        self.ui.treeViewScenario.setModel(self.projectModel)
        self.ui.treeViewStructure.setModel(self.projectModel)
        self.ui.treeViewScript.setModel(self.projectModel)
        self.scenarioSelection = self.ui.treeViewScenario.selectionModel()
        self.structureSelection = self.ui.treeViewStructure.selectionModel()
        self.scriptSelection = self.ui.treeViewScript.selectionModel()

        self.scenarioSelection.currentRowChanged.connect(self.scenarioSelection_currentRowChanged, Qt.QueuedConnection)
        self.structureSelection.currentRowChanged.connect(self.structureSelection_currentRowChanged)
        self.scriptSelection.currentRowChanged.connect(self.scriptSelection_currentRowChanged)

        # scenario structure view
        self.structureModel = StructureListModel(self)

        self.ui.listViewStructure.setModel(self.structureModel)
        self.lineSelection = self.ui.listViewStructure.selectionModel()

        self.lineSelection.currentRowChanged.connect(self.lineSelection_currentRowChanged)

        self.setProject(ProjectFile.create())

        self.initializeScenario()

    def initializeScenario(self):
        self.setCurrentScenario(Scenario.create())
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
        self.project.changed.connect(self.projectModel.projectUpdate)
        self.projectModel.setProject(self.project)
        self.projectModel.projectUpdate()

    def setCurrentScenario(self, scenario):
        self.currentScenario = scenario
        filepath = self.currentScenario.filePath()
        if not filepath:
            self.setWindowTitle(self.tr("Hestia [*]"))

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

    @pyqtSlot(object)
    def projectChanged(self, container):
        self.setWindowModified(True)
        if container:
            filepath = container.filePath()
            self.setWindowTitle(self.tr("%1 - Hestia [*]").arg(filepath))


    @pyqtSlot()
    def projectModel_projectUpdated(self):
        self.ui.treeViewScenario.setRootIndex(self.projectModel.index(0, 0))
        self.ui.treeViewStructure.setRootIndex(self.projectModel.index(0, 0))
        self.ui.treeViewScript.setRootIndex(self.projectModel.index(0, 0))
        self.ui.treeViewScenario.expandAll()
        self.ui.treeViewStructure.expandAll()
        self.ui.treeViewScript.expandAll()

    @pyqtSlot()
    def previewWindow_ready(self):
        self.previewHasReady = True
        # set default font
        if __debug__:
            path = os.path.join(os.path.dirname(__file__), DEFAULT_FONT)
        else:
            appDir = six.text_type(QCoreApplication.applicationDirPath())
            path = os.path.join(appDir, DEFAULT_FONT)
        if not os.path.exists(path):
            QMessageBox.critical(self,
                self.tr("Font not found"),
                self.tr("Font \"%1\" cannot open.").arg(path)
            )
            sys.exit(1)
        font = ftgl.FTPixmapFont(path.encode(DEFAULT_ENCODING))
        if not font.FaceSize(30):
            print("FaceSize error.", file=sys.stderr)
        self.glWindow.context().fontRegistry.installFont(None, font)

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
        self.save(filepath)

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
        scenario = Scenario.create()
        scenario.setText(content)
        # set filepath & register
        scenario.setFilePath(filename)
        self.project.append(scenario)
        self.setCurrentScenario(scenario)

    @pyqtSlot()
    def on_actionShowPreview_triggered(self):
        self.glWindow.show()

    @pyqtSlot(QAction)
    def on_menuTarget_triggered(self, target):
        # force checked
        target.setChecked(True)
        # Toggle target
        for action in self.targetActions:
            if action == target:
                continue
            if action.isChecked():
                action.setChecked(False)
        current = self.scriptSelection.currentIndex()
        self.showScript(current)

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
        self.setCurrentScenario(currentItem.object)
        self.ui.textEditScenario.setScenario(self.currentScenario)
        filepath = self.currentScenario.filePath()
        self.setWindowTitle(self.tr("%1 - Hestia [*]").arg(filepath))

    @pyqtSlot(QModelIndex, QModelIndex)
    def structureSelection_currentRowChanged(self, current, previous):
        if not current.isValid():
            return
        currentItem = current.internalPointer()
        previousItem = previous.internalPointer()
        if not isinstance(currentItem, FileItem):
            return
        root = self.indexToDOM(current)
        if root is None:
            return
        self.structureModel.setRoot(root)

    @pyqtSlot(QModelIndex, QModelIndex)
    def scriptSelection_currentRowChanged(self, current, previous):
        self.showScript(current)

    @pyqtSlot(QModelIndex)
    def showScript(self, index):
        if not index.isValid():
            self.ui.textEditScript.clear()
            return
        item = index.internalPointer()
        if not isinstance(item, FileItem):
            self.ui.textEditScript.clear()
            return
        root = self.indexToDOM(index)
        if root is None:
            self.ui.textEditScript.clear()
            return
        script = self.makeScript(root)
        self.ui.textEditScript.setPlainText(script)

    def indexToDOM(self, index):
        if not index.isValid():
            return None
        item = index.internalPointer()
        if not isinstance(item, FileItem):
            return None
        text = item.object.text()
        xhtml = converter.toXHTML(text)
        return etree.fromstring(xhtml)

    def makeScript(self, root):
        xslt = self.currentTargetXSLT()
        return six.text_type(xslt(root))

    def currentTargetXSLT(self):
        root = qt.toUnicode(QCoreApplication.applicationDirPath())
        if __debug__:
            root = os.path.dirname(__file__)
        if self.ui.actionMarkdown.isChecked():
            return etree.XSLT(etree.parse(os.path.join(root, XSLT_MARKDOWN)))
        elif self.ui.actionKAG3.isChecked():
            return etree.XSLT(etree.parse(os.path.join(root, XSLT_KAG3)))
        elif self.ui.actionNScripter.isChecked():
            return etree.XSLT(etree.parse(os.path.join(root, XSLT_NSCRIPTER)))
        else:
            raise Exception

    @pyqtSlot(QModelIndex)
    def scenarioRestored(self, index):
        self.ui.treeViewScenario.setCurrentIndex(index)

    @pyqtSlot(QModelIndex, QModelIndex)
    def lineSelection_currentRowChanged(self, current, previous):
        obj = LoadIdentity() & Ortho2DContext() & BlendWrapper(Color(0.0, 0.0, 0.0, 0.5) & RelativeQuad(Rect(0.0, 0.0, 1280, 300)))
        self.doubleBufferObject.setMessageWindow(obj)

        text = self.currentText(current)
        obj = LoadIdentity() & Ortho2DContext() & Color(1.0, 1.0, 1.0) & RasterPos(100, 200) & TextObject(text)
        self.doubleBufferObject.setMessage(obj)

        self.doubleBufferObject.flip()

    def currentText(self, current):
        item = self.structureModel.data(current)
        return six.text_type(item)
