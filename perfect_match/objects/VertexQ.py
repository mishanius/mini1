from .BipartiteVertex import BipartiteVertex
from .BipartiteGraph import BipartiteSet

class VertexQ(BipartiteVertex):
    ''' inherits  BipartiteVertex
            :param lable X so that the :BipartiteGraph lable function is X->vertex
            :param neighbor_sup a function : index-> neighbor vertex'''
    def __init__(self,lable, neighbor_sup=None):
        BipartiteVertex.__init__(self,lable, BipartiteSet.Q, neighbor_sup)

    def __str__(self):
        return str(self.lable)+"Q"

    def __repr__(self):
        return self.__str__()
