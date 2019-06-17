from .BipartiteGraph import BipartiteSet
from abc import ABC, abstractmethod


class BipartiteVertex(ABC):
    def __init__(self, lable=None, vertex_set=BipartiteSet.P, neighbor_sup=None):
        """
        abstract class representing a vertex in a bipartite graph
        each vertex is BipartiteSet.Q or BipartiteSet.P
        each vertex got a neighboor suplier: function: i->BipartiteVertex
        each vertex got a label (an integer representing the number of the vertex)
        each vertex got a name a string that includes the number of the vertex and more data
        """
        self.lable = lable
        self.vertex_set = vertex_set
        self.neighbor_suplier = neighbor_sup

    @property
    def name(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.name)

    def get_neighboors(self):
        """returns a list of neighbors
            this is a final list"""
        i = 0
        res = []
        while self.neighbor_suplier(i) is not None:
            res.append(self.neighbor_suplier(i))
            i += 1
        return res

    def get_neighboor(self, index):
        """returns a neighbor at place index"""
        return self.neighbor_suplier(index)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, BipartiteVertex) and self.name == o.name