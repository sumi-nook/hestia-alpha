# -*- coding: utf-8 -*-

from __future__ import print_function

from OpenGL.GL import *


class GlobalEnvironment(object):
    def __init__(self):
        self.vendor = self.get_string(GL_VENDOR)
        self.renderer = self.get_string(GL_RENDERER)
        self.version = self.get_string(GL_VERSION)
        self.extensions = self.get_string(GL_EXTENSIONS).split()
        self.max_vertex_attribs = self.get_integer(GL_MAX_VERTEX_ATTRIBS)
        self.max_varying_vectors = self.get_integer(GL_MAX_VARYING_VECTORS)
        self.max_vertex_uniform_vectors = self.get_integer(GL_MAX_VERTEX_UNIFORM_VECTORS)
        self.max_fragment_uniform_vectors = self.get_integer(GL_MAX_FRAGMENT_UNIFORM_VECTORS)
        self.max_vertex_texture_image_units = self.get_integer(GL_MAX_VERTEX_TEXTURE_IMAGE_UNITS)
        self.max_texture_image_units = self.get_integer(GL_MAX_TEXTURE_IMAGE_UNITS)
        self.max_texture_coords = self.get_integer(GL_MAX_TEXTURE_COORDS)
        self.max_texture_size = self.get_integer(GL_MAX_TEXTURE_SIZE)
        self.max_cube_map_texture_size = self.get_integer(GL_MAX_CUBE_MAP_TEXTURE_SIZE)
        self.max_renderbuffer_size = self.get_integer(GL_MAX_RENDERBUFFER_SIZE)
        self.max_viewport_dims = self.get_integer(GL_MAX_VIEWPORT_DIMS)

    def dump(self):
        print("Vendor:", self.vendor)
        print("GPU:", self.renderer)
        print("Ver:", self.version)
        #print("Extensions:", self.extensions)
        print("MAX_VERTEX_ATTRIBS:", self.max_vertex_attribs)
        print("MAX_VARYING_VECTORS:", self.max_varying_vectors)
        print("MAX_VERTEX_UNIFORM_VECTORS:", self.max_vertex_uniform_vectors)
        print("MAX_FRAGMENT_UNIFORM_VECTORS:", self.max_fragment_uniform_vectors)
        print("MAX_VERTEX_TEXTURE_IMAGE_UNITS:", self.max_vertex_texture_image_units)
        print("MAX_TEXTURE_IMAGE_UNITS:", self.max_texture_image_units)
        print("MAX_TEXTURE_COORDS:", self.max_texture_coords)
        print("MAX_TEXTURE_SIZE:", self.max_texture_size)
        print("MAX_CUBE_MAP_TEXTURE_SIZE:", self.max_cube_map_texture_size)
        print("MAX_RENDERBUFFER_SIZE:", self.max_renderbuffer_size)
        print("MAX_VIEWPORT_DIMS:", self.max_viewport_dims)

    @classmethod
    def get_string(cls, n):
        return glGetString(n)

    @classmethod
    def get_integer(cls, n):
        try:
            return glGetInteger(n)
        except:
            return None
