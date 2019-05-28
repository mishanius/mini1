import unittest
from perfect_match.objects.BipartiteFunctiionalGraph import BipartiteFunctionalGraph
from perfect_match.objects.VertexP import VertexP
from perfect_match.objects.VertexQ import VertexQ


class TestFunctionalGraph(unittest.TestCase):
    @staticmethod
    def create_neigbor_expression(i, d, n):
        return lambda index: VertexQ(i + index, lambda index: None) if index + i <= n and index < d else (
            VertexQ(index+i - n, lambda index: None) if index < d else None)

    def setUp(self):
        d = 2
        n = 3
        self.label_generator_lambda = lambda: (i for i in range(1, n + 1))
        self.label_to_vertex_expression = lambda l: VertexP(l, self.create_neigbor_expression(l, d, n))
        self.graph = BipartiteFunctionalGraph(self.label_generator_lambda, self.label_to_vertex_expression)

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


if __name__ == '__main__':
    unittest.main()
