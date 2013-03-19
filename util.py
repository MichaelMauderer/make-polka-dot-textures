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
import numpy as np
import random
from abc import ABCMeta, abstractmethod


def great_circle_distance(standpoint, forepoint):
    """
    Returns the great circle distance of two points on the unit sphere.

    Uses the Haversine formula.
    See: http://en.wikipedia.org/wiki/Great-circle_distance
         http://en.wikipedia.org/wiki/Haversine_formula

    Parameters
    ----------
    standpoint : Point on the unitsphere.
    forepoint : Point on the unitsphere.
    """
    phi_s, lambda_s = standpoint
    phi_f, lambda_f = forepoint
    d_lambda = np.abs(lambda_f - lambda_s)
    d_phi = np.abs(phi_s - phi_f)

    result = np.sin(d_phi / 2) ** 2
    result += np.cos(phi_s) * np.cos(phi_f) * (np.sin(d_lambda / 2) ** 2)
    result = 2 * np.arcsin(np.sqrt(result))

    return result


def cylindric_to_spheric(height, angle):
    """
    Convert cylindric coordinates on a unit cylinder to sperical coordinates
    on a unit sphere.

    Parameters
    ----------
    height : Height between 0 and 1.
    angle : Angle between 0 and 2pi.

    Returns
    -------
    Coordinates tuple of the following values:

    latitude : Latitude between -pi and pi.
    longitude : Longitude between -pi/2 and pi/2

    """
    longitude = angle - np.pi
    latitude = np.arcsin(2 * height - 1)

    return latitude, longitude


class _iter_random_dots_base():
    """
    Yields up to n coordinates of points with the minimal
    given distance to all other points.
    Since the used algorithm may not guarantee termination a upper limit
    for attempts to generate a valid point is given. If this limit is reached
    the iterator will stop prematurely.

    Parameters
    ----------
    n : Maximum number of dots to create
    min_distance : Minimal distance between any points.
    allowed_misses : upper limit for attempts to generate a valid point.
    verbose: If True will print current state of the algorithm.
             Amount of created dots, amount of current misses.

    Returns
    -------
    Point as tuple
    """

    __metaclass__ = ABCMeta

    def __init__(self, n, min_distance, allowed_misses=10000, verbose=False):
        self.n = n
        self.min_distance = min_distance
        self.allowed_misses = allowed_misses
        self.verbose = verbose
        self.dots = []
        self.misses = 0

    @abstractmethod
    def point_distance(self, p1, p2):
        return None

    @abstractmethod
    def create_random_point(self):
        return None

    def __iter__(self):
        return self

    def __next__(self):
        while len(self.dots) < self.n and self.misses < self.allowed_misses:
            if self.verbose:
                print('Dots:', len(self.dots), ' Misses:', self.misses)
            candidate = self.create_random_point()
            if any([self.point_distance(dot, candidate)for dot in self.dots]):
                self.misses += 1
                continue
            self.dots.append(candidate)
            self.misses = 0
            return candidate
        raise  StopIteration


class iter_dots_on_sphere(_iter_random_dots_base):
    """
    Yields up to n coordinates of points on a unitsphere each with the minimal
    given distance to all other points.
    Since the used algorithm does not guarantee termination a upper limit
    for attempts to generate a valid point is given. If this limit is reached
    the iterator will stop prematurely.

    Parameters
    ----------
    n : Maximum number of dots to create
    distance : Minimal distance between all points.
    allowed_misses : upper limit for attempts to generate a valid point.
    verbose: If True will print current state of the algorithm.
             Amount of created dots, amount of current misses.

    Returns
    -------
    Point as tuple of the following values:

    latitude : Latitude between -pi and pi.
    longitude : Longitude between -pi/2 and pi/2
    """
    def point_distance(self, p1, p2):
        return great_circle_distance(p1, p2) < self.min_distance

    def create_random_point(self):
        latitude = (random.random() * 2 - 1) * np.pi / 2
        longitude = (random.random() * 2 - 1) * np.pi
        return latitude, longitude


class iter_dots_on_plane(_iter_random_dots_base):
    """
    Yields up to n coordinates of points on a unitplane each with the minimal
    given distance to any other point.
    Since the used algorithm does not guarantee termination a upper limit
    for attempts to generate a valid point is given. If this limit is reached
    the iterator will stop prematurely.

    Parameters
    ----------
    n : Maximum number of dots to create
    min_distance : Minimal distance between all points.
    allowed_misses : upper limit for attempts to generate a valid point.
    verbose: If True will print current state of the algorithm.
             Amount of created dots, amount of current misses.

    Returns
    -------
    Point as tuple of the following values:

    x : x-coordinate in range 0..1.
    y : y-coordinate in range 0..1
    """
    def point_distance(self, p1, p2):
        distance = abs(np.linalg.norm(p1 - p2))
        return distance < self.min_distance

    def create_random_point(self):
        x = random.random()
        y = random.random()
        return x, y
