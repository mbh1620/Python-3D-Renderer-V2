from wireframe import *
import pygame
import numpy as np
from camera import *
import time
from Classes.Toolbar import Toolbar
from obj_loader import OBJ_loader
import tkinter as tk
from tkinter import filedialog

class ProjectionViewer:

	''' Displays 3D Objects on a Pygame Screen '''

	def __init__(self, width, height, center_point):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('3D Renderer')
		self.background = (10,10,50)

		#Setup camera
		self.camera = Camera([0,0,0],0,0)
		self.center_point = center_point

		self.wireframes = {}
		self.lights = {}

		self.displayNodes = False
		self.displayEdges = False
		self.displayFaces = True
		self.nodeColour = (255,255,255)
		self.edgeColour = (200,200,200)
		self.nodeRadius = 2

		self.toolbar = Toolbar(self.screen, self.width)

		pygame.init()

	def run(self):

		key_to_function = {
		pygame.K_LEFT: (lambda x: x.rotate_about_camera('Y', 0.05)),
 		pygame.K_RIGHT:(lambda x: x.rotate_about_camera('Y', -0.05)),
 		pygame.K_DOWN: (lambda x: x.translateAll([0,  10, 0])),
 		pygame.K_UP:   (lambda x: x.translateAll([0, -10, 0])),

 		pygame.K_w: (lambda x: x.move_cam_forward(20)),
 		pygame.K_s: (lambda x: x.move_cam_backward(20)),
 		pygame.K_a: (lambda x: x.move_cam_left(20)),
 		pygame.K_d: (lambda x: x.move_cam_right(20)),

		}

		running = True
		flag = False

		while running:

			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				elif event.type == pygame.MOUSEBUTTONUP:
					self.toolbar.process_click(pygame.mouse.get_pos())
				
			if keys[pygame.K_LEFT]:
				key_to_function[pygame.K_LEFT](self)
			if keys[pygame.K_RIGHT]:
				key_to_function[pygame.K_RIGHT](self)
			if keys[pygame.K_DOWN]:
				key_to_function[pygame.K_DOWN](self)
			if keys[pygame.K_UP]:
				key_to_function[pygame.K_UP](self)
			if keys[pygame.K_w]:
				key_to_function[pygame.K_w](self)
			if keys[pygame.K_a]:
				key_to_function[pygame.K_a](self)
			if keys[pygame.K_s]:
				key_to_function[pygame.K_s](self)
			if keys[pygame.K_d]:
				key_to_function[pygame.K_d](self)

			self.display()
			self.toolbar.render()

			if self.toolbar.open_flag == True:
				self.open_file()
				self.toolbar.open_flag = False

			pygame.display.flip()

	def addWireframe(self, name, wireframe):
		self.wireframes[name] = wireframe
		#translate to center
		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width,self.height,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def addLight(self, name, light):
		self.lights[name] = light

		lightWireframe = Wireframe()
		lightPosition = np.array([[light.position[0], light.position[1], light.position[2]]])
		lightWireframe.addNodes(lightPosition)

		self.wireframes[name] = lightWireframe

	def display(self):

		self.screen.fill(self.background)

		for wireframe in self.wireframes.values():
			wireframe.transform_for_perspective((self.width/2, self.height/2), self.camera.fov, self.camera.zoom)	

			if self.displayNodes:
				for node in wireframe.perspective_nodes:
					if node[2] > 0 and node[2] < 10000 and node[0] > 0 and node[0] < 1199:
						pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
			else:
				pass
			if self.displayEdges:
				for n1, n2 in wireframe.edges:
					clipN1 = self.clipNode(wireframe.perspective_nodes[n1])
					clipN2 = self.clipNode(wireframe.perspective_nodes[n2])
					if type(clipN1) == int or type(clipN2) == int:
						pass
					else:
						pygame.draw.aaline(self.screen, self.edgeColour, clipN1[:2], clipN2[:2], 1)

			else:
				pass
			if self.displayFaces:
				for face in wireframe.faces:
					n1, n2, n3 = face.vertices
					clipN1 = self.clipNode(wireframe.perspective_nodes[n1]) 
					clipN2 = self.clipNode(wireframe.perspective_nodes[n2])
					clipN3 = self.clipNode(wireframe.perspective_nodes[n3])

					if type(clipN1) == int or type(clipN2) == int or type(clipN3) == int:
						pass
					else:

						cull = self.backFaceCull(clipN1, clipN2, clipN3)
						if cull:
							pass
						else:
							pygame.draw.polygon(self.screen, [self.processLighting(face) * x for x in face.material], [clipN1[:2], clipN2[:2], clipN3[:2]], 0)
			else:
				pass

	def processLighting(self, face):

		directionVector = [None, None, None]

		for light in self.lights.values():
			directionVector[0] = ( light.position[0] - face.fNormal[0])  
			directionVector[1] = ( light.position[1] - face.fNormal[1])  
			directionVector[2] = ( light.position[2] - face.fNormal[2])

			olddirectionVectorX = directionVector[0]
			olddirectionVectorY = directionVector[1]
			olddirectionVectorZ = directionVector[2]

			directionVector[0] = directionVector[0] / math.sqrt((olddirectionVectorX**2) + (olddirectionVectorY**2) + (olddirectionVectorZ**2))
			directionVector[1] = directionVector[1] / math.sqrt((olddirectionVectorX**2) + (olddirectionVectorY**2) + (olddirectionVectorZ**2))
			directionVector[2] = directionVector[2] / math.sqrt((olddirectionVectorX**2) + (olddirectionVectorY**2) + (olddirectionVectorZ**2))

		cosTheta = self.clamp((directionVector[0]*face.fNormal[0]) + (directionVector[1]*face.fNormal[1]) + (directionVector[2]*face.fNormal[2]), 0, 1)

		return cosTheta
		
	def clamp(self, num, min_value, max_value):
		return max(min(num, max_value), min_value)

	def backFaceCull(self, n1, n2, n3):

		answer = ((n1[0] * n2[1]) + (n2[0]* n3[1]) + (n3[0] * n1[1])) - ((n3[0] * n2[1]) + (n2[0] * n1[1]) + (n1[0] * n3[1]))

		if answer > 0:
			return True
		else:
			return False

	def clipNode(self, node):

		x = self.width
		y = self.height
		z = 2000
		clippedNode = 0
		
		if node[0] > x or node[0] < 0:
			return 0

		if node[1] > y or node[0] < 0: 
			return 0

		if node[2] < z and node[2] > 0:
			clippedNode = node
		else:
			return 0

		return clippedNode

	def translateAll(self, vector):
		''' Translate all wireframes along a given axis by d units '''
		wf = Wireframe()
		matrix = wf.translationMatrix(*vector)
		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def scaleAll(self, vector):
		wf = Wireframe()
		matrix = wf.scaleMatrix(*vector)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def rotateAll(self, axis, theta):

		wf = Wireframe()
		if axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)
			#wireframe.transform_for_perspective()


	def rotate_about_Center(self, Axis, theta):

		#First translate Centre of screen to 0,0

		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		#Do Rotation
		wf = Wireframe()
		if Axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif Axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif Axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)
		

		#Translate back to centre of screen

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def rotate_about_camera(self, Axis, theta):

		wf = Wireframe()

		matrix = wf.translationMatrix(-self.width/2, -self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		#Do Rotation
		wf = Wireframe()
		if Axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif Axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif Axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)
		

		#Translate back to original position

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)


		self.camera.hor_angle += theta

		if self.camera.hor_angle >= 2*math.pi:
			self.camera.hor_angle -= 2*math.pi
		elif self.camera.hor_angle < -2*math.pi:
			self.camera.hor_angle += 2*math.pi

		self.camera.define_render_space()
		# print(self.camera.pos)
	

	def scale_centre(self, vector):

		#Transform center of screen to origin

		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		#Scale the origin by vector

		wf = Wireframe()
		matrix = wf.scaleMatrix(*vector)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def move_cam_forward(self, amount):
		#Moving the camera forward will be a positive translation in the z axis for every other object.
		self.camera.set_position(self.center_point)
		self.camera.define_render_space()
		self.translateAll([0,0,-amount])
		
	def move_cam_backward(self, amount):
		self.camera.set_position(self.center_point)
		self.camera.define_render_space()
		self.translateAll([0,0,amount])

	def move_cam_left(self, amount):
		self.camera.set_position(self.center_point)
		self.camera.define_render_space()
		self.translateAll([-amount,0,0])

	def move_cam_right(self, amount):
		self.camera.set_position(self.center_point)
		self.camera.define_render_space()
		self.translateAll([amount,0,0])

	def Toggle_Nodes(self):
		if self.displayNodes == True:
			self.displayNodes = False
		else:
			self.displayNodes = True


	def open_file(self):

		root = tk.Tk()
		root.withdraw()

		file_path = filedialog.askopenfilename()

		model= OBJ_loader(file_path, 50)

		model_wf = model.create_wireframe()

		self.addWireframe('model_'+str(len(self.wireframes)), model_wf)


		
					








