# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from qt import Qt
from qt import QVariant
from qt import QModelIndex
from qt import QAbstractListModel


class StructureListModel(QAbstractListModel):
    def __init__(self, parent):
        """
        :type parent: QObject
        """
        super(StructureListModel, self).__init__(parent)
        self._root = None

    def setRoot(self, root):
        self.beginResetModel()
        self._root = root
        self.endResetModel()

    def columnCount(self, parent=QModelIndex()):
        """
        :rtype: int
        """
        return 1

    def rowCount(self, parent=QModelIndex()):
        if self._root is None:
            return 0
        return len(self._root)

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        return self._nodeToValue(self._root[index.row()])

    def _nodeToValue(self, node):
        cls = node.attrib["class"]
        if "speech" in cls:
            return self._speechText(node)
        elif "description" in cls:
            return self._descriptionText(node)

    def _speechText(self, node):
        name = node[0].text
        speech = self._nodesText(node[1:])
        return "【{}】{}".format(name, speech)

    def _descriptionText(self, node):
        return self._nodesText(node)

    def _nodesText(self, node):
        return "".join(x for x in self._nodesTexts(node))

    def _nodesTexts(self, nodes):
        for child in nodes:
            if child.text:
                yield child.text
            yield self._nodesText(child)
