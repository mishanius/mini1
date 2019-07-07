
import unittest

from perfect_match.utils.real_graph_factory import generate_expander, create_random_graph_matching_reduction


class TestGraphs(unittest.TestCase):

    def test_margulis_expander(self):
        graph = generate_expander()
        self.validate_d_regularity(graph, 100, 8)
    
    def test_random_graph_generation_by_reduction(self):
        graph = create_random_graph_matching_reduction(10,5)
        self.validate_d_regularity(graph, 10, 5)
        graph = create_random_graph_matching_reduction(100, 5)
        self.validate_d_regularity(graph, 100, 5)
        graph = create_random_graph_matching_reduction(300, 120)
        self.validate_d_regularity(graph, 300, 120)

    def validate_d_regularity(self, bipartite_graph, n, d):
        ps = {}
        qs = {}
        for p in bipartite_graph.vertices_p():
            ps[p] = len(p.get_neighboors())
            for q in p.get_neighboors():
                if q in qs:
                    qs[q] += 1
                else:
                    qs[q] = 1
        # validations
        self.assertTrue(len(ps) == n)
        self.assertTrue(len(qs) == n)
        for p in ps:
            self.assertTrue(len(p.get_neighboors()) == d)
        for q in qs:
            self.assertTrue(qs[q] == d)


if __name__ == '__main__':
    unittest.main()
