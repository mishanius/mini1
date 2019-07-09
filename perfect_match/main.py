import argparse
from functools import reduce
import pprint
import logging

from perfect_match.objects.MetricLogger import MetricLogger
from perfect_match.objects.match_finder import find_match, max_time
from perfect_match.utils.functional_graph_factory import modolu_graph
from perfect_match.utils.real_graph_factory import generate_simple_d_regular_offset_graph, generate_expander, \
    create_random_graph_matching_reduction
import time


def reducer(acc, y):
    old = len(acc)
    acc.add(y)
    if old == len(acc):
        raise Exception("not a MATCH!!! {}".format(y))
    return acc


def complete_test():
    graph_constructors = (generate_simple_d_regular_offset_graph, modolu_graph, create_random_graph_matching_reduction)
    for graph_constructor in graph_constructors:
        if graph_constructor != modolu_graph:
            mult = 100
            continue
        else:
            mult = 1000
        for i in range(1, 35, 1):
            metric_logger.experiment = str(mult * i)
            metric_logger.set_metric("graph generating function", graph_constructor.__name__)
            metric_logger.set_metric("d", int((mult * i) / 2))
            metric_logger.set_metric("n", int(mult * i))
            res = find_match(graph_constructor(mult * i, int((mult * i) / 2)), metric_logger)
            metric_logger.flush_all()
        metric_logger.create_full_move_plot()
        metric_logger.trunc_walk_per_match()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds matching for d regular graph')
    parser.add_argument('-n', type=int, help='number of vertices')
    parser.add_argument('-d', type=int, help='d-regularity')
    parser.add_argument('--full', action='store_true', help='create match in a full graph')
    parser.add_argument('--expander', action='store_true', help='create match in an expander graph')
    parser.add_argument('--functional', action='store_true', help='create match in a functional graph')
    parser.add_argument('--random', action='store_true', help='create match in a random d regular graph')
    parser.add_argument('--complete_test', action='store_true', help='tests all the cases')
    args = parser.parse_args()
    start = time.time()
    metric_logger = MetricLogger(logging.INFO)
    res = 0
    if args.complete_test:
        complete_test()
        exit()
    elif args.full:
        metric_logger.experiment = "offset graph"
        metric_logger.set_metric("d", args.d)
        metric_logger.set_metric("n", args.n)
        res = find_match(generate_simple_d_regular_offset_graph(args.n, args.d), metric_logger)
        metric_logger.flush_all()
    elif args.functional:
        metric_logger.experiment = "functional graph"
        metric_logger.set_metric("d", args.d)
        metric_logger.set_metric("n", args.n)
        res = find_match(modolu_graph(args.n, args.d), metric_logger)
        metric_logger.flush_all()
    elif args.random:
        graph = create_random_graph_matching_reduction(args.d, args.n)
        metric_logger.experiment = "random graph"
        metric_logger.set_metric("d", args.d)
        metric_logger.set_metric("n", args.n)
        res = find_match(graph, metric_logger)
        metric_logger.flush_all()
    elif args.expander:
        res = find_match(generate_expander())
    else:
        print("usage: --full/--expander/--function/--complete_test -n <some number> -d <some number>")
        exit()

    end = time.time()
    print("took:{}".format(end - start))
    sst = reduce(reducer, res, set())
    sst2 = reduce(reducer, res.values(), set())
    if len(sst) != args.n:
        exit(2)
    elif len(sst2) != args.n:
        exit(2)
    else:
        pp = pprint.PrettyPrinter(indent=4)
        metric_logger.trunc_walk_per_match()
        # pp.pprint(res)
