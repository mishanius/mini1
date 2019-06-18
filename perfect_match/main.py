import json
import argparse
from functools import reduce

import numpy as np
import logging

from perfect_match.objects.BipartiteRealGraph import BipartiteRealGraph
from perfect_match.objects.BipartiteVertex import VertexP
from perfect_match.objects.MetricLogger import MetricLogger
from perfect_match.objects.BipartiteGraph import BipartiteGraph
from perfect_match.objects.RealVertexP import RealVertexP
from perfect_match.objects.RealVertexQ import RealVertexQ
from perfect_match.objects.bi_graph_generator import generate_simple_d_regular_offset_graph
import time

max_time = {}
ALGO_MOV = "algorithm move"
BRUTO_MOV = "algorithm bruto move"


def find_match(bi_graph, metric_logger=MetricLogger(logging.INFO)):
    s = [p for p in bi_graph.vertices_p()]
    n = len(s)
    matches = {}
    supers = {}
    j = 0
    metric_logger.inc_metric(ALGO_MOV)
    metric_logger.inc_metric(BRUTO_MOV)
    while len(matches) < n:
        starti = time.time()
        b = 2 * (2 + n / (n - j))
        path = {}
        start_time = time.time()
        chosen_index = np.random.randint(0, n - j)
        metric_logger.log_max_time("random", start_time)
        start_time = time.time()
        chosen = s.pop(chosen_index)
        metric_logger.log_max_time("remove", start_time)
        fail_count = 0
        start_time = time.time()
        metric_logger.inc_metric(ALGO_MOV)
        metric_logger.inc_metric(BRUTO_MOV)
        while not truncated_walk(chosen, b - 1, bi_graph, path, supers, 0, metric_logger):
            metric_logger.log_max_time("truncated_walk", start_time)
            metric_logger.debug("failed truncated b is {}".format(b))
            path = {}
            metric_logger.inc_metric(ALGO_MOV)
            fail_count += 1
            if (fail_count > 5000):
                metric_logger.info("failed more then 5000!!")
                continue
                # raise Exception("failed retry b:{0} supers:{1}".format(b, matches))
        metric_logger.log_max_time("full_walk", start_time)
        x = len(matches)

        matches = mod_symetric_difference(path, matches, supers, chosen, metric_logger)
        metric_logger.inc_metric(ALGO_MOV)
        metric_logger.inc_metric(BRUTO_MOV)
        y = len(matches)
        if x + 1 < y:
            raise Exception("not a match!!!!!!!!!!!!!!!!")
        j = j + 1
        if j % 500 == 0:
            metric_logger.info("matched {} failed {}".format(j, fail_count))
        metric_logger.log_max_time("whole iteration", starti)
    return matches


def mod_symetric_difference(path, matches, supers, chosen, metric_logger):
    """this function updates the matches (mutation), removes all even edges that are present in path (backward)
        and adds new edges
    """
    start_time = time.time()
    symetric_dif_walk(path, matches, supers, chosen, metric_logger)
    metric_logger.log_max_time("mod_symetric_difference", start_time)
    sst2 = reduce(reducer, matches.values(), set())
    return matches


def symetric_dif_walk(path, matches, supers, curr, metric_logger):
    while True:
        metric_logger.inc_metric(BRUTO_MOV)
        if isinstance(curr, VertexP):
            matches[curr] = path[curr]
            supers[path[curr]] = curr
            curr = path[curr]
            if not curr in path:
                return
        else:
            del matches[path[curr]]
            curr = path[curr]


def truncated_walk(s, b, bi_graph, path, supers, move=0, metric_logger=None):
    while True:
        if isinstance(s, VertexP):
            next = s.get_neighboor(np.random.randint(0, bi_graph.d))
            path[s] = next
            metric_logger.debug("{0} -> {1}".format(s, next))
            metric_logger.inc_metric(BRUTO_MOV)
            metric_logger.inc_metric(ALGO_MOV)
            b -= 1
            s = next
        else:
            if s not in supers:
                metric_logger.debug("true {}".format(b))
                metric_logger.log_max("truncated_walk", move)
                return True
            else:
                paired_in_super = supers[s]
                path[s] = paired_in_super
                metric_logger.debug("{0} -> {1}".format(s, paired_in_super))
                next = paired_in_super.get_neighboor(np.random.randint(0, bi_graph.d))
                path[paired_in_super] = next
                metric_logger.debug("{0} -> {1}".format(paired_in_super, next))
                metric_logger.inc_metric(BRUTO_MOV)
                metric_logger.inc_metric(ALGO_MOV)
                s = next
                b -= 1


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


def create_random_graph_matching_reduction(n, d):
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
        matches = find_match(temp_graph,metric_logger)
        for match in matches.keys():
            i = new_p_group.index(match)
            new_p_group[i].add_neighboor(matches[match])
            p_group[i].remove_neighbore(matches[match])
        temp_max_d -= 1
        temp_d -= 1
    return BipartiteRealGraph(d, new_p_group)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds matching for d regular graph')
    parser.add_argument('--json', help='json file path', )
    parser.add_argument('--full', help='create match in a full graph', )
    parser.add_argument('--functional', help='create match in a functional graph', )
    args = parser.parse_args()
    start = time.time()
    metric_logger = MetricLogger(logging.INFO)
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
            res = find_match(generate_simple_d_regular_offset_graph(200, 1000), metric_logger)
            # sst = reduce(reducer, res, set())
            # print(len(sst))
            # print(sst)
            # print(res)
            # print(len(res))
    if args.functional:
        real = create_random_graph_matching_reduction(100, 30)
        res = find_match(real)
        # p = modolu_graph(200000, 1500)
        # metric_logger.experiment = "functional_{}".format(i)
        # res = find_match(modolu_graph(100, 2))
        print(res)
        #
        sst = reduce(reducer, res, set())
        print(len(sst))
        print(sst)
        #
        sst2 = reduce(reducer, res.values(), set())
        print(len(sst2))
        print(sst2)

        metric_logger.flush_all()
        # print(len(res))
    end = time.time()
    print("took:{}".format(end - start))
    print(max_time)
