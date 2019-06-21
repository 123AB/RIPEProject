# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:48:15 2019

@author: 14496
"""
import os

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pickle
import json
import scipy.stats as sp
import matplotlib.colors as mcolors
import time


#def draw(G, pos, measures, measure_name):
    
#    nodes = nx.draw_networkx_nodes(G, pos, node_size=250, cmap=plt.cm.plasma, 
#                                   node_color=measures.values(),
#                                   nodelist=measures.keys())
#    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
    
    # labels = nx.draw_networkx_labels(G, pos)
#    edges = nx.draw_networkx_edges(G, pos)

#    plt.title(measure_name)
#    plt.colorbar(nodes)
#    plt.axis('off')
#    plt.show()
    
def draw(G, pos, measures, measure_name):
    nodes = nx.draw_networkx_nodes(G, pos, node_size=10, cmap=plt.cm.plasma, 
                                   node_color=np.array(list(measures.values())).astype(float),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
    
    # labels = nx.draw_networkx_labels(G, pos)
#     edges = nx.draw_networkx_edges(G, pos)

    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()


def betweenness_centrality(G):
    start = time.time()
    print("Calculate the betweenness_centrality")
    G2 = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    end = time.time()
    print("The Calculation is finished")
    G.betweeness = G2
    return G2

def percolation_centrality(G):
    G2 = nx.percolation_centrality(G, attribute='percolation', states=None, weight=None)
    return G2


def clustering_coefficient(G):

    CC = nx.clustering(G,node=None, weight=None)
    return CC
#matplotlib inline

filelocation="data/"
filename="201603.as-rel-geo3.txt"

filepath=filelocation+filename

edge_list = pd.read_csv(filepath, sep='|', usecols=[0,1], header=None, names=["source", "target"])

# edge_list.describe()
# edge_list.head

#print(edge_list.iloc[:5])

# test_list = edge_list.head(1000)
# G = nx.from_pandas_edgelist(test_list)
# nx.draw(G)


G = nx.from_pandas_edgelist(edge_list)

graph_nodes = G.__len__()
graph_edges = G.size()

pos = nx.spectral_layout(G)

#pos = nx.spring_layout(G)

draw(G, pos, nx.betweenness_centrality(G), 'Betweenness Centrality')

G3 = betweenness_centrality(G)
print("The graph is:")
print(G3)

#plot
#node_sample_sizes = [10, 50, 100, 500, 1000, 2500]
#frac_list = []

#for s in node_sample_sizes:
#    degree_loc = [edge_list['source'].value_counts()[n:].index[0] for n in range(0,s)]
#    size_subgraph = edge_list.loc[edge_list['source'].isin(degree_loc)].shape[0]
#    fraction = size_subgraph / graph_edges
#    frac_list.append(fraction)
    
#df_frac = pd.DataFrame(list(zip(node_sample_sizes, frac_list)),columns=['sample_size','betweeness'])
#ax = sns.lineplot(x='sample_size', y='betweeness', data=df_frac)
##############

# Number of nodes
#print("Number of nodes in graph: \n\t", graph_nodes)
# Number of edges
#print("Number of edges in graph: \n\t", graph_edges)


#degrees = list(dict(G.degree()).values())

#plt.title("Degree Histogram")
#plt.ylabel("Count [Log]")
#plt.xlabel("Degree")
#plt.hist(degrees, density=True, log=True)
#plt.show()

# Show 10 highest degrees
#print(sorted(degrees)[::-1][:10])
# Show 10 lowest degrees
#print(sorted(degrees)[:10])


#node_sample_sizes = [10, 50, 100, 500, 1000, 2500]
#frac_list = []

#for s in node_sample_sizes:
#    degree_loc = [edge_list['source'].value_counts()[n:].index[0] for n in range(0,s)]
#    size_subgraph = edge_list.loc[edge_list['source'].isin(degree_loc)].shape[0]
#    fraction = size_subgraph / graph_edges
#    frac_list.append(fraction)
    
#print(frac_list)

#df_frac = pd.DataFrame(list(zip(node_sample_sizes, frac_list)),columns=['sample_size','fraction'])
#ax = sns.lineplot(x='sample_size', y='fraction', data=df_frac)

#r=nx.degree_assortativity_coefficient(G)
#print(r)


# Select the largest connected component

#connected_components = nx.connected_components(G)
#largest_cc = max(connected_components, key=len)
#G2 = G.subgraph(largest_cc)
#print(len(G2))


# component_list = [len(n) for n in connected_components]
# print(np.max(sorted(component_list)))
# print(component_list)
# print(sorted(component_list)[::-1][:5])

#graph_nodes = G2.__len__()
#graph_edges = G2.size()

# Number of nodes
#print("Number of nodes in graph: \n\t", graph_nodes)
# Number of edges
#print("Number of edges in graph: \n\t", graph_edges)


#percolation_centrality(G)
#percolation_centrality(G)
#clustering_coefficient(G)

def checkSpread(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

"""
def shorestPath(G, initial):
      visited = {initial: 0}
      path = {}

      nodes = set(G.nodes)

      while nodes: 
          min_node = None
          for node in nodes:
              if node in visited:
                  if min_node is None:
                      min_node = node
                  elif visited[node] < visited[min_node]:
                          min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in G.edges[min_node]:
            weight = current_weight + G.distance[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node
    return visited, path
"""



