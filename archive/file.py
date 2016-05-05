# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from io import BytesIO

import shutil
import tempfile
import zipfile

from . import container
from .exceptions import ArchiveException


class ProjectFile(object):
    def __init__(self, fp):
        """
        :type fp: zipfile.ZipFile
        """
        self.filepath = None
        self.fp = fp
        self.containers = container.parse(self.fp)
        self.saved = False

    def append(self, container):
        assert(container not in self.containers)
        self.containers.append(container)

    def setFilePath(self, filepath):
        self.filepath = filepath

    def save(self):
        assert(self.filepath is not None)
        fp = tempfile.NamedTemporaryFile()
        archive = zipfile.ZipFile(fp, "w")
        for container in self.containers:
            print(container)
            container.archive(archive)
        archive.close()
        shutil.copyfile(fp.name, self.filepath)

    @staticmethod
    def create():
        return ProjectFile(zipfile.ZipFile(BytesIO(), "a"))
