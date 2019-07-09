import logging
import time

import numpy as np

from perfect_match.objects.BipartiteVertex import VertexP
from perfect_match.objects.MetricLogger import MetricLogger

max_time = {}
ALGO_MOV = "algorithm move"
BRUTO_MOV = "algorithm bruto move"


def find_match(bi_graph, metric_logger=None):
    if not metric_logger:
        metric_logger=MetricLogger(logging.INFO)
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
        chosen_index = np.random.randint(0, n - j)
        chosen = s.pop(chosen_index)
        start_time = time.time()
        metric_logger.inc_metric(ALGO_MOV)
        metric_logger.inc_metric(BRUTO_MOV)
        truncated_walk(chosen, b - 1, bi_graph, path, supers, 0, metric_logger)
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
            metric_logger.info("matched {}".format(j))
        metric_logger.log_max_time("whole iteration", starti)
    return matches


def mod_symetric_difference(path, matches, supers, chosen, metric_logger):
    """this function updates the matches (mutation), removes all even edges that are present in path (backward)
        and adds new edges
    """
    start_time = time.time()
    symetric_dif_walk(path, matches, supers, chosen, metric_logger)
    metric_logger.log_max_time("mod_symetric_difference", start_time)
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
    moves = 1
    while True:
        metric_logger.log_max("truncated_walk",moves)
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
                metric_logger.append_metric("truncated_walk_moves", moves)
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
        moves+=1


def path_to_matching(path):
    moves = set()
    for k in path:
        moves.add(frozenset({k, path[k]}))
    return moves