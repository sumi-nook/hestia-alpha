import os

import py2exe
from distutils.core import setup

includes = ["sip", "lxml._elementpath",
            "markdown.extensions.nl2br"]
excludes = []
dll_excludes = ["w9xpopen.exe"]

if os.name == "nt":
    includes.append("OpenGL.platform.win32")

py2exe_options = {
    "compressed": 1,
    "optimize": 2,
    "bundle_files": 1,
    "includes" : includes,
    "excludes": excludes,
    "dll_excludes": dll_excludes,
}

setup(
    options={"py2exe" : py2exe_options},
    windows=[{"script" : "main.py",
              "dest_base": "Hestia",
              # version info.
              "version": "0.0.0.4",
              "name": "Hestia",
              "company_name:": "nook",
              "copyright": "Copyright (c) 2016 S2_SUMI.",
              "description": "Common Intermediate Script System"}],
    zipfile=None,
)
