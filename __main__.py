from projectionViewer import ProjectionViewer 
import wireframe
import numpy as np
from obj_loader import OBJ_loader
import random
import os
from Classes.Light import Light

import tkinter as tk

from tkinter import filedialog

root = tk.Tk()
root.withdraw()

grid= OBJ_loader('./Assets/grid.obj' , 50)

ball= OBJ_loader('./Assets/ball.obj' , 50)

# planeCreator= OBJ_loader('./Assets/cube.obj' , 100)

center_point = wireframe.Wireframe()

nodes = np.array([[0,0,0]])

center_point.addNodes(nodes)

gridwf = grid.create_wireframe()

gridwf.showFaces = False
gridwf.showEdges = False

pv = ProjectionViewer(1200, 1000, center_point)

#Default 1200 x 1000
#Monitor 2560 x 1440

pv.addWireframe('center_point', center_point)
pv.addWireframe('grid', gridwf)

light1 = Light((100, 100, -100), 1)

pv.addLight('Light1', light1)

pv.translateAll([600, 0, 0])

pv.run()