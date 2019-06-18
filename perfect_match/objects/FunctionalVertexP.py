from perfect_match.objects.BipartiteVertex import VertexP

class FunctionalVertexP(VertexP):
    ''' inherits  BipartiteVertex
        :param lable X so that the :BipartiteGraph lable function is X->vertex
        :param neighbor_sup a function : index-> neighbor vertex'''
    def __init__(self, lable, neighbor_sup):
        VertexP.__init__(self, lable)
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

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, FunctionalVertexP) and self.name == o.name
