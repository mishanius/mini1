# Mini-project for Ben Gurion University, in subject of randomized algorithms.
## intro
in this project we find perfect matching in d regular bi-partite graphs via random walks.
we follow the following article https://arxiv.org/pdf/0909.3346.pdf

we support working on a number of different graphs:
- real graphs (all vertices and edges are in ram) 
- real random graphs 
- functional garphs (each vertex holds a function which generates neighbors as a lazy list)
- exclusive expander using the margolis construction for bipartite graph 

## dependencies
- numpy
- matplotlib
## usage
```
main.py --full/--expander/--functional/--random -d <d regularity> -n <number of edges>
```
### example 
```
main.py --random -n 500 -d 100
```
will create a random 100 regular bipartite graph with 500 vertices and find a perfect match in it.

## output and metrics
each run of the script produces the following output:
1. a mapping of vertices from P group to Q group, which is the perfect match calculated.
2. a graph representing the number of moves made in the method truncated walk, as a function of number of couples found in the growing matching at the time.
3. metrics:
      - "took" - total runtime (in seconds).
      - "algorithm bruto move" - number of moves made by the script, including 'algorithm moves' as described, symetric difference and           creation of super nodes.
      - "algorithm move" - number of moves made explicitly by the algorithm as described in the article.
      - "truncated_walk" - longest truncated walk (in terms of how many times the while loop executed).
      - "whole iteration" -  longest time (in seconds) to make *one* matching.
      - "mod_symetric_difference" - longest time (in seconds) to calculate a symetric difference.
      
### example output  
  ```
  main.py --random -n 100 -d 10
  ```
  ```
perfect_match.objects.MetricLogger - INFO - MetricLogger has started
perfect_match.objects.MetricLogger - INFO - MetricLogger has started
random graph - INFO - metric algorithm bruto move : 1341
random graph - INFO - metric truncated_walk_moves : [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 4, 3, 2, 2, 2, 4, 3, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 4, 4, 2, 3, 8, 3, 4, 2, 4, 2, 4, 2, 2, 3, 3, 4, 2, 2, 9, 5, 7, 7, 2, 2, 4, 5, 2, 6, 9, 3, 4, 3, 7, 2, 23, 4, 4, 3, 10, 8, 2, 24, 10, 34, 17, 25, 40, 43, 99, 81]
random graph - INFO - metric n : 100
random graph - INFO - metric d : 10
random graph - INFO - metric algorithm move : 781
random graph - INFO - timing for mod_symetric_difference : 0.0
random graph - INFO - timing for full_walk : 0.0
random graph - INFO - timing for truncated_walk : 99
random graph - INFO - timing for whole iteration : 0.0
took:0.3537905216217041
{   99P: 80Q,
    100P: 51Q,
    97P: 49Q,
    98P: 85Q,
    95P: 93Q,
    96P: 8Q,
    1P: 95Q,
    2P: 11Q,
    3P: 83Q,
    4P: 57Q,
    5P: 82Q,
    6P: 65Q,
    7P: 66Q,
    8P: 64Q,
    9P: 75Q,
    10P: 60Q,
    11P: 70Q,
    12P: 87Q,
    ... more matchings...}
  ```
  ![alt text](https://github.com/mishanius/mini1/blob/michael_real_graph/perfect_match/output_example/myplot.png "Logo Title Text 1")
   
## more running examples 
```add some examples```

## notes
### working with functional graphs :
The class is called BipartiteFunctionalGraph
1. each BipartiteFunctionalGraph recieves :
      - a label generation function (label is usually a number or a string)
      - a label to functionalVertex function
2. each FunctionalVertex recieves:
      - a label 
      - a neighbor supplier - a function : index-> neighbor vertex
3. currently we are working with a modulu graph - for each i in P, i's neighbors in Q are i, i+1, i+2, ... (i+d)%n 
### example from code
modolu_graph creates a functional modulu graph, the constructor receives a label generator and a 'lable to vertex' function
each vertex i receives a function that maps an index 0...d-1 to neighbor vertex at index.
```
def create_neighbor_expression(i, d, n):
    return lambda index: FunctionalVertexQ(i + index, lambda index: None) if index + i <= n and index < d else (
        FunctionalVertexQ(index + i - n, lambda index: None) if index < d else None)

def modolu_graph(n, d):
    label_generator_lambda = lambda: (i for i in range(1, n + 1))
    label_to_vertex_expression = lambda l: FunctionalVertexP(l, create_neigbor_expression(l, d, n))
    return BipartiteFunctionalGraph(d, label_generator_lambda, label_to_vertex_expression)
```
## working with metric logger : TODO

## a few words regarding the interfaces and classes : TODO
