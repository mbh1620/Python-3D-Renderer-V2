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
from tkinter.colorchooser import askcolor
from Functions.pointInTriangle import pointInTriangle
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
		self.displayFaces = False
		self.nodeColour = (255,255,255)
		self.edgeColour = (200,200,200)
		self.nodeRadius = 3

		self.toolbar = Toolbar(self.screen, self.width)

		self.first_click = None
		self.second_click = None
		self.converted_clicks = []

		self.render_flag = False

		self.shading = True

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

		running = True
		flag = False

		while running:

			if self.render_flag == True:
				self.connected_node_click_function(self.first_click, pygame.mouse.get_pos())

			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				elif event.type == pygame.MOUSEBUTTONDOWN:

					if self.toolbar.extrude_flag == True:
						start_position = pygame.mouse.get_pos()

						x, y = start_position

						if 120 < x and x < 350 and 140 < y and y < 160:
							# self.toolbar.extrude_flag = False
							# break
							pass
						else:

							wireframe = self.selectFace(start_position)

							if wireframe == None:
								pass

							else:
							
								while event.type != pygame.MOUSEBUTTONUP:
									
									end_position = pygame.mouse.get_pos()

									self.extrude_face(wireframe, start_position, end_position)

									for event in pygame.event.get():
										if event.type == pygame.MOUSEBUTTONUP:
											break

					if self.toolbar.change_colour_flag == True:

						start_position = pygame.mouse.get_pos()

						wireframe = self.selectFace(start_position)

						self.change_wireframe_colour(wireframe)

						self.toolbar.change_colour_flag = False
				
				elif event.type == pygame.MOUSEBUTTONUP:

					if self.toolbar.measure_tool_flag == True:
						print("first measure click")

						if self.first_click == None:
							self.first_click = pygame.mouse.get_pos()
							self.click_function(self.first_click)
							self.render_flag = True
						else:
							self.render_flag = False
							self.second_click = pygame.mouse.get_pos()
							self.connected_node_click_function(self.first_click, self.second_click)
							self.first_click = None
							self.second_click = None

					
					if self.toolbar.draw_rectangle_flag == True:
						self.toolbar.view_flag = False

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
							

					if self.toolbar.draw_circle_flag == True:
						self.toolbar.view_flag = False

						if self.first_click == None:
							self.first_click = pygame.mouse.get_pos()
							self.click_function(self.first_click)
						else:
							self.second_click = pygame.mouse.get_pos()
							self.click_function(self.second_click)
							self.create_circle_wireframe(self.first_click, self.second_click)

							self.first_click = None
							self.second_click = None

							self.toolbar.draw_circle_flag = False

					if self.toolbar.draw_polygon_flag:
						self.polygon_clicker(pygame.mouse.get_pos())
					
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

							if self.toolbar.shading_flag == True:
								colour = [self.processLighting(face) * x for x in face.material]
							else:
								colour = [x for x in face.material]
							
							if math.isnan(colour[0]):
								colour = [70,70,70]

							# self.rasterTriangle(clipN1[:2], clipN2[:2], clipN3[:2], colour)	
							pygame.draw.polygon(self.screen, colour, [clipN1[:2], clipN2[:2], clipN3[:2]], 0)
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


	def open_file(self, filename=None, showWireframeFaces=True, showWireframeEdges=True, showWireframeNodes=True):

		if filename == None:
			self.root = tk.Tk()
		
			self.root.withdraw()

			file_path = filedialog.askopenfilename()

		else:
			file_path = filename

		model= OBJ_loader(file_path, 100)

		model_wf = model.create_wireframe()

		model_wf.showFaces = showWireframeFaces
		model_wf.showEdges = showWireframeEdges
		model_wf.showNodes = showWireframeNodes

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

	def polygon_clicker(self, click):

		node = self.convertNode(click)

		if len(self.converted_clicks) == 0:
			self.converted_clicks.append(node)
			self.click_function(click)
			return 0

		if abs(node[0] - self.converted_clicks[0][0]) > 20 or abs(node[2] - self.converted_clicks[0][2]) > 20:
			self.converted_clicks.append(node)
			self.click_function(click)
		else:
	
			self.toolbar.draw_polygon_flag = False
			self.create_polygon_wireframe(self.converted_clicks)
			self.converted_clicks = []

		return 0

	def create_polygon_wireframe(self, clicks):

		polygonWf = Wireframe()

		polygonWf.addNodes(np.array(clicks))

		edge_list = []
		polygon_face_list = []

		for i in range(0,len(clicks)-1):
			edge_list.append((i, i+1))

		fNormal = [0,1,0]

		num_of_triangles = len(clicks)-2

		for i in range(0, num_of_triangles):
			polygon_face_list.append(Face((i+2, i+1, 0), fNormal, (122,122,122)))

		polygon_face_list.append

		edge_list.append((len(clicks)-1, 0))

		polygonWf.addEdges(edge_list)
		polygonWf.addFaces(polygon_face_list)

		polygonWf.showNodes = True
		polygonWf.showEdges = True

		self.addWireframe('polygon'+str(len(self.wireframes.keys())), polygonWf)

	def create_circle_wireframe(self, center_point, radius_point):

		world_center_point = self.convertNode(center_point)
		world_radius_point = self.convertNode(radius_point)

		radius = math.sqrt(((world_radius_point[0]-world_center_point[0])**2)+(world_radius_point[2]-world_center_point[2])**2)

		number_of_points_at_edge=30

		degree_intervals = 360/number_of_points_at_edge

		theta = 0 

		circle_points = []
		circle_edges = []
		circle_faces = []
		fNormals = []
		fNormal = [0,1,-1]

		circle_points.append(world_center_point)

		for i in range(0,number_of_points_at_edge):

			x = world_center_point[0] + (radius * math.cos((theta/360)*2*math.pi))
			y = 0
			z = world_center_point[2] + (radius * math.sin((theta/360)*2*math.pi))
			theta += degree_intervals

			if i <= number_of_points_at_edge:
				if i == 0:
					pass
				else:
					circle_edges.append((i, i+1))
					circle_faces.append(Face((i+1, i, 0), fNormal, (122,122,122)))

			circle_points.append([x, y, z])

		circle_edges.append((number_of_points_at_edge-1, 1))
		circle_faces.append(Face((1, number_of_points_at_edge-1, 0), fNormal, (122,122,122)))

		for i in circle_faces:
		
			p1, p2, p3 = i.vertices
			facePoints = circle_points[p1], circle_points[p2], circle_points[p3]
			i.fNormal = self.generate_face_normal(facePoints)

		circle_wireframe = Wireframe()

		circle_wireframe.type = "Circle"

		circle_wireframe.addNodes(np.array(circle_points))
		circle_wireframe.addEdges(circle_edges)
		circle_wireframe.addFaces(circle_faces)

		circle_wireframe.showFaces = True

		self.addWireframe('circle_wireframe' + str(len(self.wireframes.values())), circle_wireframe)

	def click_function(self, position):

		click_node = Wireframe()

		convertedNode = self.convertNode(position)
		
		node = np.array([[convertedNode[0], convertedNode[1], convertedNode[2]]])

		click_node.addNodes(node)

		click_node.showNodes = True

		self.addWireframe('clickNode'+str(len(self.wireframes.keys())), click_node)

	def connected_node_click_function(self, position1, position2):

		connected_nodes = Wireframe()

		convertedNode1 = self.convertNode(position1)
		node1 = np.array([[convertedNode1[0], convertedNode1[1], convertedNode1[2]]])
		connected_nodes.addNodes(node1)

		convertedNode2 = self.convertNode(position2)
		node2 = np.array([[convertedNode2[0], convertedNode2[1], convertedNode2[2]]])
		connected_nodes.addNodes(node2)

		connected_nodes.addEdges([(0,1)])

		connected_nodes.showNodes = True
		connected_nodes.showEdges = True

		self.addWireframe('measureToolWireframe',connected_nodes)



	def flag_detection(self):
		if self.toolbar.open_flag == True:
			self.open_file()
			self.toolbar.open_flag = False
		if self.toolbar.view_model_flag:
			self.toolbar.view_model_flag = False
			self.view_model_window()

		if self.toolbar.faces_flag == True:
			self.displayFaces = True
		elif self.toolbar.faces_flag == False:
			self.displayFaces = False

		if self.toolbar.edges_flag == True:
			self.displayEdges = True
		elif self.toolbar.edges_flag == False:
			self.displayEdges = False

		if self.toolbar.nodes_flag == True:
			self.displayNodes = True
		elif self.toolbar.nodes_flag == False:
			self.displayNodes = False

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

		return output_node

	def selectFace(self, clickPoint):

		for wireframe in self.wireframes.values():
			if wireframe == self.wireframes['grid']:
				pass
			else:
				if self.displayFaces and wireframe.showFaces:
					for face in wireframe.faces:
						n1, n2, n3 = face.vertices
				
						n1_ = wireframe.perspective_nodes[n1-2]
						n2_ = wireframe.perspective_nodes[n2-2]
						n3_ = wireframe.perspective_nodes[n3-2]

						inTriangle = pointInTriangle(clickPoint, n1_, n2_, n3_)

						if inTriangle == True:
							return wireframe


	def extrude_face(self, wireframe, start_position, end_position):	

		start_x, start_y = start_position
		end_x, end_y = end_position 

		delta = end_y - start_y

		delta = delta/10000

		wf = Wireframe()

		matrix = wf.translationMatrix(0, -delta, 0)

		if len(wireframe.nodes) == 4:
			face_node_array = np.array([wireframe.nodes[0][0:-1], wireframe.nodes[1][0:-1], wireframe.nodes[2][0:-1], wireframe.nodes[3][0:-1]])
			
			print(face_node_array)

			wireframe.transform(matrix)

			wireframe.addNodes(face_node_array)

			print("wireframe nodes")
			print(wireframe.nodes[5])

			facePoints = wireframe.nodes[5], wireframe.nodes[4], wireframe.nodes[1]
			face1 = Face((int(5), int(4), int(1)), self.generate_face_normal(facePoints), (211,211,211))
			facePoints = wireframe.nodes[1], wireframe.nodes[4], wireframe.nodes[0]
			face2 = Face((int(1), int(4), int(0)), self.generate_face_normal(facePoints), (211,211,211))

			facePoints = wireframe.nodes[0], wireframe.nodes[7], wireframe.nodes[3]
			face3 = Face((int(0), int(7), int(3)), self.generate_face_normal(facePoints), (211,211,211))
			facePoints = wireframe.nodes[4], wireframe.nodes[7], wireframe.nodes[0]
			face4 = Face((int(4), int(7), int(0)), self.generate_face_normal(facePoints), (211,211,211))

			facePoints = wireframe.nodes[3], wireframe.nodes[7], wireframe.nodes[6]
			face5 = Face((int(3), int(7), int(6)), self.generate_face_normal(facePoints), (211,211,211))
			facePoints = wireframe.nodes[2], wireframe.nodes[3], wireframe.nodes[6]
			face6 = Face((int(2), int(3), int(6)), self.generate_face_normal(facePoints), (211,211,211))

			facePoints = wireframe.nodes[6], wireframe.nodes[5], wireframe.nodes[2]
			face7 = Face((int(6), int(5), int(2)), self.generate_face_normal(facePoints), (211,211,211))
			facePoints = wireframe.nodes[2], wireframe.nodes[5], wireframe.nodes[1]
			face8 = Face((int(2), int(5), int(1)), self.generate_face_normal(facePoints), (211,211,211))

			wireframe.addFaces([face1, face2, face3, face4, face5, face6, face7, face8])

		if wireframe.type == "Circle":

			node_len = 30

			face_node_array = []

			for node in wireframe.nodes:
				face_node_array.append(node[:-1])

			wireframe.showNodes = True

			wireframe.type = "Cylinder"

			wireframe.addNodes(np.array(face_node_array))

			edge_list = []

			face_list = []

			for i in range(2,int(len(wireframe.nodes)/2)):
			
				if i == 1:
					pass
				else:
					edge_list.append((i,i+31))
					edge_list.append((i,i+30))
					edge_list.append((i+30, i+31))

			for i in range(1, int(len(wireframe.nodes)/2)):

				face_list.append(Face((i+31, i+1,i), [0,1,0], (211,211,211)))
				face_list.append(Face((i, i+30, i+31), [0,1,0], (211,211,211)))

			face_list.append(Face((1, 30, 61), [0,1,0], (211,211,211)))
			face_list.append(Face((32, 1, 61), [0,1,0], (211,211,211)))

			for i in range(31, len(wireframe.nodes)-2):

				face_list.append(Face((i+2, i+1,31), [0,1,0], (211,211,211)))

			face_list.append(Face((32, 61,31), [0,1,0], (211,211,211)))

			edge_list.append((61,32))

			wireframe.addEdges(edge_list)

			wireframe.addFaces(face_list)

			wireframe.showEdges = False
			wireframe.showNodes = False

		if wireframe.type == "Cylinder" and len(wireframe.nodes) >= 30:
			for node in wireframe.nodes[-31:]:
				node[1] += -delta*100

			for i in wireframe.faces:

				p1, p2, p3 = i.vertices
						
				facePoints = wireframe.nodes[p1], wireframe.nodes[p2], wireframe.nodes[p3]

				i.fNormal = self.generate_face_normal(facePoints)

		else:
			wireframe.nodes[0][1] += -delta
			wireframe.nodes[1][1] += -delta
			wireframe.nodes[2][1] += -delta
			wireframe.nodes[3][1] += -delta

			for i in wireframe.faces:

				p1, p2, p3 = i.vertices
						
				facePoints = wireframe.nodes[p1], wireframe.nodes[p2], wireframe.nodes[p3]

				i.fNormal = self.generate_face_normal(facePoints)



	def change_wireframe_colour(self,wireframe):

		colour = askcolor(title="Choose Colour for Object")

		rgb, hex_Val = colour

		print(colour)

		for face in wireframe.faces:
			face.material = rgb

	def generate_face_normal(self, face):

		faceNormal = [None, None, None]

		vectorU = self.minus(face[1], face[0])
		vectorV = self.minus(face[2], face[0])

		faceNormal[0] = (vectorU[1]*vectorV[2])-(vectorU[2]*vectorV[1])	
		faceNormal[1] = (vectorU[2]*vectorV[0])-(vectorU[0]*vectorV[2])
		faceNormal[2] = (vectorU[0]*vectorV[1])-(vectorU[1]*vectorV[0])
		
		#Now need to normalize the vector

		vectorNormalX = faceNormal[0]
		vectorNormalY = faceNormal[1]
		vectorNormalZ = faceNormal[2]

		bottom = math.sqrt((vectorNormalX**2) + (vectorNormalY**2) + (vectorNormalZ**2))

		faceNormal[0] = faceNormal[0] / bottom
		faceNormal[1] = faceNormal[1] / bottom
		faceNormal[2] = faceNormal[2] / bottom

		return faceNormal

	def minus(self, a, b):

		vector = [None, None, None]
		
		vector[0] = a[0] - b[0]
		vector[1] = a[1] - b[1]
		vector[2] = a[2] - b[2]

		#normaliseVector here! 

		vectorX = vector[0]
		vectorY = vector[1]
		vectorZ = vector[2]

		bottom = math.sqrt((vectorX**2) + (vectorY**2) + (vectorZ**2))

		# if bottom != 0:
		# 	vector[0] = vector[0] / bottom
		# 	vector[1] = vector[1] / bottom
		# 	vector[2] = vector[2] / bottom

		return vector

	def rasterTriangle(self, p1, p2, p3, colour):

		p1x, p1y = p1
		p2x, p2y = p2
		p3x, p3y = p3

		x_coordinates = [p1x,p2x,p3x]
		y_coordinates = [p1y,p2y,p3y]

		boundary_x = [min(x_coordinates), max(x_coordinates)]
		boundary_y = [min(y_coordinates), max(y_coordinates)]

		for x in np.arange(boundary_x[0], boundary_x[1]+1, 1):
			for y in np.arange(boundary_y[0], boundary_y[1]+1, 1):
				
				point = [x, y]
				n1 = [p1x, p1y]
				n2 = [p2x, p2y]
				n3 = [p3x, p3y]

				if pointInTriangle(point, n1, n2, n3) == True:

					pygame.draw.circle(self.screen, colour, (int(x), int(y)), 0, 0)










		


		





		
					








