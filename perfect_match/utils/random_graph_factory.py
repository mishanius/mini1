from perfect_match.objects.BipartiteRealGraph import BipartiteRealGraph
from ..objects.RealVertexP import RealVertexP
from ..objects.RealVertexQ import RealVertexQ
import numpy as np


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

