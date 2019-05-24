from perfect_match.objects.BipartiteGraph import BipartiteGraph
def generate_simple_full_graph(n):
    p = [str(x) for x in range(1,n)]
    q = [str(-x) for x in range(1,n)]
    p_dict = {}
    q_dict = {}
    for k in p:
        p_dict[k] = q
    for k in q:
        q_dict[k] = []
    return BipartiteGraph(p_dict, q_dict)

def generate_simple_d_regular_offset_graph(d, n):
    p = [str(x) for x in range(1, n+1)]
    q = [str(-x) for x in range(1, n+1)]
    p_dict = {}
    q_dict = {}
    for k in range(0,n):
        p_dict[p[k]] = []
        for a in range(0,d):
            l = k+a
            if l<n:
                p_dict[p[k]].append(q[l])
            else:
                l = l - n
                p_dict[p[k]].append(q[l])
    return BipartiteGraph(p_dict, q_dict)