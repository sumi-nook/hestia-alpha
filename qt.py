# -*- coding: utf-8 -*-

import six

from PyQt4.Qt import *

VERSION = 4

def toUnicode(x):
    if VERSION == 4:
        return six.text_type(x)
    return x
