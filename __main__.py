from projectionViewer import ProjectionViewer 
import wireframe
import numpy as np
from obj_loader import OBJ_loader
import random
from mesh_floor import *
from building_generator import *


cube = wireframe.Wireframe()

axes = wireframe.Wireframe()

a = np.array([[0,0,0],[1000,0,0], [0,1000,0], [0,0,1000], [1000, 1000, 1000], [1000, 1000, 0], [1000, 0, 1000], [0, 1000, 1000]])

b = np.array([[0,0,0],[10000,0,0],[10000, 0, 10000], [0,0,10000]])

cube.addNodes(a)
# cube.addEdges([(0,1), (0,2), (0,3)])
cube.addEdges([(0,1), (0,2), (0,3)])
cube.addEdges([(4,5), (4,6), (4,7)])

axes.addNodes(b)
axes.addFaces([(0,1,2,(0,100,20))])
axes.addFaces([(2,3,0,(0,100,20))])


cube.addFaces([(0,2,3,(100,0,0))])
cube.addFaces([(0,1,3,(40,0,0))])
cube.addFaces([(0,1,2,(255,0,0))])
cube.addFaces([(4,5,6,(255,0,0))])
cube.addFaces([(4,5,7,(100,0,0))])
cube.addFaces([(3,4,7,(50,0,0))])
cube.addFaces([(3,4,6,(50,0,0))])
cube.addFaces([(2,3,7,(100,0,0))])
cube.addFaces([(2,5,7,(100,0,0))])
cube.addFaces([(1,2,5,(255,0,0))])
cube.addFaces([(1,6,3,(100,0,0))])
cube.addFaces([(1,6,5,(255,0,0))])
	
pv = ProjectionViewer(1200, 1000, cube)
	
pv.addWireframe('cube', cube)
pv.addWireframe('axes', axes)

pv.run()