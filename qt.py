# -*- coding: utf-8 -*-

import six

from PyQt4.Qt import *
from PyQt4.QtOpenGL import *

VERSION = 4

def toUnicode(x):
    if VERSION == 4:
        return six.text_type(x)
    return x


if VERSION == 5:
    QString = str
