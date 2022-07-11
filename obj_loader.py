#OBJ file loader class
import wireframe
import numpy as np

class OBJ_loader:

	def __init__(self, filename, scaleFactor):
		self.filename = filename
		self.scaleFactor = scaleFactor

		self.objectArray = []
		self.nodeArray = []
		self.faceArray = []
		self.edgeArray = []

		self.process_file()

	def process_file(self):

		f = open(self.filename, "r")

		for i in f:

			if i[0] == 'v' and i[1] == 't':
				pass

			elif i[0] == 'v' and i[1] == 'n':
				pass

			elif i[0] == 'v' and i[1] == ' ':
				i = i.split()
				self.nodeArray.append([(float(i[1])*self.scaleFactor), (float(i[2])*self.scaleFactor), float(i[3])*self.scaleFactor])

			elif i[0] == 'f':

				i = i.split()
				face = []
				for subsection in i:
					subsections = subsection.split('/')
					if subsections[0] != 'f':
						face.append(subsections[0])
				if len(face) == 4:
						#Create two triangles
					triangle1 = (int(face[0])-1, int(face[1])-1, int(face[2])-1, (255, 0, 0))
					triangle2 = (int(face[2])-1, int(face[3])-1, int(face[0])-1, (225, 0, 0))

					self.faceArray.append(triangle1)
					self.faceArray.append(triangle2)
				elif len(face) == 3:
						#Create one triangle
					triangle1 = (int(face[0])-1, int(face[1])-1, int(face[2])-1, (255,0,0))
					self.faceArray.append(triangle1)

				else:
					print('length of face not valid')
			else:
				pass

		f.close()

	def process_material(self):
		pass

	def create_wireframe(self):

		Object = wireframe.Wireframe()

		Object.addNodes(np.array(self.nodeArray))
		
		for i in self.faceArray:
			Object.addFaces([i])

		return Object
