import pygame


class Toolbar:

	def __init__(self, screen, width):
		self.screen = screen
		self.width = width

		self.file_flag = False
		self.edit_flag = False
		self.view_flag = False

		self.open_flag = False

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


	def open(self):

		self.open_flag = True
		self.file_flag = False

		

