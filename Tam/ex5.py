# APPFS Exercise 5
# by Tam Tran
# in Python3

# 3 goals:
# 1) read in graph as CSV and extract its edge information to distances between vertices
# 2) update the distance between the vertices anytime a shorter distance is found (shortest path)
# 3) return the longest shortest path

import sys
import pandas as pd
import numpy as np

def run(graphfile):
    
    graph = pd.read_csv(graphfile, sep = " ", names = ['src', 'dst', 'weight']).drop(0)
    
    # generate distances dataframe
    unique_vertices = np.unique(np.append(graph['src'].unique(), graph['dst'].unique()))
    distances = pd.DataFrame(unique_vertices, columns = ['vertex'])
    distances['shortest_distance'] = [float('inf')] * distances.shape[0]
    distances['previous_vertex'] = [None] * distances.shape[0]
    
    # to keep track of the vertices that have been processed
    visited = []
    unvisited = list(distances['vertex'])
    
    # setting the vertex 1 as our reference/starting vertex
    s = 1
    unvisited.remove(s)
    visited.append(s)
    distances.loc[distances.vertex == s, 'shortest_distance'] = 0 
    next_s = s

    # run shortest path algorithm
    while unvisited:
        distances, next_s = update_distances(graph, distances, next_s, unvisited)
        unvisited.remove(next_s)
        visited.append(next_s)
        
    # get longest shortest path
    print("RESULT VERTEX", distances.loc[distances['shortest_distance'].argmax(), 'vertex'])
    print("RESULT DIST", int(distances['shortest_distance'].max()))
    
    
def update_distances(graph, distances, s, unvisited):
    
    for dnode in graph[graph['src'] == s]['dst']:

        current_dist = distances[distances.vertex == dnode].iloc[0]['shortest_distance']
        s_weight = distances.loc[distances.vertex == s, 'shortest_distance']
        edge_weight = graph.loc[(graph['src'] == s) & (graph['dst'] == dnode), 'weight']
        compare_dist = float(s_weight) + float(edge_weight)
        
        if current_dist > compare_dist:
            distances.loc[distances.vertex == dnode, ['shortest_distance', 'previous_vertex']] = compare_dist, s

    # get the next_s that is still in unvisited
    indices = distances['shortest_distance'].argsort() #returns list of indices of elements in ascending order
    for i in indices:
        if distances.iloc[i]['vertex'] in unvisited:
            next_s = distances.iloc[i]['vertex']
            break

    return distances, next_s    


graphfile = sys.argv[1]
run(graphfile)