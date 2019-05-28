from .BipartiteGraph import BipartiteSet
from abc import ABC, abstractmethod


class BipartiteVertex(ABC):
    def __init__(self, lable=None, vertex_set=BipartiteSet.P, neighbor_sup=(lambda i: None)):
        """
        abstract class representing a vertex in a bipartite graph
        each vertex is BipartiteSet.Q or BipartiteSet.P
        each vertex got a neighboor suplier: function: i->BipartiteVertex
        """
        self.lable = lable
        self.vertex_set = vertex_set
        self.neighbor_suplier = neighbor_sup

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
