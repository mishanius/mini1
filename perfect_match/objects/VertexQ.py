from .BipartiteVertex import BipartiteVertex
from .BipartiteGraph import BipartiteSet

class VertexQ(BipartiteVertex):
    ''' inherits  BipartiteVertex
            :param label X so that the :BipartiteGraph label function is X->vertex
            :param neighbor_sup a function : index-> neighbor vertex'''
    def __init__(self,label, neighbor_sup):
        BipartiteVertex.__init__(self,label, BipartiteSet.Q, neighbor_sup)

    def __str__(self):
        return str(self.label)+"Q"

    def __repr__(self):
        return self.__str__()
