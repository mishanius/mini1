from .BipartiteGraph import BipartiteSet
from abc import ABC, abstractmethod


class BipartiteVertex(ABC):
    def __init__(self, num_of_vertex, label=None, vertex_set=BipartiteSet.P, neighbore_sup=(lambda i: None)):
        """
        abstract class representing a vertex in a bipartite graph
        each vertex is BipartiteSet.Q or BipartiteSet.P
        each vertex got a neighbores supplier: function: i->BipartiteVertex
        """
        self.label = label
        self.vertex_set = vertex_set
        self.neighbore_supplier = neighbore_sup
        self.num_of_vertex = num_of_vertex

    def get_neighbores(self):
        """returns a list of neighbores
            this is a final list"""
        i = self.label
        res = []
        while self.neighbore_supplier(i) is not None:
            res.append(self.neighbore_supplier(str(int(i)%self.num_of_vertex)))
            i= str(int(i)+1)
            if int(i)>int(self.label)+5:
                break
        return res

    def get_neighbore(self, index):
        #TODO: changed this to try
        """returns a neighbore at place index"""
        return self.neighbore_supplier(index)
