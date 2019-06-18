import unittest

from perfect_match.objects.FunctionalVertexP import FunctionalVertexP
from perfect_match.objects.FunctionalVertexQ import FunctionalVertexQ
from perfect_match.utils.functional_graph_factory import modolu_graph


class TestFunctionalGraph(unittest.TestCase):

    def setUp(self):
        self.graph = modolu_graph(3,2)

    def test_get_vertex(self):
        p = self.graph.get_vertex(2)
        actual = set([str(x) for x in p.get_neighboors()])
        expected = {'2Q', '3Q'}
        self.assertTrue(actual.issubset(expected))
        self.assertTrue(expected.issubset(actual))

    def test_edge(self):
        actual = set([str(x) for x in self.graph.edges()])
        expected = {'(3P, 3Q)', '(2P, 3Q)', '(3P, 1Q)', '(1P, 1Q)', '(2P, 2Q)', '(1P, 2Q)'}
        self.assertTrue(actual.issubset(expected))
        self.assertTrue(expected.issubset(actual))

    def test_vertex_eq(self):
        test_dict={}
        test_dict[FunctionalVertexP(1, lambda i:None)] = "blah blah"
        new_instance = FunctionalVertexP(1, lambda i:None)
        self.assertTrue(new_instance in test_dict)
        new_instance = FunctionalVertexP(2, lambda i: None)
        self.assertFalse(new_instance in test_dict)
        new_instance = FunctionalVertexQ(1, lambda i: None)
        self.assertFalse(new_instance in test_dict)