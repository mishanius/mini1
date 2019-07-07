from perfect_match.objects.IBipartiteGraph import IBipartiteGraph


class BipartiteFunctionalGraph(IBipartiteGraph):
    """
        this is a final immutble graph hance it doesnt support addition/removal of edges
        addition/removal of vertices
        this object is actually only a wrapper
    """

    def __init__(self, d, lable_generator=lambda: (), lable_to_vertex_lambda=lambda l: 1 / 0):
        """ initializes a graph object
            If no dictionaries or None is given,
            an empty bipartite graph will be initiated
        """
        super().__init__(d)
        self.lable_generator = lable_generator
        self.lable_to_vertex_lambda = lable_to_vertex_lambda

    def get_vertex(self, lable):
        return self.lable_to_vertex_lambda(lable)

    def vertices_p(self):
        """
        returns a generator of all the vertices in the graph
        """
        return (self.lable_to_vertex_lambda(l) for l in self.lable_generator())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def __generate_edges(self):
        """ TODO ADD DOCUMENTATION
        creates a edge generator
        """
        for v in self.vertices_p():
            for n in v.get_neighboors():
                yield (v, n)

    def __str__(self):
        raise Exception("unimplemented")

    def __repr__(self):
        return self.__str__()
