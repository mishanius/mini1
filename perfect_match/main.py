import json
import argparse
from functools import reduce

import numpy as np

from perfect_match.objects.VertexP import VertexP
from perfect_match.objects.BipartiteGraph import BipartiteGraph
from perfect_match.objects.bi_graph_generator import generate_simple_d_regular_offset_graph
import time

from perfect_match.utils.functional_graph_factory import modolu_graph

max_time = {}


def find_match(bi_graph):
    s = [p for p in bi_graph.vertices_p()]
    n = len(s)
    matches = {}
    supers = {}
    j = 0
    while len(matches) < n:
        starti = time.time()
        b = 2 * (2 + n / (n - j))
        path = {}
        start = time.time()
        chosen_index = np.random.randint(0,n-j)
        end = time.time()
        update_timer(end - start, "random")
        start = time.time()
        chosen = s.pop(chosen_index)
        end = time.time()
        update_timer(end - start, "remove")
        fail_count = 0
        # print("b:{} j:{}".format(b, j))
        verbose = False
        start = time.time()
        while not truncated_walk(chosen, b - 1, bi_graph, path, matches, verbose):
            end = time.time()
            update_timer(end - start, "truncated_walk")
            if verbose:
                print("failed truncated b is {}".format(b))
            path = {}
            fail_count += 1
            if (fail_count > 50000):
                raise Exception("failed retry b:{0} supers:{1}".format(b, matches))
        end = time.time()
        update_timer(end - start, "full_walk")
        x = len(matches)
        start = time.time()
        matches = mod_symetric_difference(path, matches, supers)
        end = time.time()
        update_timer(end - start, "mod_symetric_difference")
        y = len(matches)
        if x + 1 < y:
            print("not a match!!!!!!!!!!!!!!!!")
            exit()
        j = j + 1
        endi=time.time()
        update_timer(endi-starti,"whole iteration")
    return matches


def mod_symetric_difference(path, matches, supers):
    """this function updates the matches (mutation), removes all even edges that are present in path (backward)
        and adds new edges
    """
    for k in path.keys():
        if isinstance(k, VertexP):
            matches[k] = path[k]
            supers[path[k]] = k
        elif matches[path[k]] == k:
            del matches[path[k]]
            del supers[k]
    return matches


def update_timer(value, string):
    if string not in max_time.keys():
        max_time[string] = value
    elif max_time[string] < value:
        max_time[string] = value


def truncated_walk(s, b, bi_graph, path, supers, verbous=False):
    if b < 1:
        return False
    if isinstance(s, VertexP):
        next = s.get_neighboor(np.random.randint(0, bi_graph.d))
        path[s] = next
        if verbous:
            print("{0} -> {1}".format(s, next))
        return truncated_walk(next, b - 1, bi_graph, path, supers, verbous)
    else:
        if s not in supers:
            if verbous:
                print("true {}".format(b))
            return True
        else:
            paired_in_super = supers[s]
            path[s] = paired_in_super
            if verbous:
                print("{0} -> {1}".format(s, paired_in_super))
            next = paired_in_super.get_neighboor(np.random.randint(0, bi_graph.d))
            path[paired_in_super] = next
            if verbous:
                print("{0} -> {1}".format(paired_in_super, next))
            return truncated_walk(next, b - 1, bi_graph, path, supers, verbous)


def superize(matchings):
    supers = {}
    for k in matchings.keys():
        supers[k] = matchings[k]
        supers[matchings[k]] = k
    return supers


def path_to_matching(path):
    moves = set()
    for k in path:
        moves.add(frozenset({k, path[k]}))
    return moves


def reducer(acc, y):
    old = len(acc)
    acc.add(y)
    if old == len(acc):
        raise Exception("not a MATCH!!! {}".format(y))
    return acc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds matching for d regular graph')
    parser.add_argument('--json', help='json file path', )
    parser.add_argument('--full', help='create match in a full graph', )
    parser.add_argument('--functional', help='create match in a functional graph', )
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
        for i in range(0, 100):
            res = find_match(generate_simple_d_regular_offset_graph(3, 2000))
            # sst = reduce(reducer, res, set())
            # print(len(sst))
            # print(sst)
            # print(res)
            # print(len(res))
    if args.functional:
        res = find_match(modolu_graph(10000, 5))
        sst = reduce(reducer, res, set())
        # print(len(sst))
        # print(sst)
        # print(res)
        # print(len(res))
    end = time.time()
    print("took:{}".format(end - start))
    print(max_time)
