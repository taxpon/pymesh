# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import datetime
import math
import numpy
import os
import struct
from . import __title__
from . import __version__
from . import __url__

MODE_STL_AUTO = 0
MODE_STL_ASCII = 1
MODE_STL_BINARY = 2


class BaseMesh(object):

    stl_dtype = numpy.dtype([
        ('normals', numpy.float32, (3, )),
        ('vectors', numpy.float32, (3, 3)),
        ('attr', numpy.uint16, (1, )),
    ])

    def __init__(self):
        self.data = None
        self.normals = []
        self.vectors = []
        self.attr = []
        self.mode = MODE_STL_BINARY

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
        v2 = self.vectors[:, 2, :3]
        _normals = numpy.cross(v1 - v0, v2 - v0)

        for i in range(len(_normals)):
            norm = numpy.linalg.norm(_normals[i])
            if norm != 0:
                _normals[i] /= numpy.linalg.norm(_normals[i])

        self.normals[:] = _normals

    #####################################################################
    # Save functions
    #

    # STL
    def save_stl(self, filename, mode=MODE_STL_AUTO, update_normals=True):
        """Save data with stl format
        :param str filename:
        :param int mode:
        :param bool update_normals:
        """
        if update_normals:
            self.update_normals()

        name = os.path.split(filename)[-1]

        if mode is MODE_STL_AUTO:
            if self.mode == MODE_STL_BINARY:
                save_func = self.__save_stl_binary

            elif self.mode == MODE_STL_ASCII:
                save_func = self.__save_stl_ascii

            else:
                raise ValueError("Mode %r is invalid" % mode)

        elif mode is MODE_STL_BINARY:
            save_func = self.__save_stl_binary

        else:
            raise ValueError("Mode %r is invalid" % mode)

        with open(name, 'wb') as fh:
            save_func(fh, filename)

    def __save_stl_binary(self, fh, name):
        fh.write(("%s (%s) %s %s" % (
            "{}".format(__title__),
            "{}".format(__version__),
            datetime.datetime.now(),
            name
        ))[:80].ljust(80, ' '))

        bin_data = numpy.zeros(self.data.size, BaseMesh.stl_dtype)
        bin_data['normals'] = self.normals[:]
        bin_data['vectors'] = self.vectors[:, :, :3]
        bin_data['attr'] = self.attr
        fh.write(struct.pack('i', bin_data.size))
        bin_data.tofile(fh)

    def __save_stl_ascii(self, fh, name):
        print("solid {}".format(name), file=fh)
        for i in range(len(self.vectors)):
            print("facet normal %f %f %f" % tuple(self.normals[i][:3]), file=fh)
            print("  outer loop", file=fh)
            print("    vertex %f %f %f" % tuple(self.vectors[i][0][:3]), file=fh)
            print("    vertex %f %f %f" % tuple(self.vectors[i][1][:3]), file=fh)
            print("    vertex %f %f %f" % tuple(self.vectors[i][2][:3]), file=fh)
            print("  endloop", file=fh)
            print("endfacet", file=fh)
        print("endsolid {}".format(name), file=fh)

    # OBJ
    def save_obj(self, filename, update_normals=True):
        """Save data with OBJ format
        :param stl filename:
        :param bool update_normals:
        """
        if update_normals:
            self.update_normals()

        # Create triangle_list
        vectors_key_list = []
        vectors_list = []
        normals_key_list = []
        normals_list = []
        triangle_list = []
        for i, vector in enumerate(self.vectors):
            one_triangle = []
            for j in range(3):
                v_key = ",".join(map(str, self.vectors[i][j][:3]))
                if v_key in vectors_key_list:
                    v_index = vectors_key_list.index(v_key)
                else:
                    v_index = len(vectors_key_list)
                    vectors_key_list.append(v_key)
                    vectors_list.append(self.vectors[i][j][:3])
                one_triangle.append(v_index + 1)

            n_key = ",".join(map(str, self.normals[i][:3]))
            if n_key in normals_key_list:
                n_index = normals_key_list.index(n_key)
            else:
                n_index = len(normals_key_list)
                normals_key_list.append(n_key)
                normals_list.append(self.normals[i][:3])

            # print(normals_list)
            triangle_list.append((one_triangle, n_index + 1))

        with open(filename, "wb") as fh:
            print("# {} {}".format(__title__, __version__), file=fh)
            print("# {}".format(datetime.datetime.now()), file=fh)
            print("# {}".format(__url__), file=fh)
            print("", file=fh)
            for v in vectors_list:
                print("v {} {} {}".format(v[0], v[1], v[2]), file=fh)
            for vn in normals_list:
                print("vn {} {} {}".format(vn[0], vn[1], vn[2]), file=fh)
            for t in triangle_list:
                faces = t[0]
                normal = t[1]

                print("f {}//{} {}//{} {}//{}".format(
                    faces[0], normal,
                    faces[1], normal,
                    faces[2], normal,
                ), file=fh)

