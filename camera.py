import math
'''
Camera class

position
FOV
zoom 

'''
class Camera:

	def __init__(self, pos, hor_angle, ver_angle, fov=250, zoom=500):
		self.pos = pos
		self.fov = fov
		self.hor_angle = hor_angle
		self.ver_angle = ver_angle
		self.zoom = self.pos[2]
		self.back_straight_x = 0
		self.back_straight_z = 0

	def set_position(self, center_point):

		self.pos[0] = -center_point.nodes[0][0]
		self.pos[1] = -center_point.nodes[0][1]
		self.pos[2] = -center_point.nodes[0][2]
