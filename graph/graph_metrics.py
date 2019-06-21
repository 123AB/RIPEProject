# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:25:40 2019

@author: Brian
"""

import numpy as np
import networkx as nx
import time
import random

def assortativity(G):
    if hasattr(G, "assortativity"):
        print("Assortativity = {:.5f}. Returned cached value.".format(G.assortativity))
        return G.assortativity
    start = time.time()
    assort = nx.degree_assortativity_coefficient(G)
    end = time.time()
    print("Assortativity = {:.5f}. Time elapsed: {:.5f} seconds".format(assort, end-start))
    G.assortativity = assort
    return assort

#Clustering Coefficient of Multigraph?
#Naive clustering
def simple_cc(G):
    if hasattr(G, "simple_cc"):
        print("Clustering coefficient = {:.5f}. Returned cached value.".format(G.simple_cc))
        return G.simple_cc
    start = time.time()
    Gsimp = nx.Graph()
    for n1, n2 in G.edges():
        Gsimp.add_edge(n1.norm_id, n2.norm_id)
    end_g = time.time()
    print("Graph constructed. Time elapsed: {:.5f} seconds".format(end_g-start))
    cc = nx.average_clustering(Gsimp)
    end_cc = time.time()
    print("Clustering coefficient = {:.5f}. Time elapsed: {:.5f} seconds".format(cc, end_cc-end_g))
    G.simple_cc = cc
    return cc

#Hop count

def hop_count(G, sample_size = 10000):
    if hasattr(G, "hop_count") and hasattr(G, "hop_count_ss"):
        if G.hop_count_ss == sample_size:
            print("Average hop count = {:.5f} (sample size = {}). Returned cached value.".format(G.hop_count, G.hop_count_ss))
            return G.hop_count
    #Check if sample size is valid
    if sample_size < 0:
        raise Exception("Sample size cannot be negative.")
    #Check if graph is connected. If not, take the biggest component.
    if not nx.is_connected(G):
        print("Graph is disconnected. Using largest component.")
        components = list(nx.connected_components(G))
        sizes = list()
        for component in components:
            sizes.append(len(component))
        stacked = np.column_stack((components, sizes))
        ind=np.argsort(-stacked[:,1])
        stacked = stacked[ind]
        nodes = list(stacked[0,0])
    else:
        nodes = list(G.nodes)
    #Check if sample size is valid
    n_nodes = len(nodes)
    if n_nodes < 2:
        print("Not enough nodes. Average hop count undefined.")
        return float('NaN')
    n_pairs = int(n_nodes*(n_nodes-1)/2)   
    if sample_size > n_pairs:
        print("Sample size exceeds number of node pairs. Using all node pairs instead.")
        sample_size = 0
    #Sample node pairs
    if sample_size == 0:
        indexes = range(n_pairs)
    else:
        random.seed(a=time.time())
        indexes = random.sample(range(n_pairs), sample_size)
    #Calculate shortest paths
    hop_counts = list()
    for index in indexes:
        pair = _pair_helper(nodes, index)
        hop_counts.append(_sp_helper(G, nodes, pair))
    hop_count = np.mean(hop_counts)
    #Return
    G.hop_count_ss = sample_size
    G.hop_count = hop_count
    return G.hop_count

#Given a node list and an index, select a random pair of nodes
def _pair_helper(node_list: list, index: int) -> tuple:
    n_nodes = len(node_list)
    n_pairs = int(n_nodes*(n_nodes-1)/2)
    if index < 0 or index > n_pairs-1:
        raise Exception("Index out of range")
    #Begin
    for n1 in range(n_nodes-1, 0, -1):
        #Arithmetic series sum
        offset = int(n1 * (n1-1) / 2)
        if index >= offset:
            n2 = index - offset
            return (n1, n2)

#Compute the shortest path between two nodes
#Inputs: graph, node list, node pair specified as a tuple of indexes in the node list
def _sp_helper(graph, node_list: list, pair: tuple) -> int:
    sn = node_list[pair[0]]
    tn = node_list[pair[1]]
    return nx.algorithms.shortest_paths.generic.shortest_path_length(graph, source=sn,target=tn,weight=None)    