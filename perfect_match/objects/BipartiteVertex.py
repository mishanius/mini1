from abc import ABC, abstractmethod
from enum import Enum


class BipartiteSet(Enum):
    P = 0
    Q = 1


class BipartiteVertex(ABC):

    def __init__(self, lable=None, vertex_set=BipartiteSet.P):
        '''
           abstract class representing a vertex in a bipartite graph
           each vertex is BipartiteSet.Q or BipartiteSet.P
           each vertex got a label (an integer representing the number of the vertex)
           each vertex got a name a string that includes the number of the vertex and more data
        '''
        self.lable = lable
        self.vertex_set = vertex_set

    def __repr__(self):
        return self.__str__()

    def get_label(self):
        return self.lable

    @property
    def name(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.name)

    @abstractmethod
    def get_neighboors(self):
        """returns a list of neighbors
                    this is a final list"""
        pass

    @abstractmethod
    def get_neighboor(self, index):
        """returns a neighbor at place index"""
        pass


class VertexQ(BipartiteVertex):
    def __init__(self, lable=None):
        super().__init__(lable, BipartiteSet.Q)

    def __str__(self):
        return str(self.lable) + "Q"


class VertexP(BipartiteVertex):
    def __init__(self, lable=None):
        super().__init__(lable, BipartiteSet.P)

    def __str__(self):
        return str(self.lable) + "P"
