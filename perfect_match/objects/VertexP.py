from .BipartiteVertex import BipartiteVertex
from .BipartiteGraph import BipartiteSet


class VertexP(BipartiteVertex):
    ''' inherits  BipartiteVertex
        :param label X so that the :BipartiteGraph label function is X->vertex
        :param neighbor_sup a function : index-> neighbor vertex'''
    def __init__(self, num_of_vertex, label, neighbore_sup):
        BipartiteVertex.__init__(self,num_of_vertex, label, BipartiteSet.P, neighbore_sup)

    def __str__(self):
        return str(self.label) + "P"

    def __repr__(self):
        return self.__str__()
