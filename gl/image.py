# -*- coding: utf-8 -*-

from __future__ import division

import math

from OpenGL.GL import *

from qt import Qt
from qt import QColor
from qt import QImage
from qt import QPainter
from qt import QGLWidget

from utility import bits

from .base import Rect
from .base import DrawObject
from .environment import GlobalEnvironment
from .texture import Texture


def power_of_two(size, maximum=None):
    """Calculate nearest power of two

    :type size: int
    :param size: input size
    :type maximum: int or None
    :param maximum: maximum size (must be 2**n)
    :return: nearest power of two value
    """
    length = bits.length(size)
    max_size = 2**length
    min_size = max_size >> 1
    result = 0
    if abs(max_size-size) < abs(size-min_size):
        result = max_size
    else:
        result = min_size
    if maximum is not None:
        assert power_of_two(maximum) == maximum
        return min(result, maximum)
    return result


def pot_resize(img, maximum=None):
    """Resize image to power of two

    :type img: QImage
    :param img: input image
    :type maximum: int or None
    :param maximum: maximum size (must be 2**n)
    :return: resized image
    """
    w, h = img.width(), img.height()
    base = power_of_two(max(w, h), maximum=maximum)
    if w > h:
        aspect = h / w
        h = int(math.ceil(aspect * base))
        w = base
    else:
        aspect = w / h
        w = int(math.ceil(aspect * base))
        h = base
    return img.scaled(w, h, Qt.KeepAspectRatio, Qt.FastTransformation)


def pot_square_resize(img, maximum=None):
    """Resize image to power of two square

    :type img: QImage
    :param img: input image
    :type maximum: int or None
    :param maximum: maximum size (must be 2**n)
    :return: resized image
    """
    resized = pot_resize(img, maximum=maximum)
    w, h = resized.width(), resized.height()
    base = max(w, h)
    #pad = base - min(w, h)
    new_img = QImage(base, base, img.format())
    new_img.fill(QColor(0, 0, 0))
    painter = QPainter(new_img)
    painter.drawImage(0, 0, resized)
    return new_img, w / base, h / base


class ImageTexture(Texture):
    def __init__(self, mode, x, y, width, height, data, rect=None):
        super(ImageTexture, self).__init__()
        self.mode = mode
        # mapping size
        self.x = x
        self.y = y
        # image size
        self.width = width
        self.height = height
        self.data = data

        # image rect
        self.rect = rect
        if rect is None:
            self.rect = Rect(-1.0, -1.0, 1.0, 1.0)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, self.mode, self.width, self.height,
                     0, self.mode, GL_UNSIGNED_BYTE, self.data)

        # texture repeat option
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # texture zoom option
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def draw(self, ctx):
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        # left, top
        glTexCoord2d(1.0-self.x, 1.0-self.y)
        glVertex3d(self.rect.x, self.rect.y,  0.0)
        # left, bottom
        glTexCoord2d(1.0-self.x, 1.0)
        glVertex3d(self.rect.x, self.rect.h,  0.0)
        # right, bottom
        glTexCoord2d(1.0, 1.0)
        glVertex3d(self.rect.w, self.rect.h,  0.0)
        # right, top
        glTexCoord2d(1.0, 1.0-self.y)
        glVertex3d(self.rect.w, self.rect.y,  0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        glFlush()

    @staticmethod
    def create(path, rect=None):
        img = QImage(path)

        # convert to pot image
        pot_img, x, y = pot_square_resize(img)
        width, height = pot_img.width(), pot_img.height()

        # QImage format: 0xffRRGGBB
        mode = GL_RGBA

        # image data
        tex_img = QGLWidget.convertToGLFormat(pot_img)
        data = tex_img.bits().asstring(tex_img.numBytes())

        return ImageTexture(mode, x, y, width, height, data, rect)
