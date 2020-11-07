import bpy
import numpy as np
import bmesh

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

    verts = np.zeros((len(xvals),len(yvals),3)) # grid of vertices

    for i, xval in enumerate(xvals):
        for j, yval in enumerate(yvals):
                            
            # mark specific points, if not in the vicinity of any point this does nothing
            found_point = False
            for k, point in enumerate(points):
                point_zval = function(point[0],point[1])
                # set caps on zvalue
                if minz is not None:
                    point_zval = max(point_zval,minz)
                if maxz is not None:
                    point_zval = min(point_zval,maxz)
                
                radius = points_radius[k]
                if (np.sqrt((xval-point[0])**2+(yval-point[1])**2))<radius:
                    zval = point_zval+points_dz[k]
                    found_point = True
            if found_point:
                verts[i,j] = np.array([xval,yval,zval])
                continue
                    
                    
            zval = function(xval,yval)
            if len(contours)>0: # if we have to plot contours we need the gradient information
                grad = abs_grad_function(xval,yval)
            
            # adjust z values to make contours
            # essentially, in the proximity of a contour line the surface is flattened to the
            # value of the desired contour
            for k, contour in enumerate(contours):
                contour_width = contour_widths[k]
                #estimate if distance to contour line is smaller than condour_width using gradient
                if abs(zval-contour) < grad*contour_width/2:
                    zval = contour

            # set caps on zvalue
            if minz is not None:
                zval = max(zval,minz)
            if maxz is not None:
                zval = min(zval,maxz)
                
            # save this vertex
            verts[i,j] = np.array([xval,yval,zval])
            
    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    obj = bpy.data.objects.new("MyObject", mesh)  # add a new object using the mesh
    
    scene = bpy.context.scene
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj  # set as the active object in the scene
    obj.select_set(True)
    
    mesh = bpy.context.object.data
    bm = bmesh.new()
    
    # this list of lists will contain all the actual mesh vertices
    # we store them to add the faces afterfards.
    vertex_matrix = [[None for x in range(len(xvals))] for y in range(len(yvals))] 
    for i, xval in enumerate(xvals):
        for j, yval in enumerate(yvals):
            v = verts[i,j]
            vertex_matrix[i][j] = bm.verts.new(v)  # add a new vert
    
    # draw all faces
    for i in range(len(xvals)-1):
        for j in range(len(yvals)-1):
            v1 = vertex_matrix[i][j]
            v2 = vertex_matrix[i+1][j]
            v3 = vertex_matrix[i][j+1]
            v4 = vertex_matrix[i+1][j+1]
            face1 = bm.faces.new((v1, v2, v3))
            face2 = bm.faces.new((v2, v3, v4))
            face2.normal_flip()
    
    # make the bmesh the object's mesh
    bm.to_mesh(mesh)  
    bm.free()  # always do this when finished

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
