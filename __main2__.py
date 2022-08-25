from projectionViewer import ProjectionViewer 
import wireframe
import numpy as np
from obj_loader import OBJ_loader
import random
from mesh_floor import *
from building_generator import *
import os
from Classes.Light import Light

import tkinter as tk

from tkinter import filedialog

root = tk.Tk()
root.withdraw()

load_ball_1= OBJ_loader('./Assets/sphere.obj' , 50)
grid= OBJ_loader('./Assets/grid.obj' , 50)

gridwf = grid.create_wireframe()
gridwf.showFaces = False
gridwf.showEdges = False

ball1 = load_ball_1.create_wireframe()
ball1.showEdges = False

pv = ProjectionViewer(1200, 1000, ball1)
	
pv.addWireframe('ball1', ball1)
pv.addWireframe('grid', gridwf)

light1 = Light((500, 200, -100), 1)

pv.addLight('Light1', light1)

pv.run()