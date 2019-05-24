from .BipartiteGraph import BipartiteSet
from abc import ABC, abstractmethod


class BipartiteVertex(ABC):
    def __init__(self, lable=None, vertex_set=BipartiteSet.P, neighbor_sup=(lambda: 1 / 0)):
        """
        abstract class representing a vertex in a bipartite graph
        each vertex is BipartiteSet.Q or BipartiteSet.P
        """
        self.lable = lable
        self.vertex_set = vertex_set
        self.neighbor_suplier = neighbor_sup

    def get_neighboors(self):
        """returns a list of neighbors
            this is a final list"""
        return self.neighbor_suplier()
