from projectionViewer import ProjectionViewer 
import wireframe
import numpy as np
from obj_loader import OBJ_loader
import random
from mesh_floor import *
from building_generator import *

load_deer= OBJ_loader('./Assets/deer.obj', 100)
load_cube= OBJ_loader('./Assets/untitled.obj', 100)

cube = load_cube.create_wireframe()
deer = load_deer.create_wireframe()
	
pv = ProjectionViewer(1200, 1000, cube)
	
pv.addWireframe('cube', cube)
pv.addWireframe('deer', deer)

pv.run()