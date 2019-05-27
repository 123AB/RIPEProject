# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:47:44 2019

@author: Brian
"""

import networkx as nx
from node_objects.node import Node

import pickle
import os
local_data_path = os.path.dirname(os.path.realpath(__file__)) + "\\pkls\\"

import numpy as np

#Load graph data from text file and create a graph.
def load_graph_data(data_path):
    G = nx.MultiGraph()
    #Dictionary for tracking whether a node has already been seen
    seen = dict()
    
    with open(data_path) as f:
        for x in f:
            #Read line, strip newline, split on vertical bar "|"
            content = x.strip()
            line_spl = content.split("|")
            
            #Pop node1 ID. If ID has not been seen, add to dictionary and make new node.
            #Otherwise find the node in the graph with the matching ID.
            n1_id = int(line_spl.pop(0))
            if not n1_id in seen.keys():
                seen[n1_id] = True
                node1 = Node(n1_id)
            else:
                for node in G.nodes():
                    if node.id == n1_id:
                        node1 = node
                        break
            
            #Pop node2 ID and repeat.
            n2_id = int(line_spl.pop(0))
            if not n2_id in seen.keys():
                seen[n2_id] = True
                node2 = Node(n2_id)
            else:
                for node in G.nodes():
                    if node.id == n2_id:
                        node2 = node
                        break
            
            #The remaining entries are links. Loop over the links.
            #Split each link on comma ",". The first element is the name of the city.
            #Add an edge between node1 and node2 and set the city as the attribute of the edge.
            for link in line_spl:
                link_spl = link.split(",")
                ct = link_spl[0]
                G.add_edge(node1, node2, city = ct)
    return G

#Load graph data using integers as nodes.
#Nodes are integers so there is no need to check if a node exists already.
def load_graph_data_legacy(data_path):
    G = nx.MultiGraph()
    with open(data_path) as f:
        for x in f:
            #Read line, strip newline, split on vertical bar "|"
            content = x.strip()
            line_spl = content.split("|")
            
            #First two entries are nodes. Pop them and cast to integer.
            node1 = int(line_spl.pop(0))
            node2 = int(line_spl.pop(0))
            
            #The remaining entries are links. Loop over the links.
            #Split each link on comma ",". The first element is the name of the city.
            #Add an edge between node1 and node2 and set the city name as the attribute of the edge.
            for link in line_spl:
                link_spl = link.split(",")
                ct = link_spl[0]
                G.add_edge(node1, node2, city = ct)
    return G

#Load location data from text file and create a coordinate dictionary/city list.
def load_loc_data(data_path):
    coords = dict()
    cts = list()
    
    with open(data_path) as f:
        for x in f:
            #Read line, strip newline, split on vertical bar "|"
            content = x.strip()
            line_spl = content.split("|")
            
            #City is element 0
            ct = line_spl[0]
            
            #Latitide and longitude are element 5 and 6 respectively.
            lat = float(line_spl[5])
            lon = float(line_spl[6])
            
            #Append city and coordinates.
            cts.append(ct)
            coords[ct] = (lon, lat)
    return coords, cts

#Calculate distances
def calculate_distances(coords, cts):
    city_distances = dict()
    for i1 in range(len(cts)-1):
        for i2 in range(i1+1, len(cts)):
            ct1 = cts[i1]
            ct2 = cts[i2]
            city_distances[ct1, ct2] = haversine_km(coords[ct1], coords[ct2])
    return city_distances

#Haversine distance calculation. Returns answer in kilometers.
#https://www.movable-type.co.uk/scripts/latlong.html
#https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def haversine_km(coords_1, coords_2):
    R = 6371e3
    d_lon = np.radians(coords_2[0] - coords_1[0])
    d_lat = np.radians(coords_2[1] - coords_1[1])
    lat_1 = np.radians(coords_1[1])
    lat_2 = np.radians(coords_2[1])
    a = np.sin(d_lat/2)**2 + np.cos(lat_1)*np.cos(lat_2)*np.sin(d_lon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R*c
    return d/1000

#Get distance from dictionary
def get_distance(ct1, ct2, distances):
    if (ct1, ct2) in distances.keys():
        return distances[ct1, ct2]
    elif (ct2, ct1) in distances.keys():
        return distances[ct2, ct1]
    else:
        print("Error: distance not found.")
        return 0

#Serialize graph object to binary data
#Note: make sure pkls folder exists
#https://stackoverflow.com/questions/38233515/pickle-file-import-error?rq=1
def save_graph(graph, name: str):
    file_location = '{}{}.pkl'.format(local_data_path, name)
    with open(file_location, 'wb') as output:
        pickle.dump(graph, output, pickle.HIGHEST_PROTOCOL)
    print("Graph saved to {}".format(file_location))

#Load graph from file
def reload_graph(name: str):
    file_location = '{}{}.pkl'.format(local_data_path, name)
    try:
        with open(file_location, 'rb') as input:
            graph = pickle.load(input)
            print("Loaded graph from {}".format(file_location))
    except FileNotFoundError:
        print("File not found: {}".format(file_location))
        return False
    return graph
