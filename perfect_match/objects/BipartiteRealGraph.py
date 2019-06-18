from perfect_match.objects.IBipartiteGraph import IBipartiteGraph


class BipartiteRealGraph(IBipartiteGraph):
    def __init__(self, d, vertices_p):
        super().__init__(d)
        self.__vertices_p = vertices_p

    def get_vertex(self, lable):
        return self.__vertices_p[lable]

    def vertices_p(self):
        """
        returns a generator of all the vertices in the graph
        """
        return self.__vertices_p

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def __generate_edges(self):
        """ TODO ADD DOCUMENTATION
        creates a edge generator
        """
        for v in self.vertices_p():
            for n in v.get_neighboors():
                yield (v,n)


    def __str__(self):
        raise Exception("unimplemented")

    def __repr__(self):
        return self.__str__()