# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import six

from qt import pyqtSignal
from qt import QObject


DEFAULT_ENCODING = "utf-8"


class ContainerBase(QObject):

    changed = pyqtSignal(object)

    def __init__(self, parent=None):
        """
        :type parent: QObject
        """
        super(ContainerBase, self).__init__(parent)

    def archive(self, archive):
        """
        :type archive: zipfile.ZipFile
        """
        raise NotImplementedError


class Scenario(ContainerBase):
    def __init__(self, filepath, content):
        """
        :type filepath: str
        :type content: bytes
        """
        super(Scenario, self).__init__()
        self.filepath = filepath
        self.content = content

    def archive(self, archive):
        """
        :type archive: zipfile.ZipFile
        """
        assert(self.filepath is not None)
        archive.writestr(self.filepath, self.content)

    def isSame(self, text):
        """
        :rtype: bool
        """
        return self.content == text.encode(DEFAULT_ENCODING)

    def filePath(self):
        """
        :rtype: str
        """
        return self.filepath

    def setFilePath(self, filepath):
        """
        :type filepath: str
        """
        self.filepath = filepath

    def text(self):
        """
        :rtype: str
        """
        return self.content.decode(DEFAULT_ENCODING, "ignore")

    def setText(self, text):
        """
        :type archive: str
        """
        assert(isinstance(text, six.text_type))
        self.content = text.encode(DEFAULT_ENCODING)
        self.changed.emit(self)

    @staticmethod
    def create():
        """
        :rtype: Scenario
        """
        return Scenario(None, b"")


EXT_MAP = {
    ".txt": Scenario,
    ".md": Scenario,
}


def parse(archive):
    """
    :type archive: zipfile.ZipFile
    :rtype: list of ContainerBase
    """
    result = []
    for name in archive.namelist():
        root, ext = os.path.splitext(name)
        if ext not in EXT_MAP:
            continue
        result.append(EXT_MAP[ext](name, archive.read(name)))
    return result
