from .VertexP import VertexP
class BipartiteFunctionalGraph(object):
    """
        this is a final immutble graph hance it doesnt support addition/removal of edges
        addition/removal of vertices
        this object is actually only a wrapper
    """

    def __init__(self, label_generator=lambda :(), label_to_vertex_lambda = lambda l:1/0):
        """ a graph generator: parameters are:
                label_generator:  a function with no parameters, that returns nothing. what the function
                                does in generating a label (=name\index) for a new generated vertex (without creating
                                a vertex).
                                the function should be a for loop in range (i,n+1)  - this way we get the
                                wanted size of the graph we'll generate
                                
                label_to_vertex_lambda: a function that receives a label, and returns the corresponding vertex
                (creating the vertex).
        """
        self.label_generator = label_generator
        self.label_to_vertex_lambda = label_to_vertex_lambda



    def get_vertex(self, label):
        return self.label_to_vertex_lambda(label)

    def vertices_p(self):
        """
        returns a generator of all the vertices in the graph
        """
        return (self.label_to_vertex_lambda(l) for l in self.label_generator())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def __generate_edges(self):
        """ TODO ADD DOCUMENTATION
        creates a edge generator
        """
        for v in self.vertices_p():
            for n in v.get_neighbores():
                yield (v,n)


    def __str__(self):
        raise Exception("unimplemented")

    def __repr__(self):
        return self.__str__()
