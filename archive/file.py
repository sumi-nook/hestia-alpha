# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import six

from io import BytesIO

import shutil
import tempfile
import zipfile

from qt import pyqtSignal, pyqtSlot
from qt import QObject

from .container import parse as container_parse
from .container import ContainerBase
from .container import Scenario
from .exceptions import ArchiveException


class ProjectFile(QObject):

    # archive content changed
    changed = pyqtSignal(object)

    def __init__(self, fp):
        """
        :type fp: zipfile.ZipFile
        """
        super(ProjectFile, self).__init__()
        self.filepath = None
        self.fp = fp
        self.containers = container_parse(self.fp)
        self.saved = True

    def append(self, container):
        assert(container not in self.containers)
        self.containers.append(container)
        container.changed.connect(self.containerChanged)
        self.changed.emit(container)

    def filePath(self):
        return self.filepath

    def setFilePath(self, filepath):
        self.filepath = filepath

    def loadResource(self, path, test_exts=[]):
        path = os.path.normpath(path)
        if os.sep == "\\":
            path = path.replace("\\", "/")
        for name in self.fp.namelist():
            if name == path:
                return self.fp.read(name)
            for ext in test_exts:
                if name != (path + ext):
                    continue
                return self.fp.read(name)
        return None

    def isChanged(self):
        return not self.saved

    def save(self):
        assert(self.filepath is not None)
        fp = tempfile.NamedTemporaryFile()
        archive = zipfile.ZipFile(fp, "w")
        for container in self.containers:
            container.archive(archive)
        archive.close()
        shutil.copyfile(fp.name, self.filepath)
        self.saved = True

    @pyqtSlot(object)
    def containerChanged(self, container):
        self.saved = False
        self.changed.emit(container)

    @staticmethod
    def create():
        """
        :rtype: ProjectFile
        """
        return ProjectFile(zipfile.ZipFile(BytesIO(), "a"))

    @staticmethod
    def open(filepath):
        """
        :type filepath: str
        :rtype: ProjectFile
        """
        result = ProjectFile(zipfile.ZipFile(open(filepath, "rb")))
        result.setFilePath(filepath)
        for container in result.containers:
            container.changed.connect(result.containerChanged)
        return result
