import unittest
from perfect_match.objects.BipartiteGraph import BipartiteGraph, BipartiteSet

class TestSum(unittest.TestCase):
    def setUp(self):
        p = {"a": ["d"],
             "b": ["e"],
             "c": ["f"],
             }
        q = {"d": ["a"],
             "e": ["b"],
             "f": ["c"],
             }

        self.graph = BipartiteGraph(p, q)

    def test_vartices(self):
        print("Vertices of graph:")
        actual = set(self.graph.vertices())
        expected = {'c', 'a', 'b', 'e', 'd', 'f'}
        self.assertTrue(actual.issubset(expected))
        self.assertTrue(expected.issubset(actual))

    def test_edge(self):
        print("Edges of graph:")
        print(self.graph.edges())
        actual = set(self.graph.edges())
        expected = {('b', 'e'), ('c', 'f'), ('a', 'd')}
        self.assertTrue(actual.issubset(expected))
        self.assertTrue(expected.issubset(actual))

    def test_add_vertex(self):
        self.graph.add_vertex("z", BipartiteSet.Q)
        actual = set(self.graph.vertices())
        expected = {'c', 'a', 'b', 'e', 'd', 'f', 'z'}
        self.assertTrue(actual.issubset(expected))
        self.assertTrue(expected.issubset(actual))

    def test_add_edge(self):
        self.graph.add_vertex("z", BipartiteSet.Q)
        self.graph.add_edge(("a", "z"))
        actual = set(self.graph.edges())
        expected = {('b', 'e'), ('c', 'f'), ('a', 'd'), ('a', 'z')}
        self.assertTrue(actual.issubset(expected))
        self.assertTrue(expected.issubset(actual))

if __name__ == '__main__':
    unittest.main()
