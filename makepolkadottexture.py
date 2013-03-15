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
from PIL import Image
import util

#-----------------------------------------------------------------------------
# Script parameters
#------------------------------------------------------------------------------
dot_r = 0.1
dot_n = 150
dot_min_distance = 2.5 * dot_r
image_size = 2048, 1024
image_filename = 'texture.png'

#------------------------------------------------------------------------------
# Create array of cylinder coordinates for each pixel of the texture
#------------------------------------------------------------------------------
angles = np.linspace(0, 2 * np.pi, image_size[0])
height = np.linspace(0, 1., image_size[1])
angle_grid, height_grid = np.meshgrid(angles, height)

#------------------------------------------------------------------------------
# Convert cylinder coordinates to spherical coordinates
#------------------------------------------------------------------------------
spherical_points = util.cylindric_to_spheric(height_grid, angle_grid)

#------------------------------------------------------------------------------
# Compute distances to each randomly generated point on the sphere
# Keep the minimal distance for each pixel
#------------------------------------------------------------------------------
dots = util.iter_dots(dot_n, dot_min_distance)
min_distances = util.great_circle_distance(spherical_points, next(dots))
for dot in dots:
    distances = util.great_circle_distance(spherical_points, dot)
    np.minimum(distances, min_distances, out=min_distances)

#------------------------------------------------------------------------------
# Use the float array to create an array of uint8, containing either black if
# the minimal distance for a given pixel to any of the points is below
# the dot_r or white otherwise
#------------------------------------------------------------------------------
black = np.zeros(image_size, dtype=np.uint8)
white = np.ones(image_size, dtype=np.uint8) * 255
spherical_projected_texture = np.where(min_distances.T < dot_r, black, white)

#------------------------------------------------------------------------------
# Save the array to an image
#------------------------------------------------------------------------------
image = Image.fromarray(spherical_projected_texture.T)
image.save(image_filename)
