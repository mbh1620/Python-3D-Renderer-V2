from wireframe import *
import pygame
import numpy as np
from camera import *
import time
from Classes.Toolbar import Toolbar
from obj_loader import OBJ_loader
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Classes.Face import Face

class ProjectionViewer:

	''' Displays 3D Objects on a Pygame Screen '''

	def __init__(self, width, height, center_point):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('3D Renderer')
		self.background = (10,10,50)

		self.root = None
		self.root_flag = False

		#Setup camera
		self.camera = Camera([0,0,0],0,0)
		self.center_point = center_point

		self.wireframes = {}
		self.lights = {}

		self.displayNodes = True
		self.displayEdges = True
		self.displayFaces = True
		self.nodeColour = (255,255,255)
		self.edgeColour = (200,200,200)
		self.nodeRadius = 2

		self.toolbar = Toolbar(self.screen, self.width)

		self.first_click = None
		self.second_click = None

		pygame.init()

	def run(self):

		key_to_function = {
		pygame.K_LEFT: (lambda x: x.rotate_about_camera('Y', 0.05)),
 		pygame.K_RIGHT:(lambda x: x.rotate_about_camera('Y', -0.05)),
 		pygame.K_DOWN: (lambda x: x.move_cam_up(10)),
 		pygame.K_UP:   (lambda x: x.move_cam_down(10)),

 		pygame.K_w: (lambda x: x.move_cam_forward(20)),
 		pygame.K_s: (lambda x: x.move_cam_backward(20)),
 		pygame.K_a: (lambda x: x.move_cam_left(20)),
 		pygame.K_d: (lambda x: x.move_cam_right(20)),

		}

		# self.camera.set_position(self.center_point)

		running = True
		flag = False

		while running:

			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.toolbar.extrude_flag == True:
						start_position = pygame.mouse.get_pos()
						wireframe = self.wireframes['drawnRectangle5']
						
						while event.type != pygame.MOUSEBUTTONUP:
							
							end_position = pygame.mouse.get_pos()
							self.extrude_face(wireframe, start_position, end_position)
							for event in pygame.event.get():
								if event.type == pygame.MOUSEBUTTONUP:
									break
						
				
				elif event.type == pygame.MOUSEBUTTONUP:

					if self.toolbar.draw_rectangle_flag == True:

						if self.first_click == None:
							self.first_click = pygame.mouse.get_pos()
							self.click_function(self.first_click)
						else:
							self.second_click = pygame.mouse.get_pos()
							self.click_function(self.second_click)
							self.create_rectangle_wireframe(self.first_click,self.second_click)

							self.toolbar.draw_rectangle_flag = False
							self.first_click = None
							self.second_click = None

					else:
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

			self.flag_detection()
				
			pygame.display.flip()

	def addWireframe(self, name, wireframe):
		self.wireframes[name] = wireframe

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

			if self.displayNodes and wireframe.showNodes:
				for node in wireframe.perspective_nodes:
					if node[2] > 0 and node[2] < 10000 and node[0] > 0 and node[0] < 1199:
						pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
			else:
				pass
			if self.displayEdges and wireframe.showEdges:
				for n1, n2 in wireframe.edges:
					clipN1 = self.clipNode(wireframe.perspective_nodes[n1])
					clipN2 = self.clipNode(wireframe.perspective_nodes[n2])
					if type(clipN1) == int or type(clipN2) == int:
						pass
					else:
						pygame.draw.aaline(self.screen, self.edgeColour, clipN1[:2], clipN2[:2], 1)

			else:
				pass
			if self.displayFaces and wireframe.showFaces:
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
		buffer_factor = 200
		clippedNode = 0
		
		if node[0] > x+buffer_factor or node[0] < 0-buffer_factor:
			return 0

		if node[1] > y+buffer_factor or node[0] < 0-buffer_factor: 
			return 0

		if node[2] < z and node[2] > 0:
			clippedNode = node
		else:
			return 0

		return clippedNode

	def translateAll(self, vector):

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

	def rotate_about_Center(self, Axis, theta):

		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		wf = Wireframe()
		if Axis == 'X':
			matrix = wf.rotateXMatrix(theta)
		elif Axis == 'Y':
			matrix = wf.rotateYMatrix(theta)
		elif Axis == 'Z':
			matrix = wf.rotateZMatrix(theta)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

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
		
		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		self.camera.hor_angle += theta

		if self.camera.hor_angle >= 2*math.pi:
			self.camera.hor_angle -= 2*math.pi
		elif self.camera.hor_angle < -2*math.pi:
			self.camera.hor_angle += 2*math.pi

	def scale_centre(self, vector):

		wf = Wireframe()
		matrix = wf.translationMatrix(-self.width/2,-self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		wf = Wireframe()
		matrix = wf.scaleMatrix(*vector)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

		wf = Wireframe()
		matrix = wf.translationMatrix(self.width/2,self.height/2,0)

		for wireframe in self.wireframes.values():
			wireframe.transform(matrix)

	def move_cam_forward(self, amount):
		self.camera.set_position(self.center_point)
		self.translateAll([0,0,-amount])
		
	def move_cam_backward(self, amount):
		self.camera.set_position(self.center_point)
		self.translateAll([0,0,amount])

	def move_cam_left(self, amount):
		self.camera.set_position(self.center_point)
		self.translateAll([-amount,0,0])

	def move_cam_right(self, amount):
		self.camera.set_position(self.center_point)
		self.translateAll([amount,0,0])

	def move_cam_up(self, amount):
		self.camera.set_position(self.center_point)
		self.translateAll([0, amount, 0])

	def move_cam_down(self, amount):
		self.camera.set_position(self.center_point)
		self.translateAll([0, -amount, 0])


	def Toggle_Nodes(self):
		if self.displayNodes == True:
			self.displayNodes = False
		else:
			self.displayNodes = True


	def open_file(self, filename=None, showWireframeFaces=True, showWireframeEdges=False):

		if filename == None:
			self.root = tk.Tk()
		
			self.root.withdraw()

			file_path = filedialog.askopenfilename()

		else:
			file_path = filename

		model= OBJ_loader(file_path, 50)

		model_wf = model.create_wireframe()

		model_wf.showFaces = showWireframeFaces
		model_wf.showEdges = showWireframeEdges

		self.addWireframe(str(file_path.split("/")[-1])+str(len(self.wireframes)), model_wf)

	def view_model_window(self):

		self.root = tk.Tk()
		
		self.root.geometry('500x300')
		self.root.resizable(False, False)
		self.root.title('Current Models')

		self.root_flag = True

		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

		listbox = tk.Listbox(
			self.root,
			height=6,
			selectmode='extended')

		listbox.grid(
			column=0,
			row=0,
			sticky='nwes')

		num = 0 
		for i in self.wireframes.keys():
			listbox.insert(num, i)
			num += 1

		# self.toolbar.view_model_flag == False

		delete_button = ttk.Button(
			self.root,
			text="Delete",
			command=self.delete_model()
			)

		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		
		while self.root_flag == True:
			self.root.update()

		self.root.destroy()

	def delete_model(self):
		pass

	def on_closing(self):
	
		self.root_flag = False

	def create_rectangle_wireframe(self, first_click, second_click):

		rectangleWf = Wireframe()
		converted_first_click = self.convertNode(first_click)
		converted_second_click = self.convertNode(second_click)

		nodes = np.array([[converted_first_click[0], converted_first_click[1], converted_first_click[2]], [converted_first_click[0], converted_first_click[1], converted_second_click[2]], [converted_second_click[0], converted_second_click[1], converted_second_click[2]], [converted_second_click[0], converted_second_click[1], converted_first_click[2]]])
		rectangleWf.addNodes(nodes)

		fNormal = [0,1,0]

		rectangleWf.addEdges([(0,1),(1,2),(2,3),(3,0)])
		face1 = Face((2,1,0),fNormal, (122,122,122))
		face2 = Face((0,3,2),fNormal, material=(122,122,122))
		rectangleWf.addFaces([face1])
		rectangleWf.addFaces([face2])
		
		self.addWireframe('drawnRectangle'+str(len(self.wireframes.keys())), rectangleWf)

	def click_function(self, position):

		click_node = Wireframe()

		convertedNode = self.convertNode(position)
		
		node = np.array([[convertedNode[0], convertedNode[1], convertedNode[2]]])

		click_node.addNodes(node)

		click_node.showNodes = True

		self.addWireframe('clickNode'+str(len(self.wireframes.keys())), click_node)

	def flag_detection(self):
		if self.toolbar.open_flag == True:
			self.open_file()
			self.toolbar.open_flag = False
		if self.toolbar.view_model_flag:
			self.toolbar.view_model_flag = False
			self.view_model_window()

		if self.toolbar.grid_flag == True:
				
			if self.wireframes['grid'].showEdges == False:
				self.wireframes['grid'].showEdges = True
			else:
				self.wireframes['grid'].showEdges = False

			self.toolbar.grid_flag = False

		if self.toolbar.draw_rectangle_flag == True:
			pass


	def convertNode(self, node):

		x,y = node
		
		output_node = [None, None, None]

		delta = -self.camera.pos[1]

		z = ((delta*self.camera.fov)-((self.height/2)*self.camera.fov)-(self.camera.zoom*y)+((self.height/2)*self.camera.zoom))/(-y+(self.height/2))

		output_node[0] = (((x)*(self.camera.zoom-z) - ((self.width/2)*(self.camera.zoom-z)))/self.camera.fov)+(self.width/2)
		output_node[1] = 0+delta
		output_node[2] = z

		print(output_node)

		return output_node

	def checkWireframe(self, point):
		#return a wireframe which the point is in
		pass
		# for wireframe in self.wireframes.values:

		# 	if point()



		# return wireframe


	def extrude_face(self, wireframe, start_position, end_position):

		print(start_position, end_position)

		#We need to raise the face and then add faces on all the sides

		start_x, start_y = start_position
		end_x, end_y = end_position 

		delta = end_y - start_y

		delta = delta/10000

		wf = Wireframe()

		matrix = wf.translationMatrix(0, -delta, 0)


		if len(wireframe.nodes) < 8:
			face_node_array = np.array([wireframe.nodes[0][0:-1], wireframe.nodes[1][0:-1], wireframe.nodes[2][0:-1], wireframe.nodes[3][0:-1]])
			print(face_node_array)
			wireframe.transform(matrix)

			wireframe.addNodes(face_node_array)
			print(face_node_array)

			face1 = Face((int(5), int(4), int(1)), [0,0,1], (211,211,211))
			face2 = Face((int(1), int(4), int(0)), [0,0,1], (211,211,211))
			
			face3 = Face((int(0), int(7), int(3)), [-1,0,0], (211,211,211))
			face4 = Face((int(4), int(7), int(0)), [-1,0,0], (211,211,211))
			
			face5 = Face((int(3), int(7), int(6)), [0,1,0], (211,211,211))
			face6 = Face((int(2), int(3), int(6)), [0,1,0], (211,211,211))

			face7 = Face((int(6), int(5), int(2)), [0,1,0], (211,211,211))
			face8 = Face((int(2), int(5), int(1)), [0,1,0], (211,211,211))

			wireframe.addFaces([face1, face2, face3, face4, face5, face6, face7, face8])

		else:
			wireframe.nodes[0][1] += -delta
			wireframe.nodes[1][1] += -delta
			wireframe.nodes[2][1] += -delta
			wireframe.nodes[3][1] += -delta

		print("node count" + str(len(wireframe.nodes)))

		#find which wireframe has been clicked from start point





		


		





		
					








