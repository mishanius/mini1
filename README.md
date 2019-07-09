# Mini in randomized algorithms
## intro
in this project we find perfect matching in d regular bi-partite graphs via random walks.
we follow the following article https://arxiv.org/pdf/0909.3346.pdf

we work with a number of diffarent graphs:
- real graphs (all vertices and edges are in ram) 
- real random graphs 
- functional garphs (each vertex got a function which generates neighboors as a lazy list)
- exclusive expander using the margolis construction for bipartite graph 
## usage
```
main.py --full/--expander/--functional/--random -d <d regularity> -n <number of edges>
```
### example 
```
main.py --random -n 500 -d 100
```
will create a random 100 regular bipartite graph with 500 vertices and find a perfect match in it

## output and metrics
each run of the script produces the following output:
1. a mapping betwing vertices from P group to Q group, this mapping is a perfect match
2. a graph representing the number of moves made inside truncated walk, as a function of number of matchings
3. metrics:
      - "took" total runtime in seconds
      - "algorithm bruto move" number of moves made by the script including algorithm moves as described, symetric diffarance and creation of super nodes
      - "algorithm move" number of moves made explicitly by the algorithm as described in the article 
      - "truncated_walk" longest truncated walk
      - "whole iteration" longest time(seconds) to make *one* matching 
      - "mod_symetric_difference" longest time(seconds) to make a symetric diffarance 
      
### example output  
  ```
  main.py --random -n 100 -d 10
  ```
  ```
  perfect_match.objects.MetricLogger - INFO - MetricLogger has started
random graph - INFO - metric algorithm move : 705
took:0.33397722244262695
random graph - INFO - metric d : 10
random graph - INFO - metric n : 100
random graph - INFO - metric truncated_walk_moves : [1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 4, 5, 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 1, 2, 3, 4, 1, 2, 1, 2, 3, 4, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 1, 2, 3, 4, 5, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 1, 2, 1, 2, 3, 4, 5, 1, 2, 3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 1, 2, 3, 4, 5, 1, 2, 1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 1, 2, 3, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 1, 2, 3, 4, 5, 6]
random graph - INFO - metric algorithm bruto move : 1231
random graph - INFO - timing for mod_symetric_difference : 0.01565241813659668
random graph - INFO - timing for whole iteration : 0.01565241813659668
random graph - INFO - timing for truncated_walk : 120
random graph - INFO - timing for full_walk : 0.0
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
   
      
