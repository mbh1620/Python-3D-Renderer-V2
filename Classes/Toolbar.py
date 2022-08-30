import pygame


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
		self.grid_flag = False
		self.extrude_flag = False

	def render(self):
		pygame.draw.rect(self.screen, (161, 161, 161), pygame.Rect(0,0,self.width, 30))

		font = pygame.font.Font('freesansbold.ttf', 20)
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

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Open File', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (60, 50)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Add Light', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (60, 75)
		self.screen.blit(text, textRect)

	def edit(self):
		pygame.draw.rect(self.screen, (161, 161, 161), pygame.Rect(60,30,200, 250))

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Hello', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (100, 50)
		self.screen.blit(text, textRect)

	def view(self):
		pygame.draw.rect(self.screen, (161, 161, 161), pygame.Rect(120,30,200, 250))

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'View Models', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 50)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Floor Grid √', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 70)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Measure Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 90)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Draw Rectangle Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 110)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Draw Polygon Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 130)
		self.screen.blit(text, textRect)

		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f'Extrude Tool', True, (255,255,255),(161, 161, 161))
		textRect = text.get_rect()
		textRect.center = (200, 150)
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
			elif 120 < x and x < 350 and 140 < y and y < 160:
				self.toggle_extrude_tool()

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

		font = pygame.font.Font('freesansbold.ttf', 20)
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

	def toggle_grid(self):

		self.grid_flag = True

	def toggle_measure_tool(self):

		self.measure_tool_flag = True

	def toggle_rectangle_tool(self):
		self.draw_rectangle_flag = True
		#Tool for drawing a rectangle

	def toggle_extrude_tool(self):
		self.extrude_flag = True

		

