#OBJ file loader class
import wireframe
import numpy as np
from Classes.Face import Face
import math


class OBJ_loader:

	def __init__(self, filename, scaleFactor, offset=[0,0,0]):
		self.x_offset = offset[0]
		self.y_offset = offset[1]
		self.z_offset = offset[2]

		self.filename = filename
		self.scaleFactor = scaleFactor

		self.objectArray = []
		self.nodeArray = []
		self.faceArray = []
		self.edgeArray = []
		self.vertexNormalArray = []
		self.materialDictionary = {}

		mtlFile = self.process_material_file()
		self.process_file(mtlFile)

	def process_file(self, mtlFile):

		#Work out the File type

		filetype = self.filename.split('.')[-1]

		print(filetype)

		if filetype == "tri":

			self.process_proprietary_file()

		else:


			f = open(self.filename, "r")

			if len(self.materialDictionary.keys()) == 0:
				self.materialDictionary['default'] = (255,255,255)

			material = ''

			for i in f:

				if i[0] == 'v' and i[1] == 't':
					pass

				elif i[0] == 'v' and i[1] == 'n':
					i = i.split()
					self.vertexNormalArray.append([(float(i[1])*self.scaleFactor), (float(i[2])*self.scaleFactor), (float(i[3])*self.scaleFactor)])

				elif i[0] == 'v' and i[1] == ' ':
					i = i.split()
					self.nodeArray.append([(float(i[1])*self.scaleFactor), (float(i[2])*self.scaleFactor), (float(i[3])*self.scaleFactor)])

				elif i.find('usemtl') != -1:
					if mtlFile == False:
						material = 'default'
					else:
						i = i.split(' ')
						material = i[1]

				elif i[0] == 'f':

					i = i.split()
					face = []
					faceVertexNormals = []
					for subsection in i:
						subsections = subsection.split('/')
						if subsections[0] != 'f':
							face.append(subsections[0])
							faceVertexNormals.append(subsections[2])
					if len(face) == 4:
							#Create two triangles
						triangle1 = Face((int(face[0])-1, int(face[1])-1, int(face[2])-1), self.getFaceNormal(self.vertexNormalArray[int(faceVertexNormals[0])-1], self.vertexNormalArray[int(faceVertexNormals[1])-1], self.vertexNormalArray[int(faceVertexNormals[2])-1]), self.materialDictionary[material])
						triangle2 = Face((int(face[2])-1, int(face[3])-1, int(face[0])-1), self.getFaceNormal(self.vertexNormalArray[int(faceVertexNormals[2])-1], self.vertexNormalArray[int(faceVertexNormals[3])-1], self.vertexNormalArray[int(faceVertexNormals[0])-1]), self.materialDictionary[material])

						self.edgeArray.append((int(face[0])-1, int(face[1])-1))
						self.edgeArray.append((int(face[1])-1, int(face[2])-1))
						self.edgeArray.append((int(face[2])-1, int(face[0])-1))
						self.edgeArray.append((int(face[2])-1, int(face[3])-1))
						self.edgeArray.append((int(face[3])-1, int(face[0])-1))
						self.edgeArray.append((int(face[0])-1, int(face[2])-1))

						self.faceArray.append(triangle1)
						self.faceArray.append(triangle2)
					elif len(face) == 3:
							#Create one triangle
						triangle1 = Face((int(face[0])-1, int(face[1])-1, int(face[2])-1), self.getFaceNormal(self.vertexNormalArray[int(faceVertexNormals[0])-1], self.vertexNormalArray[int(faceVertexNormals[1])-1], self.vertexNormalArray[int(faceVertexNormals[2])-1]), self.materialDictionary[material])
						self.edgeArray.append((int(face[0])-1, int(face[1])-1))
						self.edgeArray.append((int(face[1])-1, int(face[2])-1))
						self.edgeArray.append((int(face[2])-1, int(face[0])-1))
						self.faceArray.append(triangle1)

					else:
						pass

				elif i[0] == 'm':
					#use material to add the colour to the face
					pass

				elif i[0] == 'l':

					i = i.split()
					self.edgeArray.append((int(i[1])-1, int(i[2])-1))

				else:
					pass

			f.close()

	def getFaceNormal(self, vertexNormalA, vertexNormalB, vertexNormalC):

		averagedVertexNormal = [None, None, None]

		averagedVertexNormal[0] = (vertexNormalA[0] + vertexNormalB[0] + vertexNormalC[0])/3.0
		averagedVertexNormal[1] = (vertexNormalA[1] + vertexNormalB[1] + vertexNormalC[1])/3.0
		averagedVertexNormal[2] = (vertexNormalA[2] + vertexNormalB[2] + vertexNormalC[2])/3.0

		vectorNormalX = averagedVertexNormal[0]
		vectorNormalY = averagedVertexNormal[1]
		vectorNormalZ = averagedVertexNormal[2]

		bottom = math.sqrt((vectorNormalX**2) + (vectorNormalY**2) + (vectorNormalZ**2))

		if bottom == 0:
			bottom = 0.1

		averagedVertexNormal[0] = averagedVertexNormal[0] / bottom
		averagedVertexNormal[1] = averagedVertexNormal[1] / bottom
		averagedVertexNormal[2] = averagedVertexNormal[2] / bottom

		return averagedVertexNormal

	def process_material_file(self):
		#open the same filename with the .mtl file extension
		filename = self.filename.rsplit(".", 1)
		filename = filename[0] + ".mtl"

		materialName = ''

		skipFlag = False
		mtlFile = True

		try:
			f = open(filename, 'r')

		except:
			print("No Mtl file!")
			skipFlag = True
			mtlFile = False
		
		if skipFlag == False:

			for i in f:
				if i.find('newmtl') == 0:
					i = i.split(' ')
					materialName = i[-1]
					print(materialName)

				if i[0] == 'K' and i[1] == 'd':
					i = i.split(' ')
					r = float(i[1])*255
					g = float(i[2])*255
					b = float(i[3])*255

					self.materialDictionary[materialName] = (r,g,b)

		return mtlFile

	def process_proprietary_file(self):

		f = open(self.filename, "r")

		f.seek(2)

		header = f.readline()

		numberOfVertices = header.split()[0]

		print("start reading tri file here")

		print(numberOfVertices)

		for i in range(0,int(numberOfVertices)):

			line = f.readline()

			line = line.split()

			self.nodeArray.append([(float(line[1])*self.scaleFactor), (float(line[2])*self.scaleFactor), (float(line[3])*self.scaleFactor)])

		#For now generate the nodes to see what they look like

		numberOfTriangles = f.readline()
		
		print(numberOfTriangles.split)

		for i in range(0, int(numberOfTriangles.split()[0])):

			line = f.readline()

			line = line.split()

			self.edgeArray.append((int(line[1]), int(line[2])))
			self.edgeArray.append((int(line[2]), int(line[3])))
			self.edgeArray.append((int(line[3]), int(line[1])))

			triangle1 = Face((int(line[1]), int(line[2]), int(line[3])), [1,1,1], (100,100,100))

			self.faceArray.append(triangle1)


	def create_wireframe(self):

		Object = wireframe.Wireframe()

		Object.addNodes(np.array(self.nodeArray))
		Object.addEdges(self.edgeArray)
		
		for i in self.faceArray:
			Object.addFaces([i])

		Object.addMaterial(self.materialDictionary)

		return Object
