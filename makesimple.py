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
from PIL import Image, ImageDraw
import util

#-----------------------------------------------------------------------------
# Script parameters
#------------------------------------------------------------------------------
dot_r = 0.05
max_dot_n = 100
dot_min_distance = 2.5 * dot_r
border_distance = dot_r
image_size = 1024, 1024
image_filename = 'texture.png'


#------------------------------------------------------------------------------
# Save the array to an image
#------------------------------------------------------------------------------
image = Image.new('RGB', image_size, (255, 255, 255))
draw = ImageDraw.Draw(image)
dot_iter = util.iter_dots_on_plane(max_dot_n, dot_min_distance,
                                  border_distance=border_distance)
for dot in dot_iter:
    x, y = dot
    x_left = (x - dot_r) * image_size[0]
    x_right = (x + dot_r) * image_size[0]
    y_upper = (y - dot_r) * image_size[1]
    y_lower = (y + dot_r) * image_size[1]
    draw.ellipse((x_left, y_upper, x_right, y_lower), fill=(0, 0, 0))
image.save(image_filename)
