from .BipartiteVertex import BipartiteVertex
from .BipartiteGraph import BipartiteSet

class VertexP(BipartiteVertex):
    def __init__(self,lable, neighbor_sup):
        BipartiteVertex.__init__(self,lable, BipartiteSet.P, neighbor_sup)

    def get_neighboors(self):
        return self.neighbor_suplier()

    def __str__(self):
        return str(self.lable)+"P"

    def __repr__(self):
        return self.__str__()
