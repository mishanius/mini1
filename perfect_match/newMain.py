import json
import argparse
import numpy as np
import random
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
        chosen = unmatchedPVertices.pop(random.randrange(len(unmatchedPVertices)))
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
        next = choosenVertic.get_neighbor(indGen) #next = the neighbore, which belongs to Q.
        path[choosenVertic.__str__()] = next.__str__() #attach the pair (choosenVertice,next)
        return truncated_walk(next, b - 1, bi_graph, path, superNodes, pVertices)
    else:                #this scenerio stands for when choosenVertic is actually from Q
        superNodesKeys = superNodes.keys()
        if not choosenVertic.__str__() in superNodesKeys:   #check if choosenVertic doesnt participate in the match
            return True                                     #if it doesnt - we wanna continue, we're good !
        else:                                               #choosenVertic is already in the match, so we want to update
            other = superNodes[choosenVertic.__str__()]     #other is choosenVertic' old matched vertice from P
            del superNodes[choosenVertic.__str__()]         #we erase the old match that choosenVertice participated in
            del superNodes[other]
            path[choosenVertic.__str__()] = other  #update path to hold (choosenVertic,other) edge
            paired_in_super_vertex = bi_graph.get_vertex(other[:len(other)-1]) #get p's vertice object (not just label)
            neighbors = paired_in_super_vertex.get_neighbores().copy() #get all of p's neighbors
            listedSuperNodesKeys = list(superNodesKeys)
            listedSuperNodesKeys.append(choosenVertic.__str__()) #add choosenVertic to already-matched vertices
            neighbors = [x for x in neighbors if x.__str__() not in listedSuperNodesKeys] #filter out from neighbors
                                                                                          #the already-matched vertices
            next = np.random.choice(neighbors) #choose a new vertex from Q so we can continue the procedure
            path[other] = next.__str__()
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
        counter=0
        for i in range(0,10):
            #TODO: insert argument 'n' aswell to config
            n=10000
            bi_graph = BipartiteFunctionalGraph(lambda:(i for i in range(0,n)),lambda l:(VertexP(n, l, lambda i:(VertexQ(n, i,lambda i: None) if int(i)>n else VertexQ(n, int(i)%n, lambda i: None)))))
            try:
                res = find_match(bi_graph)
                counter+=1
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
    print("took:{}".format(end - start), "and sucseeded: ", counter, " times!")
