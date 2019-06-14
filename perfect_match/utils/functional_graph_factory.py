from perfect_match.objects.BipartiteFunctiionalGraph import BipartiteFunctionalGraph
from perfect_match.objects.VertexP import VertexP
from perfect_match.objects.VertexQ import VertexQ


def create_neigbor_expression(i, d, n):
    return lambda index: VertexQ(i + index, lambda index: None) if index + i <= n and index < d else (
        VertexQ(index + i - n, lambda index: None) if index < d else None)


def modolu_graph(n, d):
    label_generator_lambda = lambda: (i for i in range(1, n + 1))
    label_to_vertex_expression = lambda l: VertexP(l, create_neigbor_expression(l, d, n))
    return BipartiteFunctionalGraph(d, label_generator_lambda, label_to_vertex_expression)
