# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import numpy
import os
import struct
from .base import BaseMesh


class Stl(BaseMesh):

    MODE_AUTO = 0
    MODE_ASCII = 1
    MODE_BINARY = 2

    HEADER_SIZE = 80
    COUNT_SIZE = 4
    MAX_COUNT = 1e6
    BUFFER_SIZE = 4096

    stl_dtype = numpy.dtype([
        ('normals', numpy.float32, (3, )),
        ('vectors', numpy.float32, (3, 3)),
        ('attr', numpy.uint16, (1, )),
    ])

    def __init__(self, filename, mode=MODE_AUTO):
        """Craete a instance of Stl.
        :param str filename: The filename to open
        :param int mode: The mode to open, default is :py:data:`AUTOMATIC`.
        """
        super(Stl, self).__init__()

        with open(filename, "rb") as fh:
            name, data, mode = Stl.__load(fh, mode=mode)

        self.name = name
        self.data = data
        self.mode = mode
        self.normals = data['normals']
        self.vectors = numpy.ones((
            data['vectors'].shape[0],
            data['vectors'].shape[1],
            data['vectors'].shape[2] + 1
        ))
        self.vectors[:, :, :-1] = data['vectors']
        self.attr = data['attr']

    @staticmethod
    def __load(fh, mode=MODE_AUTO):
        """Load Mesh from STL file

        :param FileIO fh: The file handle to open
        :param int mode: The mode to open, default is :py:data:`AUTOMATIC`.
        :return:
        """
        header = fh.read(Stl.HEADER_SIZE).lower()
        name = ""
        data = None
        if not header.strip():
            return

        if mode in (Stl.MODE_AUTO, Stl.MODE_ASCII) and header.startswith('solid'):
            try:
                name = header.split('\n', 1)[0][:5].strip()
                data = Stl.__load_ascii(fh, header)
                mode = Stl.MODE_ASCII

            except:
                pass

        else:
            data = Stl.__load_binary(fh)
            mode = Stl.MODE_BINARY

        return name, data, mode

    @staticmethod
    def __load_binary(fh):
        # Read the triangle count
        count, = struct.unpack("i", fh.read(Stl.COUNT_SIZE))
        assert count < Stl.MAX_COUNT, \
            'File too large, got {} triangles which exceeds the maximum of {}' .format(
                count, Stl.MAX_COUNT
            )
        return numpy.fromfile(fh, Stl.stl_dtype, count=count)

    @staticmethod
    def __load_ascii(fh, header):
        return numpy.fromiter(Stl.__ascii_reader(fh, header), dtype=Stl.stl_dtype)

    @staticmethod
    def __ascii_reader(fh, header):
        """
        :param fh:
        :param header:
        :return:
        """

        lines = header.split('\n')
        recoverable = [True]

        def get(prefix=''):
            if lines:
                line = lines.pop(0)
            else:
                raise RuntimeError(recoverable[0], 'Unable to find more lines')

            if not lines:
                recoverable[0] = False

                # Read more lines and make sure we prepend any old data
                lines[:] = fh.read(Stl.BUFFER_SIZE).split('\n')
                line += lines.pop(0)
            line = line.lower().strip()
            if prefix:
                if line.startswith(prefix):
                    values = line.replace(prefix, '', 1).strip().split()
                elif line.startswith('endsolid'):
                    raise StopIteration()
                else:
                    raise RuntimeError(recoverable[0],
                                       '%r should start with %r' % (line,
                                                                    prefix))

                if len(values) == 3:
                    vertex = [float(v) for v in values]
                    return vertex
                else:  # pragma: no cover
                    raise RuntimeError(recoverable[0],
                                       'Incorrect value %r' % line)
            else:
                return line

        line = get()
        if not line.startswith('solid ') and line.startswith('solid'):
            print("Error")

        if not lines:
            raise RuntimeError(recoverable[0],
                               'No lines found, impossible to read')

        while True:
            # Read from the header lines first, until that point we can recover
            # and go to the binary option. After that we cannot due to
            # unseekable files such as sys.stdin
            #
            # Numpy doesn't support any non-file types so wrapping with a
            # buffer and/or StringIO does not work.
            try:
                normals = get('facet normal')
                assert get() == 'outer loop'
                v0 = get('vertex')
                v1 = get('vertex')
                v2 = get('vertex')
                assert get() == 'endloop'
                assert get() == 'endfacet'
                attrs = 0
                yield (normals, (v0, v1, v2), attrs)
            except AssertionError, e:
                raise RuntimeError(recoverable[0], e)
            except StopIteration:
                if any(lines):
                    # Seek back to where the next solid should begin
                    fh.seek(-len('\n'.join(lines)), os.SEEK_CUR)
                raise

