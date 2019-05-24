import json
import argparse
import numpy as np
from perfect_match.objects.BipartiteGraph import BipartiteGraph
from perfect_match.objects.bi_graph_generator import generate_simple_full_graph, generate_simple_d_regular_offset_graph
from functools import reduce
from perfect_match.objects.BipartiteGraph import BipartiteSet
import time


def find_match(bi_graph):
    s = list(bi_graph.get_p().keys())
    n = len(bi_graph.get_p().keys())
    matches = set()
    supers = {}
    j = 0
    while len(matches) < n:
        b = 2*(2 + n / (n - j))
        path = {}
        chosen = np.random.choice(s, 1)[0]
        s.remove(chosen)
        fail_count = 0
        # print("b:{} j:{}".format(b, j))
        while not truncated_walk(chosen, b - 1, bi_graph, path, supers):
            path = {}
            fail_count += 1
            if(fail_count>1000):
                print("failed retry b:{0} supers:{1}".format(b, supers))

        if fail_count > 2:
            print("fail count:{0}".format( fail_count))
        x = len(matches)
        old = matches.copy()
        matches = matches.symmetric_difference(path_to_matching(path))
        y = len(matches)
        if x+1<y:
            print("not a match!!!!!!!!!!!!!!!!")
            exit()
        # print("matches:{}".format(matches))
        supers = superize(matches)
        j = j + 1
    return matches


def truncated_walk(s, b, bi_graph, path, supers, verbous = False):
    if b < 1:
        return False
    if s in bi_graph.get_p():
        next = np.random.choice(bi_graph.get_p()[s], 1)[0]
        path[s] = next
        # print("{0} -> {1}".format(s, next))
        return truncated_walk(next, b - 1, bi_graph, path, supers)
    else:
        if s not in supers:
            # print("true {}".format(b))
            return True
        else:
            paired_in_super = supers[s]
            path[s] = paired_in_super
            # print("{0} -> {1}".format(s, paired_in_super))
            neigbors = bi_graph.get_p()[paired_in_super].copy()
            neigbors.remove(s)
            next = np.random.choice(neigbors, 1)[0]
            path[paired_in_super] = next
            # print("{0} -> {1}".format(paired_in_super, next))
            return truncated_walk(next, b - 1, bi_graph, path, supers)


def superize(matchings):
    supers = {}
    for (x, y) in matchings:
        supers[x] = y
        supers[y] = x
    return supers


def path_to_matching(path):
    moves = set()
    for k in path:
        moves.add(frozenset({k, path[k]}))
    return moves


def reducer(acc, y):
    old = len(acc)
    acc.add(y[0])
    if old == len(acc):
        print("not a MATCH!!! {}".format(y[0]))
    return acc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds matching for d regular graph')
    parser.add_argument('--json', help='json file path', )
    parser.add_argument('--full', help='create match in a full graph', )
    args = parser.parse_args()
    start = time.time()
    if args.json:
        fh = open(args.json)
        data = json.load(fh)
        bi_graph = BipartiteGraph(data['P'], data['Q'])
        res = find_match(bi_graph)
        # sst = reduce(reducer, res, set())
        print(len(res))
        print(res)
    if args.full:
        for i in range(0,100):
            res = find_match(generate_simple_d_regular_offset_graph(3,2000))
            # sst = reduce(reducer, res, set())
            # print(len(sst))
            # print(sst)
            # print(res)
            # print(len(res))
    end = time.time()
    print("took:{}".format(end - start))
