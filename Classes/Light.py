class Light

	def __init__(self, position, intensity, direction, color=(0,0,0)):

		self.position = position
		self.intensity = intensity
		self.direction = direction
		self.color = color

	def calculateShading(face):
		#Function used to calculate shading brightness between a light and a face

		#Calculate Face Normal, then use geometry to work out the light level of the face

		#Brightness decreases using an inverse square of the distance

		# B ∝ 1/D²

		# Brightness also decreases on a face depending on the angle of incidence so the larger the angle, the less bright the face will appear,

		# https://www.tomdalling.com/blog/modern-opengl/06-diffuse-point-lighting/

		







	