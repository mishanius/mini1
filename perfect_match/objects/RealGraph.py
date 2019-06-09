import random

class RealGraph:

	def __init__(self, n, d):
		if n == 0 or d == 0:
			raise Exception("Graph with 0 vertices or 0 neighbors isn't supported")
		if d > n-1:
			raise Exception("d's value cannot be bigger than n-1")
		self.groupP, self.groupQ = self.generateNeighbores(n, d, self.generateGroup(n), self.generateGroup(n), 0)

	def generateGroup(self, n):
		return {k:[] for k in range(1, n+1)}

	def generateCountedGroup(self, n, d):
		return {k:d for k in range(1, n+1)}

	def generateNeighbores(self, n, d, firstGroup, secondGroup, loopCounter):
		optionalNeighbores = self.generateCountedGroup(n,d)
		for x in firstGroup.keys():
			uniteratedOptionalNeighbors = list(optionalNeighbores.keys())
			while(1):
				if len(firstGroup[x]) == d:             #vertex x has d neighbors, we can move to next vertex
					if x == n:                          #if its the last vertex, we're done with the procedure
						print("Looped: ", loopCounter)
						return firstGroup, secondGroup
					break                               #vertex x has d neighbors, we can move to next vertex
				a = uniteratedOptionalNeighbors.pop(random.randrange(len(uniteratedOptionalNeighbors))) #pick random ind that wasnt picked before for this vertex
				if len(firstGroup[n]) < d-1 and len(uniteratedOptionalNeighbors) == 0:
					return self.generateNeighbores(n, d, self.generateGroup(n), self.generateGroup(n), loopCounter+1)
				if not(a in firstGroup[x]):           #check that choosen vertex isnt already a neighbor
					firstGroup[x].append(a)             #if isnt, add to x's neighbor list
					secondGroup[a].append(x)
					optionalNeighbores[a] = optionalNeighbores[a]-1 #mark that choosen vertex a has room for 1 less neighbor
					if optionalNeighbores[a] == 0:
						del optionalNeighbores[a]

	def getGroupP(self):
		return self.groupP

	def getGroupQ(self):
		return self.groupQ

	def getNeighborsOfP(self):
		return list(map(self.groupP.get, self.groupP.keys()))

	def getNeighborsOfQ(self):
		return list(map(self.groupQ.get, self.groupQ.keys()))

	#def getRandomMatching(self):


print("-------Testing with n=10, d=4")
graph = RealGraph(10000, 15)
#print(graph.getNeighborsOfP())
'''
a,b  = generateGraph(10, 4)
print(a)
print(b, "\n")

print("-------Testing with n=100, d=7")
a,b  = generateGraph(100, 7)
print(a)
print(b, "\n")
print("-------Testing with n=1,000, d=7")
a,b  = generateGraph(1000, 7)
print(a)
print(b, "\n")
print("-------Testing with n=10,000, d=7")
a,b  = generateGraph(10000, 7)
print(a)
print(b, "\n")
'''