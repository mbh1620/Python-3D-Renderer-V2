class Face:

	def __init__(self, vertices, fNormal, material):

		self.vertices = vertices
		self.fNormal = fNormal
		self.material = material

	def calculateFaceNormal(self):
		pass

	def calculateShading(self):
		pass
