make-polka-sphere-texture
=========================

Contains three scripts to create random polka dot textures.

makesimple.py creates an image containing polka dots.

makepolygon.py creates an image containing polka dots that are bounded by a polygon.
The example uses a regular octagon.

makesherical.py crates a texture containing the cylindric projection of a sphere covered
in randomly distributed polka dots. This texture can then be used to render
a correctly textured sphere by reprojecting the texture using a cylindric 
projection.