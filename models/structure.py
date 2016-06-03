# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import enum

from qt import Qt
from qt import QVariant
from qt import QModelIndex
from qt import QAbstractListModel


class StructureType(enum.Enum):
    Unknown = 0
    Speech = 1
    Description = 2
    Comment = 3
    BackgroundImage = 4


class StructureContext(object):
    def __init__(self, ctx=None):
        self.bg_img = None
        self.ch_imgs = []
        if ctx is not None:
            self.bg_img = ctx.bg_img
            self.ch_imgs = ctx.ch_imgs


class StructureNode(object):
    def __init__(self, type, elem, ctx):
        self.type = type
        self.elem = elem
        self.ctx = ctx

    def data(self, role=Qt.DisplayRole):
        raise NotImplementedError


class UnknownNode(StructureNode):
    def __init__(self, elem, ctx):
        super(UnknownNode, self).__init__(StructureType.Unknown, elem, ctx)

    def data(self, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        return "<Unknown>"


class SpeechNode(StructureNode):
    def __init__(self, elem, ctx):
        super(SpeechNode, self).__init__(StructureType.Speech, elem, ctx)

    def data(self, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        name = self.elem[0].text
        speech = _nodesText(self.elem[1:])
        return "【{}】{}".format(name, speech)


class DescriptionNode(StructureNode):
    def __init__(self, elem, ctx):
        super(DescriptionNode, self).__init__(
            StructureType.Description, elem, ctx
        )

    def data(self, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        return _nodesText(self.elem)


class CommentNode(StructureNode):
    def __init__(self, elem, ctx):
        super(CommentNode, self).__init__(StructureType.Comment, elem, ctx)

    def data(self, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        return "※{}".format(_nodesText(self.elem))


class BackgroundImageNode(StructureNode):
    def __init__(self, elem, ctx):
        super(BackgroundImageNode, self).__init__(
            StructureType.BackgroundImage, elem, ctx
        )

    def data(self, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        alt = ""
        if self.elem.attrib["alt"]:
            alt = "：{}".format(self.elem.attrib["alt"])
        return "※背景：{}{}".format(self.elem.attrib["src"], alt)

    @property
    def src(self):
        return self.elem.attrib["src"]


def _nodesText(node):
    return "".join(x for x in _nodesTexts(node))

def _nodesTexts(nodes):
    for child in nodes:
        if child.text:
            yield child.text
        yield _nodesText(child)


def _parse(root):
    result = []
    ctx = StructureContext()
    for elem in root:
        if elem.tag not in ["p", "img"]:
            result.append(UnknownNode(elem, ctx))
            continue
        cls = elem.attrib.get("class", "")
        if elem.tag == "p":
            if "speech" in cls:
                result.append(SpeechNode(elem, ctx))
            elif "description" in cls:
                result.append(DescriptionNode(elem, ctx))
            elif "comment" in cls:
                result.append(CommentNode(elem, ctx))
        elif elem.tag == "img" and "background" in cls:
            ctx = StructureContext(ctx)
            node = BackgroundImageNode(elem, ctx)
            ctx.bg_img = node
            result.append(node)
        else:
            result.append(UnknownNode(elem, ctx))
    return result


class StructureListModel(QAbstractListModel):
    def __init__(self, parent):
        """
        :type parent: QObject
        """
        super(StructureListModel, self).__init__(parent)
        self._root = None

    def setRoot(self, root):
        self.beginResetModel()
        self._root = _parse(root)
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
        return index.internalPointer().data(role)

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid():
            return QModelIndex()
        return self.createIndex(row, column, self._root[row])
