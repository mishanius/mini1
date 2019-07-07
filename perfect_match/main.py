import argparse
from functools import reduce

import logging

from perfect_match.objects.MetricLogger import MetricLogger
from perfect_match.objects.match_finder import find_match, max_time
from perfect_match.utils.real_graph_factory import generate_simple_d_regular_offset_graph, generate_expander, \
    create_random_graph_matching_reduction
import time


def reducer(acc, y):
    old = len(acc)
    acc.add(y)
    if old == len(acc):
        raise Exception("not a MATCH!!! {}".format(y))
    return acc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds matching for d regular graph')
    parser.add_argument('--full', help='create match in a full graph', )
    parser.add_argument('--expander', help='create match in an expander graph', )
    parser.add_argument('--functional', help='create match in a functional graph', )
    args = parser.parse_args()
    start = time.time()
    metric_logger = MetricLogger(logging.INFO)
    res = 0
    if args.full:
        for i in range(0, 1):
            res = find_match(generate_simple_d_regular_offset_graph(200, 5000), metric_logger)
    elif args.functional:
        real = create_random_graph_matching_reduction(100, 30)
        res = find_match(real)
    elif args.expander:
        res = find_match(generate_expander())
    else:
        print("usage: --full/--expander/--function <some number>")
        exit()

    print(res)
    sst = reduce(reducer, res, set())
    print(len(sst))
    print(sst)
    sst2 = reduce(reducer, res.values(), set())
    print(len(sst2))
    print(sst2)

    metric_logger.flush_all()

    end = time.time()
    print("took:{}".format(end - start))
    print(max_time)
