#******************************************************************************
# Copyright (C) 2013 Michael Mauderer <mail@MichaelMauderer.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all  copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE
#
#******************************************************************************
import unittest
import numpy as np
from util import cylindric_to_spheric, great_circle_distance


class DistanceCalculationTest(unittest.TestCase):

    def assert_distance(self, p1, p2, expected_distance):
        distance = great_circle_distance(p1, p2)
        self.assertAlmostEqual(expected_distance, distance)

    def test_distance_calculation_zero(self):
        self.assert_distance((0, 0), (0, 0), 0)

    def test_distance_calculation_poles(self):
        self.assert_distance((-np.pi / 2, 0), (np.pi / 2, 0), np.pi)
        self.assert_distance((-np.pi / 2, 1), (np.pi / 2, 0), np.pi)
        self.assert_distance((-np.pi / 2, 0), (np.pi / 2, 1), np.pi)
        self.assert_distance((-np.pi / 2, np.pi), (np.pi / 2, np.pi), np.pi)


class CoordinateTransformationTest(unittest.TestCase):

    def assert_transformation(self, cylindric, spherical):
        transformed = cylindric_to_spheric(*cylindric)
        self.assertAlmostEqual(transformed[0], spherical[0])
        self.assertAlmostEqual(transformed[1], spherical[1])

    def assert_latitude_transformation(self, cylindric, spherical):
        transformed = cylindric_to_spheric(*cylindric)
        self.assertAlmostEqual(transformed[0], spherical[0])

    def assert_longitude_transformation(self, cylindric, spherical):
        transformed = cylindric_to_spheric(*cylindric)
        self.assertAlmostEqual(transformed[1], spherical[1])

    def test_transformation_poles(self):
        self.assert_latitude_transformation((0, 0), (-np.pi / 2, 0))
        self.assert_latitude_transformation((1, 0), (np.pi / 2, 0))

    def test_equator_transformation(self):
        self.assert_latitude_transformation((0.5, 0), (0, 0))

        self.assert_longitude_transformation((0.5, 0), (0, -np.pi))
        self.assert_longitude_transformation((0.5, np.pi), (0, 0))

if __name__ == "__main__":
    unittest.main()
