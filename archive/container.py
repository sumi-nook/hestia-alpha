# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

class ContainerBase(object):
    def archive(self, archive):
        """
        :type archive: zipfile.ZipFile
        """
        raise NotImplementedError


class Scenario(ContainerBase):
    def __init__(self, filepath, content):
        self.filepath = filepath
        self.content = content

    def archive(self, archive):
        """
        :type archive: zipfile.ZipFile
        """
        assert(self.filepath is not None)
        archive.writestr(self.filepath, self.content)

    @staticmethod
    def create():
        return Scenario(None, b"")


EXT_MAP = {
    ".txt": Scenario,
    ".md": Scenario,
}


def parse(archive):
    """
    :type archive: zipfile.ZipFile
    """
    result = []
    for name in archive.namelist():
        root, ext = os.path.splitext(name)
        if ext not in EXT_MAP:
            continue
        result.append(EXT_MAP[ext](name, archive.read(name)))
    return result
