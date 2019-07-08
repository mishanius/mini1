import logging

import numpy as np

from perfect_match.objects.BipartiteRealGraph import BipartiteRealGraph
from perfect_match.objects.MetricLogger import MetricLogger
from perfect_match.objects.RealVertexP import RealVertexP
from perfect_match.objects.RealVertexQ import RealVertexQ
from perfect_match.objects.match_finder import find_match

def generate_simple_full_graph(n):
    p_group = [RealVertexP(i) for i in range(1, n + 1)]
    for k in p_group:
        k.set_neighboors([RealVertexQ(i) for i in range(1, n + 1)])
    return BipartiteRealGraph(n, p_group)

def generate_simple_d_regular_offset_graph(n, d):
    p_group = [RealVertexP(i) for i in range(1, n + 1)]
    for k in range(0, n):
        for a in range(0, d):
            l = k + a
            if l < n:
                p_group[k].add_neighboor(RealVertexQ(l))
            else:
                l = l - n
                p_group[k].add_neighboor(RealVertexQ(l))
    return BipartiteRealGraph(d, p_group)

def generate_expander():
    t1 = np.matrix('1 2; 0 1')
    t2 = np.matrix('1 0; 2 1')
    t1inv = np.linalg.inv(t1)
    t2inv = np.linalg.inv(t2)
    e1 = np.matrix('1; 0')
    e2 = np.matrix('1; 0')
    vertices = [(i, j) for i in range(10) for j in range(10)]
    p_group = [RealVertexP(i) for i in vertices]
    for v in p_group:
        vec = np.transpose(np.asmatrix(np.asanyarray(v.get_label())))
        val = np.matmul(t1, vec)

        v.add_neighboor(RealVertexQ((int(val[0].item()) % 10, int(val[1].item()) % 10)))

        val2 = np.add(val, e1)
        v.add_neighboor(RealVertexQ((int(val2[0].item()) % 10, int(val2[1].item()) % 10)))

        val = np.matmul(t2, vec)
        v.add_neighboor(RealVertexQ((int(val[0].item()) % 10, int(val[1].item()) % 10)))

        val2 = np.add(val, e2)
        v.add_neighboor(RealVertexQ((int(val2[0].item()) % 10, int(val2[1].item()) % 10)))

        val = np.matmul(t1inv, vec)
        v.add_neighboor(RealVertexQ((int(val[0].item()) % 10, int(val[1].item()) % 10)))

        val2 = np.add(val, e1)
        v.add_neighboor(RealVertexQ((int(val2[0].item()) % 10, int(val2[1].item()) % 10)))

        val = np.matmul(t2inv, vec)
        v.add_neighboor(RealVertexQ((int(val[0].item()) % 10, int(val[1].item()) % 10)))

        val2 = np.add(val, e2)
        v.add_neighboor(RealVertexQ((int(val2[0].item()) % 10, int(val2[1].item()) % 10)))
    return BipartiteRealGraph(8, p_group)


def create_random_graph_matching_reduction(d, n):
    metric_logger = MetricLogger(logging.ERROR)
    p_group = [RealVertexP(i) for i in range(1, n + 1)]
    new_p_group = [RealVertexP(i) for i in range(1, n + 1)]
    q_group = [RealVertexQ(i) for i in range(1, n + 1)]
    for p in p_group:
        p.set_neighboors(q_group.copy())
    temp_max_d = n
    temp_d = d
    while temp_d > 0:
        temp_graph = BipartiteRealGraph(temp_max_d, p_group.copy())
        matches = find_match(temp_graph, metric_logger)
        for match in matches.keys():
            i = new_p_group.index(match)
            new_p_group[i].add_neighboor(matches[match])
            p_group[i].remove_neighbore(matches[match])
        temp_max_d -= 1
        temp_d -= 1
    return BipartiteRealGraph(d, new_p_group)


def create_random_graph(n, d):
    p_group = [RealVertexP(i) for i in range(1, n + 1)]
    q_group = [RealVertexQ(i) for i in range(1, n + 1)]
    done = False
    i = 0
    while (not done):
        if len(q_group) < d:
            i = 0
            p_group = [RealVertexP(i) for i in range(1, n + 1)]
            q_group = [RealVertexQ(i) for i in range(1, n + 1)]
        neighboors_select = list(np.random.choice(q_group, d, replace=False))
        new_neighboors = []
        for nbr in neighboors_select:
            new_neighboors.append(nbr)
            nbr.add_neighboor(p_group[i])
            if len(nbr.get_neighboors()) == d:
                q_group.remove(nbr)
        p_group[i].set_neighboors(new_neighboors)
        if i == n - 1:
            done = True
        else:
            i += 1
    return BipartiteRealGraph(d, p_group)