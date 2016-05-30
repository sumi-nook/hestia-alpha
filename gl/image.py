# -*- coding: utf-8 -*-

import math

from OpenGL.GL import *
from PIL import Image

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

    :type img: PIL.Image
    :param img: input image
    :type maximum: int or None
    :param maximum: maximum size (must be 2**n)
    :return: resized image
    """
    w, h = img.size
    base = power_of_two(max(w, h), maximum=maximum)
    if w > h:
        aspect = float(h) / w
        h = int(math.ceil(aspect * base))
        w = base
    else:
        aspect = float(w) / h
        w = int(math.ceil(aspect * base))
        h = base
    return img.resize((w, h))


def pot_square_resize(img, maximum=None):
    """Resize image to power of two square

    :type img: PIL.Image
    :param img: input image
    :type maximum: int or None
    :param maximum: maximum size (must be 2**n)
    :return: resized image
    """
    resized = pot_resize(img, maximum=maximum)
    w, h = resized.size
    base = max(w, h)
    #pad = base - min(w, h)
    new_img = Image.new(img.mode, (base, base))
    new_img.paste(resized, (0, 0))
    return new_img, w / float(base), h / float(base)


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
        glTexCoord2d(0.0, self.y)
        glVertex3d(self.rect.x, self.rect.y,  0.0)
        # right, top
        glTexCoord2d(self.x, self.y)
        glVertex3d(self.rect.w, self.rect.y,  0.0)
        # right, bottom
        glTexCoord2d(self.x, 0.0)
        glVertex3d(self.rect.w, self.rect.h,  0.0)
        # left, bottom
        glTexCoord2d(0.0, 0.0)
        glVertex3d(self.rect.x, self.rect.h,  0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        glFlush()


class PILImageTexture(ImageTexture):
    @staticmethod
    def create(path, rect=None):
        from PIL import Image

        img = Image.open(path)

        # convert to pot image
        pot_img, x, y = pot_square_resize(img)
        width, height = pot_img.size

        # detect mode
        mode = None
        if pot_img.mode == "RGB":
            mode = GL_RGB
        else:
            mode = GL_RGBA

        # image data
        data = pot_img.tostring()

        return PILImageTexture(mode, x, y, width, height, data, rect)
