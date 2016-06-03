# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import enum
import os

import six

from qt import pyqtSignal
from qt import QObject


DEFAULT_ENCODING = "utf-8"


class DummyFileObject(object):
    def __init__(self, content):
        self._content = content

    def read(self, filepath):
        return self._content


class ContainerType(enum.Enum):
    Scenario = 1
    Image = 2


class ContainerBase(QObject):

    changed = pyqtSignal(object)

    def __init__(self, file, filepath, parent=None):
        """
        :type parent: QObject
        """
        super(ContainerBase, self).__init__(parent)
        self.file = file
        self.filepath = filepath

    def archive(self, archive):
        """
        :type archive: zipfile.ZipFile
        """
        raise NotImplementedError

    def type(self):
        """
        :rtype: ContainerType
        """
        raise NotImplementedError

    def content(self):
        """
        :rtype: bytes
        """
        return self.file.read(self.filepath)

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


class Scenario(ContainerBase):
    def __init__(self, file, filepath, parent=None):
        """
        :type filepath: str
        :type content: bytes
        """
        super(Scenario, self).__init__(file, filepath, parent)
        self._content = self.content()

    def archive(self, archive):
        """
        :type archive: zipfile.ZipFile
        """
        assert(self.filepath is not None)
        archive.writestr(self.filePath(), self._content)

    def type(self):
        return ContainerType.Scenario

    def isSame(self, text):
        """
        :rtype: bool
        """
        return self._content == text.encode(DEFAULT_ENCODING)

    def text(self):
        """
        :rtype: str
        """
        return self._content.decode(DEFAULT_ENCODING, "ignore")

    def setText(self, text):
        """
        :type archive: str
        """
        assert(isinstance(text, six.text_type))
        self._content = text.encode(DEFAULT_ENCODING)
        self.changed.emit(self)

    @staticmethod
    def create():
        """
        :rtype: Scenario
        """
        return Scenario(DummyFileObject(b""), None)


class Image(ContainerBase):
    def __init__(self, file, filepath, parent=None):
        """
        :type filepath: str
        :type content: bytes
        """
        super(Image, self).__init__(file, filepath, parent)
        self._content = self.content()

    def archive(self, archive):
        """
        :type archive: zipfile.ZipFile
        """
        assert(self.filepath is not None)
        archive.writestr(self.filePath(), self.content())

    def type(self):
        return ContainerType.Image


EXT_MAP = {
    ".txt": Scenario,
    ".md": Scenario,
    ".png": Image,
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
        result.append(EXT_MAP[ext](archive, name))
    return result
