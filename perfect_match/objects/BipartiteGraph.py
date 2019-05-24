from enum import Enum
import numpy as np
""" Python Class
A bipartite graph class,
with P, Q sets of nodes, each represented by a dict.
In each dict the keys are the nodes and the vals are arrays of neighbors (if correct bipartite graph)
the neighbors are from the other set.
"""


class BipartiteSet(Enum):
    P = 0
    Q = 1



def compute_if_absent(key, d):
    """
    helper static method for dictioneries
    """
    if key not in d:
        d[key] = np.array([])


class BipartiteGraph(object):

    def __init__(self, p_dict=None, q_dict=None):
        """ initializes a graph object
            If no dictionaries or None is given,
            an empty bipartite graph will be initiated
        """
        if p_dict is None:
            p_dict = {}
        if q_dict is None:
            q_dict = {}
        self.__p_dict = p_dict
        self.__q_dict = q_dict


    def vertices(self):
        """ returns the vertices of a graph """
        res = list(self.__p_dict.keys())
        res.extend(self.__q_dict.keys())
        return res

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex, set):
        """ If set is not P or Q throws an error.
            if the vertex "vertex" is not in
            self.__set_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if set != BipartiteSet.P and set != BipartiteSet.Q:
            raise Exception("set should be 1 or 2")
        if set == BipartiteSet.P:
            compute_if_absent(vertex, self.__p_dict)
        if set == BipartiteSet.Q:
            compute_if_absent(vertex, self.__q_dict)

    def get_q(self):
        return self.__q_dict

    def get_p(self):
        return self.__p_dict

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!

        """
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__p_dict:
            if vertex2 in self.__p_dict or vertex2 not in self.__q_dict:
                raise Exception("edge between vertexes from same group or vertex doesnt exist")
            self.__p_dict[vertex1] = np.append(self.__p_dict[vertex1], vertex2)
            return
        if vertex1 in self.__q_dict:
            if vertex2 in self.__q_dict or vertex2 not in self.__p_dict:
                raise Exception("edge between vertexes from same group or vertex doesnt exist")
            self.__q_dict[vertex1] = np.append(self.__q_dict[vertex1], vertex2)
            return
        raise Exception("vertex doesnt exist")

    def __generate_edges(self):
        """ We assume if 'a' has neighbor 'b' then 'b' has neighbor 'a'
            a static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__p_dict:
            for neighbour in self.__p_dict[vertex]:
                if (vertex , neighbour) not in edges:
                    edges.append((vertex, neighbour))
        return edges

    def __direct_graph(self):
        """
        removes edges that are not in the direction P->Q
        """
        for vertex in self.__q_dict:
            self.__q_dict[vertex] = []

    def __str__(self):
        res = "P vertices: "
        for k in self.__p_dict:
            res += str(k) + " "
        res = "\nQ vertices: "
        for k in self.__q_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res