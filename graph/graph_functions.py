# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 22:22:19 2019

@author: Brian
"""

import numpy as np
import networkx as nx

#Build a nid_to_node dictionary
def nid_to_node(G):
    if not hasattr(G, "nid_to_node"):
        G.nid_to_node = dict()
        for node in G.nodes:
            G.nid_to_node[node.norm_id] = node

#Get the distribution of each component in G
def components_list(G):
    #Sort the components by size.
    components = list(nx.connected_components(G))
    sizes = list()
    for component in components:
        sizes.append(len(component))
    stacked = np.column_stack((components, sizes))
    ind=np.argsort(-stacked[:,1])
    stacked = stacked[ind]
    components = list(stacked[:,0])
    return components

#Get component distribution sorted smallest to largest
def components_distribution(G, reverse = False):
    components = list(nx.connected_components(G))
    key_list = list()
    sizes = dict()
    for component in components:
        size = len(component)
        if not size in sizes.keys():
            sizes[size] = 1
            key_list.append(size)
        else:
            sizes[size] = sizes[size] + 1

    val_list = list()
    for key in key_list:
        val_list.append(sizes[key])
    
    stacked = np.column_stack((key_list, val_list))
    if not reverse:
        ind = np.argsort(stacked[:,0])
    else:
        ind = np.argsort(-stacked[:,0])
    stacked = stacked[ind]
    
    return list(stacked[:,0]), list(stacked[:,1])

#Largest component as subgraph
def largest_subgraph(G):
    #Sort the components by size.
    components = list(nx.connected_components(G))
    sizes = list()
    for component in components:
        sizes.append(len(component))
    stacked = np.column_stack((components, sizes))
    ind=np.argsort(-stacked[:,1])
    stacked = stacked[ind]
    components = list(stacked[:,0])
    #Make the largest component into a graph
    Gsub = nx.MultiGraph(G.subgraph(components[0]))
    return Gsub

#Returns components, largest first
def sorted_components(G, reverse = False):
    components = list(nx.connected_components(G))
    sizes = list()
    for component in components:
        sizes.append(len(component))
    stacked = np.column_stack((components, sizes))
    if not reverse:
        ind=np.argsort(-stacked[:,1])
    else:
        ind=np.argsort(stacked[:,1])
    stacked = stacked[ind]
    components = list(stacked[:,0])
    return components

#Get distance from dictionary
def get_distance(ct1, ct2, distances):
    if (ct1, ct2) in distances.keys():
        return distances[ct1, ct2]
    elif (ct2, ct1) in distances.keys():
        return distances[ct2, ct1]
    else:
        print("Error: distance not found.")
        return float("nan")

#Get list of cities within a certain radius of another city
#https://stackoverflow.com/questions/36244380/enumerate-for-dictionary-in-python
def get_cities_within_radius(ct, radius, distances):
    cts = list()
    for k, ((ct1, ct2), dist) in enumerate(distances.items()):
            if ct == ct1:
                if dist < radius:
                    cts.append(ct2)
            elif ct == ct2:
                if dist < radius:
                    cts.append(ct1)
#    print("Cities: " + str(len(cts)))
    return cts

#Bad, very slow.
def remove_link_by_city_v1(G, ct):
    deferred_removal = list()
    for edge in G.edges(keys=True, data="city"):
        n1_nid = edge[0].norm_id
        n2_nid = edge[1].norm_id
        key = edge[2]
        city = edge[3]
        if city == ct:
            deferred_removal.append((n1_nid, n2_nid, key))
    for n1_nid, n2_nid, key in deferred_removal:
        found = dict()
        for node in G.nodes:
            if node.norm_id == n1_nid:
                n1 = node
                found[n1_nid] = True
                continue
            elif node.norm_id == n2_nid:
                n2 = node
                found[n2_nid] = True
                continue
            if (n1_nid in found.keys()) and (n2_nid in found.keys()):
                G.remove_edge(n1, n2, key)
                break

#Defers node IDs and uses a lookup table to get index. Slow, bad.
def remove_link_by_city_lookup_index(G, ct, nid_to_ind):
    deferred_removal = list()
    for edge in G.edges(keys=True, data="city"):
        n1_nid = edge[0].norm_id
        n2_nid = edge[1].norm_id
        key = edge[2]
        city = edge[3]
        if city == ct:
            deferred_removal.append((n1_nid, n2_nid, key))
    for n1_nid, n2_nid, key in deferred_removal:
        ind1 = nid_to_ind[n1_nid]
        ind2 = nid_to_ind[n2_nid]
        G.remove_edge(list(G.nodes)[ind1], list(G.nodes)[ind2], key)

#Use lookup table to get node.
def remove_link_by_city_lookup(G, ct, nid_to_node):
    deferred_removal = list()
    for edge in G.edges(keys=True, data="city"):
        n1_nid = edge[0].norm_id
        n2_nid = edge[1].norm_id
        key = edge[2]
        city = edge[3]
        if city == ct:
            deferred_removal.append((n1_nid, n2_nid, key))
    for n1_nid, n2_nid, key in deferred_removal:
        G.remove_edge(nid_to_node[n1_nid], nid_to_node[n2_nid], key)

#Remove link by city (defers nodes)
def remove_link_by_city(G, ct):
    deferred_removal = list()
    for edge in G.edges(keys=True, data="city"):
        city = edge[3]
        if city == ct:
            n1 = edge[0]
            n2 = edge[1]
            key = edge[2]
            deferred_removal.append((n1, n2, key))
    for n1, n2, key in deferred_removal:
        G.remove_edge(n1, n2, key)

#Dont remove city if it was already removed
#NOTE: INIT
def remove_link_by_radius(G, ct, radius, distances, nid_to_node = False):
    cts = get_cities_within_radius(ct, radius, distances)
    cts.append(ct)#Append the main city too
    if not hasattr(G, "removed"):
        G.removed = dict()

    for city in cts:
        if not city in G.removed.keys():
            G.removed[city] = True
            if nid_to_node == False:
                remove_link_by_city(G, city)
            else:
                remove_link_by_city_lookup(G, city, nid_to_node)

#Approximate city
def approx_cities(G):
    for node in G.nodes:
        node.approx_city(G)

