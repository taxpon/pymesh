# -*- coding: utf-8 -*-

import unittest
from pymesh import stl


class SimpleTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sample(self):
        m = stl.Stl('tests/data/data_bin.stl')
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
