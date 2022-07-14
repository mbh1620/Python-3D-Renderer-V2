from projectionViewer import ProjectionViewer 
import wireframe
import numpy as np
from obj_loader import OBJ_loader
import random
from mesh_floor import *
from building_generator import *
import os
from Classes.Light import Light

files = os.scandir('./Assets/')

load_deer= OBJ_loader('./Assets/cone.obj', 50)

deer = load_deer.create_wireframe()

pv = ProjectionViewer(1200, 1000, deer)
	
pv.addWireframe('deer', deer)

light1 = Light((-1000, -100, 0), 1)

pv.addLight('Light1', light1)

pv.run()