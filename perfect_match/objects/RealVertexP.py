from .BipartiteVertex import BipartiteVertex
from .VertexP import VertexP

class RealVertexP(BipartiteVertex, VertexP):

	def __init__(self, label):
		self.label = label
		self.groupFlag = 0 			#groupFlag=1 represents group Q, groupFlag=0 represents group P


	def getLabel(self):
		return self.label

	#returns a list of vertex objects
	def getNeighbores(self):
		return self.neighbors

	#returns a list of vertex' labels
	def getNeighboresLabels(self):
		return list(map(lambda x: x.getLabel() ,self.neighbors))

	#returns a specific vertex object
	def get_neighboor(self,index):
		return self.neighbors[index]

	def getGroupFlag(self):
		return self.groupFlag

	#def appendNeighbor

	def setNeighbors(self, group):
		self.neighbors = group[self].copy()