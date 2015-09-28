# -*- coding: utf-8 -*-

import numpy
import math


class BaseMesh(object):

    def __init__(self):
        self.normals = None
        self.vectors = None

    def rotate_x(self, deg):
        """Rotate mesh around x-axis

        :param float deg: Rotation angle (degree)
        :return:
        """
        rad = math.radians(deg)
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, math.cos(rad), math.sin(rad), 0],
            [0, -math.sin(rad), math.cos(rad), 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return

    def rotate_y(self, deg):
        """Rotate mesh around y-axis

        :param float deg: Rotation angle (degree)
        """
        rad = math.radians(deg)
        mat = numpy.array([
            [math.cos(rad), 0, -math.sin(rad), 0],
            [0, 1, 0, 0],
            [math.sin(rad), 0, math.cos(rad), 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return

    def rotate_z(self, deg):
        """Rotate mesh around z-axis

        :param float deg: Rotation angle (degree)
        """
        rad = math.radians(deg)
        mat = numpy.array([
            [math.cos(rad), math.sin(rad), 0, 0],
            [-math.sin(rad), math.cos(rad), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return

    def translate_x(self, d):
        """Translate mesh for x-direction

        :param float d: Amount to translate
        """
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [d, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return

    def translate_y(self, d):
        """Translate mesh for y-direction

        :param float d: Amount to translate
        """
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, d, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return

    def translate_z(self, d):
        """Translate mesh for z-direction

        :param float d: Amount to translate
        """
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, d, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return

    def scale(self, sx, sy, sz):
        """Scale mesh

        :param float sx: Amount to scale for x-direction
        :param float sy: Amount to scale for y-direction
        :param float sz: Amount to scale for z-direction
        """
        mat = numpy.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return

    def update_normals(self):
        v0 = self.vectors[:, 0, :3]
        v1 = self.vectors[:, 1, :3]
        v2 = self.vectors[:, 1, :3]
        _normals = numpy.cross(v1 - v0, v2 - v0)
        self.normals[:] = _normals
