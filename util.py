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


def iter_dots(n, distance, allowed_misses=10000, verbose=False):
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
    misses = 0
    dots = []

    def distance_okay(p1, p2):
        return great_circle_distance(p1, p2) < distance

    while len(dots) < n and misses < allowed_misses:
        if verbose:
            print('Dots:', len(dots), ', Misses:', misses)
        latitude = (random.random() * 2 - 1) * np.pi / 2
        longitude = (random.random() * 2 - 1) * np.pi
        candidate = latitude, longitude
        if any([distance_okay(dot, candidate)for dot in dots]):
            misses += 1
            continue    
        dots.append(candidate)
        misses = 0
        yield candidate
