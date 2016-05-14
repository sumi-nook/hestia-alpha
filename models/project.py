# -*- coding: utf-8 -*-

import os

from qt import pyqtSlot
from qt import pyqtSignal
from qt import Qt
from qt import QVariant
from qt import QModelIndex
from qt import QAbstractItemModel

from archive.container import Scenario

class TreeItem(object):
    def __init__(self, parent, name):
        self._parent = parent
        self._name = name

    def parent(self):
        return self._parent

    def name(self):
        return self._name


class DirectoryItem(TreeItem):
    def __init__(self, parent, name):
        super(DirectoryItem, self).__init__(parent, name)
        self.items = []

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def append(self, item):
        self.items.append(item)

    def index(self, item):
        return self.items.index(item)


class FileItem(TreeItem):
    def __init__(self, parent, name, object):
        super(FileItem, self).__init__(parent, name)
        self.object = object


def make_project_tree(project):
    """
    :type project: archive.file.ProjectFile
    """
    root = DirectoryItem(None, "/")
    dirs = {
        "": root,
    }
    for container in project.containers:
        head, tail = os.path.split(container.filepath)
        parent = root
        current = []
        for dirname in head.split("/"):
            current.append(dirname)
            path = "/".join(current)
            if path not in dirs:
                tmp = DirectoryItem(parent, dirname)
                parent.append(tmp)
                parent = tmp
            else:
                parent = dirs[path]
        if isinstance(container, Scenario):
            parent.append(FileItem(parent, tail, container))
    return root


class ProjectTreeModel(QAbstractItemModel):

    projectUpdated = pyqtSignal()

    def __init__(self, parent):
        """
        :type parent: QObject:
        """
        super(ProjectTreeModel, self).__init__(parent)
        self.root = None

    def index(self, row, column, parent=QModelIndex()):
        if self.hasIndex(row, column, parent):
            if not parent.isValid():
                return self.createIndex(row, column, self.root)
            else:
                item = parent.internalPointer()
                assert(isinstance(item, DirectoryItem))
                return self.createIndex(row, column, item[row])
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        item = index.internalPointer()
        if item.parent() is None:
            return QModelIndex()
        if item.parent().parent() is None:
            return self.index(0, 0)
        grand = item.parent().parent()
        assert(isinstance(grand, DirectoryItem))
        return self.createIndex(grand.index(item.parent()), 0, item.parent())

    def data(self, index, role=Qt.DisplayRole):
        if self.root is None or not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        item = index.internalPointer()
        if index.column() == 0:
            return item.name()
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation != Qt.Horizontal:
            return QVariant()
        if section == 0:
            return self.tr("Name")
        return QVariant()

    def columnCount(self, parent=QModelIndex()):
        """
        :type parent: QModelIndex
        :rtype: int
        """
        return 1

    def rowCount(self, parent=QModelIndex()):
        """
        :type parent: QModelIndex
        :rtype: int
        """
        if self.root is None:
            return 0
        # root case
        if not parent.isValid():
            return 1
        item = parent.internalPointer()
        assert(isinstance(item, DirectoryItem))
        return len(item)

    def hasChildren(self, parent=QModelIndex()):
        if not parent.isValid():
            return True
        else:
            item = parent.internalPointer()
            if isinstance(item, DirectoryItem):
                return len(item) > 0
            else:
                return False

    def setProject(self, project):
        """
        :type root: TreeItem
        """
        self.project = project
        self.projectUpdate()

    @pyqtSlot()
    def projectUpdate(self):
        self.beginResetModel()
        self.root = make_project_tree(self.project)
        self.endResetModel()
        self.projectUpdated.emit()


