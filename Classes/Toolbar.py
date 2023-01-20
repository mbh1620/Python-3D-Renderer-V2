import pygame
import os, sys


class Toolbar:

	def __init__(self, screen, width):
		self.screen = screen
		self.width = width

		self.file_flag = False
		self.edit_flag = False
		self.view_flag = False

		self.open_flag = False
		self.view_model_flag = False
		self.measure_tool_flag = False
		self.draw_rectangle_flag = False
		self.draw_circle_flag = False
		self.draw_polygon_flag = False
		self.change_colour_flag = False
		self.shading_flag = True
		self.faces_flag = True
		self.edges_flag = True
		self.nodes_flag = True
		self.render_flag = False

		self.grid_flag = True
		self.extrude_flag = False

		if getattr(sys, 'frozen', False):
			self.application_path = sys._MEIPASS
		else:
			self.application_path = os.path.dirname(os.path.abspath(__file__))

	def render(self):
		pygame.draw.rect(self.screen, (161, 161, 161), pygame.Rect(0,0,self.width, 30))

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'File    Edit    View', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (100, 15)
		self.screen.blit(text, textRect)

		if self.file_flag:
			self.file()
		if self.edit_flag:
			self.edit()
		if self.view_flag:
			self.view()

		self.selector()

	def file(self):
		pygame.draw.rect(self.screen, (161, 161, 161), pygame.Rect(0,30,200, 250))

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Open File', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (60, 50)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Add Light', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (60, 75)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Render to Image', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (90, 100)
		self.screen.blit(text, textRect)

	def edit(self):
		pygame.draw.rect(self.screen, (161, 161, 161), pygame.Rect(60,30,200, 250))

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Hello', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (100, 50)
		self.screen.blit(text, textRect)

	def view(self):
		pygame.draw.rect(self.screen, (161, 161, 161), pygame.Rect(120,30,200, 250))

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'View Models', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 50)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Floor Grid √', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 70)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Measure Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 90)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Draw Rectangle Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 110)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Draw Polygon Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 130)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Draw Circle Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 150)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Extrude Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 170)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Copy Mesh Object', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 190)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Translate Object', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 210)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Change Object Colour', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 230)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Toggle Shading', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 250)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Toggle Faces', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 280)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Toggle Edges', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 310)
		self.screen.blit(text, textRect)

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'Toggle Nodes', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 340)
		self.screen.blit(text, textRect)

	def process_click(self, cursor_position):
		x, y = cursor_position
		# print(x, y)
		#File
		if 0 < x and x < 60 and 0 < y and y < 30:
			if self.file_flag == False:
				self.file_flag = True
				self.edit_flag = False
				self.view_flag = False
			else:
				self.file_flag = False

		elif 60 < x and x < 120 and 0 < y and y < 30:
			if self.edit_flag == False:
				self.edit_flag = True
				self.file_flag = False
				self.view_flag = False
			else:
				self.edit_flag = False

		elif 120 < x and x < 180 and 0 < y and y < 30:
			if self.view_flag == False:
				self.edit_flag = False
				self.file_flag = False
				self.view_flag = True
			else:
				self.view_flag = False

		if self.file_flag:
			if 0 < x and x < 120 and 30 < y and y < 70:
				self.open()
			if 0 < x and x < 120 and 70 < y and y < 110:
				self.renderToImage()

		if self.edit_flag:
			if 0 < x and x < 120 and 30 < y and y < 70:
				pass

		if self.view_flag:
			
			if 120 < x and x < 350 and 30 < y and y < 60:
				self.view_model()
			elif 120 < x and x < 350 and 60 < y and y < 80:
				self.toggle_grid()
			elif 120 < x and x < 350 and 80 < y and y < 100:
				self.toggle_measure_tool()
			elif 120 < x and x < 350 and 100 < y and y < 120:
				self.toggle_rectangle_tool()
			elif 120 < x and x < 350 and 120 < y and y < 140:
				self.toggle_polygon_tool()
			elif 120 < x and x < 350 and 140 < y and y < 160:
				self.toggle_circle_tool()
			elif 120 < x and x < 350 and 160 < y and y < 180:
				self.toggle_extrude_tool()
			elif 120 < x and x < 350 and 180 < y and y < 240:
				self.toggle_change_colour()
			elif 120 < x and x < 350 and 240 < y and y < 260:
				self.toggle_shading()
			elif 120 < x and x < 350 and 270 < y and y < 290:
				self.toggle_faces()
			elif 120 < x and x < 350 and 300 < y and y < 320:
				self.toggle_edges()
			elif 120 < x and x < 350 and 330 < y and y < 360:
				self.toggle_nodes()


	def selector(self):

		selector_distance = -10

		if self.view_model_flag:
			selector_distance = 50
		elif self.grid_flag:
			selector_distance = 70
		elif self.draw_rectangle_flag == True:
			selector_distance = 110
		elif self.extrude_flag == True:
			selector_distance = 150

		font = pygame.font.Font(self.application_path + '/Fonts/freesansbold.ttf', 20)
		text = font.render(f'√', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (310, selector_distance)
		self.screen.blit(text, textRect)
				

	def view_model(self):
		self.view_model_flag = True
		self.view_flag = False

	def open(self):

		self.open_flag = True
		self.file_flag = False

	def renderToImage(self):
		self.render_flag = True
		self.file_flag = False

	def toggle_grid(self):

		self.grid_flag = True

	def toggle_measure_tool(self):

		self.measure_tool_flag = True

	def toggle_rectangle_tool(self):
		self.draw_rectangle_flag = True
		#Tool for drawing a rectangle

	def toggle_circle_tool(self):
		self.draw_circle_flag = True

	def toggle_polygon_tool(self):
		self.draw_polygon_flag = True

	def toggle_extrude_tool(self):
		if self.extrude_flag:
			self.extrude_flag = False
		else: 
			self.extrude_flag = True

	def toggle_change_colour(self):
		self.change_colour_flag = True

	def toggle_shading(self):
		if self.shading_flag:
			self.shading_flag = False
		else:
			self.shading_flag = True

	def toggle_faces(self):

		print("Toggle Faces")

		if self.faces_flag:
			self.faces_flag = False
		else:
			self.faces_flag = True

	def toggle_edges(self):

		if self.edges_flag:
			self.edges_flag = False
		else:
			self.edges_flag = True

	def toggle_nodes(self):

		print("Toggle Nodes")

		if self.nodes_flag:
			self.nodes_flag = False
		else:
			self.nodes_flag = True


		

