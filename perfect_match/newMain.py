

import json
import argparse
import numpy as np
from perfect_match.objects.BipartiteGraph import BipartiteGraph
from perfect_match.objects.BipartiteFunctiionalGraph import BipartiteFunctionalGraph
from perfect_match.objects.VertexP import VertexP
from perfect_match.objects.VertexQ import VertexQ
from perfect_match.objects.BipartiteVertex import BipartiteVertex
from perfect_match.objects.bi_graph_generator import generate_simple_full_graph, generate_simple_d_regular_offset_graph
from functools import reduce
from perfect_match.objects.BipartiteGraph import BipartiteSet
import time


def find_match(bipartiteFunctionalGraph):
    matches = set()
    superNodes = {}
    j = 0
    pVerticesGenerator = bipartiteFunctionalGraph.vertices_p()
    pVertices=[x for x in pVerticesGenerator]
    unmatchedPVertices= pVertices.copy()    #Deep copies, so we can remove from this variable
    n=len(pVertices)
    while len(matches) < n:
        b = 2*(2 + n / (n - j))
        path = {}
        chosen = np.random.choice(unmatchedPVertices)
        while (chosen in superNodes.keys()):
            chosen = np.random.choice(unmatchedPVertices) #little change: no need [0] if we send only 1 argument
        unmatchedPVertices.remove(chosen)
        fail_count = 0
        while not truncated_walk(chosen, b - 1, bipartiteFunctionalGraph, path, superNodes, pVertices):
            path = {}
            fail_count += 1
            if(fail_count>1000):
                print("failed retry b:{0} superNodes:{1}".format(b, superNodes))
        if fail_count > 2:
            print("fail count:{0}".format( fail_count))
        x = len(matches)
        matches = matches.symmetric_difference(path_to_matching(path))
        y = len(matches)
        if x+1<y:
            print("not a match!!!!!!")
            exit()
        superNodes = superize(matches)
        j = j + 1
        if j==n and len(matches)<n:
            raise Exception("J REACHED ITS LIMIT")
    return matchesToSortedPairs(matches)


def truncated_walk(choosenVertic, b, bi_graph, path, superNodes, pVertices, verbous = False):
    #global nrange
    if b < 1:
        return False
    if choosenVertic in pVertices: #checks if the vertice is from group P
        indGen = np.random.choice(range(n)) #generates a neighbore of choosenVertic, choosenVertice belongs to P.
        #TODO: problem - the line below can generate ANY index in range, isnt necessarelly a neighbor.
        next = choosenVertic.get_neighbore(indGen) #next = the neighbore, which belongs to Q.
        path[choosenVertic.__str__()] = next.__str__() #attach the pair (choosenVertice,next)
        return truncated_walk(next, b - 1, bi_graph, path, superNodes, pVertices)
    else:                #this scenerio stands for when choosenVertic is actually from Q
        superNodeskeys = superNodes.keys()
        flag=0
        for x in superNodeskeys:
            if choosenVertic.__str__() == x:     #and this verifies this ver doesnt participate yet in the matching
                flag=1                     #therefore - we want to add it to match
                break
        if flag==0:
            return True
        else:
            other = superNodes[choosenVertic.__str__()] #the value, which is a P vertex
            del superNodes[choosenVertic.__str__()]
            del superNodes[other]
            paired_in_super = other #this will ret the ver from Q's matched neighbore, which is from P.
            path[choosenVertic.__str__()] = paired_in_super
            paired_in_super_vertex = bi_graph.get_vertex(paired_in_super[0])
            neighbors = paired_in_super_vertex.get_neighbores().copy()
            if choosenVertic in neighbors:
                neighbors.remove(choosenVertic)
            next = np.random.choice(neighbors) #choose a new vertex from Q so we can continue the procedure
            path[paired_in_super] = next.__str__()
            return truncated_walk(next, b - 1, bi_graph, path, superNodes, pVertices)


def superize(matchings):
    supers = {}
    for (x, y) in matchings:
        z = x.__str__()
        w = y.__str__()
        supers[z] = w
        supers[w] = z
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


def matchesToSortedPairs(matches):
    matcheslist=[]
    fixedmatcheslist=[]
    for x in matches:
        matcheslist.append(list(x))
    for y in matcheslist:
        if 'P' in y[0]:
            y=[y[1],y[0]]
        fixedmatcheslist.append(y)
    fixedmatcheslist.sort(key=get_label)
    # ----- THE FOLLOWING 3 LINES ARE TO FIX SORTING BY P! ALSO, CHANGE *if 'p' in y[0]* TO 'Q'
    #temp = fixedmatcheslist[0]
    #fixedmatcheslist.remove(temp)
    #fixedmatcheslist.append(temp)
    return fixedmatcheslist

def get_label(list):
    return list[0]

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
            #TODO: insert argument 'n' aswell to config
            n=10
            bi_graph = BipartiteFunctionalGraph(lambda:(i for i in range(1,n+1)),lambda l:(VertexP(n, l, lambda i:(VertexQ(n, i,lambda i: None) if int(i)>n else VertexQ(n, int(i)%n, lambda i: None)))))
            try:
                res = find_match(bi_graph)
                print("result is: ",res)
            except Exception as msg:
                print(msg)
                continue
            #res = find_match(generate_simple_d_regular_offset_graph(3,2000))
            # sst = reduce(reducer, res, set())
            # print(len(sst))
            # print(sst)
            # print(res)
            # print(len(res))
    end = time.time()
    print("took:{}".format(end - start))
