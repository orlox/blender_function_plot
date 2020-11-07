# blender_function_plot
Simple script to create a mesh from a 2d function in blender

You can simply add the code in function_plotter.py to a text viewport and run to create an example mesh. Or just open the included blend file which has the code already in it.
The code defines a create_mesh function
```python
#create a mesh with z values defined by a functions. Arguments are:
# xvals: x values of the mesh (1d array)
# yvals: y values of the mesh (1d array)
# function: function that defines z=function(x,y)
# abs_grad_function: function that returns the absolute value of the gradient at a point
#                    only needed to plot contours
# minz, maxz: if defined, clip the function to this minimum and maximum values
# contours: values in z for which we make contour lines 
# contour_widths: width of contour lines
# points: list with (x,y) tuples where we make small cylinders. These are to indicate potentially
#         interesting points
# points_radius: radius of each cylinder defined by points
# points_dz: the top of the cylinder is at a point function(x,y)+dz,
#            with points_dz defining dz for each
def create_mesh(xvals, yvals, function, abs_grad_function,
        minz=None, maxz=None, contours=[], contour_widths=[], points=[], points_radius=[], points_dz=[]):
```
and as an example, does
```python
import numpy as np

# sample function between -3<x<3 and -3<y<3 with
# 1000 points in each dimension
xvals = np.linspace(-3,3,1000)
yvals = np.linspace(-3,3,1000)

def example_function(x,y):
    r = np.sqrt(np.power(x,2)+np.power(y,2))
    return np.power(r,2)*np.sin(r*5)/10

def example_abs_grad(x,y):
    r = np.sqrt(np.power(x,2)+np.power(y,2))
    return abs(2*r*np.sin(r*5)+np.power(r,2)*np.cos(r*5)*5)/10

create_mesh(xvals,yvals,example_function,example_abs_grad,\
    contours=[-0.5,0,0.5],contour_widths=[0.05,0.05,0.05],\
    points=[(0,0),(1,1),(-1,-1)],points_radius=[0.1,0.1,0.1],points_dz=[0.4,0.4,0.4])
```
Inside blender this produces
![GitHub Logo](/example.png)
