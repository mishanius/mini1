from .BipartiteVertex import BipartiteVertex
from .BipartiteGraph import BipartiteSet

class VertexQ(BipartiteVertex):
    def __init__(self,lable, neighbor_sup):
        BipartiteVertex.__init__(self,lable, BipartiteSet.Q, neighbor_sup)

    def get_neighboors(self):
        return self.neighbor_suplier()

    def __str__(self):
        return str(self.lable)+"Q"

    def __repr__(self):
        return self.__str__()
