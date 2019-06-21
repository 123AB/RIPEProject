# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:01:11 2019

@author: Brian
"""

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

#from visualizer.drawmap import *
#reload?
import visualizer.drawmap as vis
import datareader.reader as dr
import graph.graph_functions as gf
import graph.graph_metrics as gm

#Load graph data
G0 = dr.load_pkl("G0")
if G0 == False:
    graph_data_path = "data\\201603.as-rel-geo.txt"
    G0 = dr.load_graph_data(graph_data_path)
    gf.nid_to_node(G0)
    dr.save_pkl(G0, "G0")

#Load location data
loc_data_path = "data\\201603.locations.txt"
coords, cts = dr.load_loc_data(loc_data_path)

#Compute distances between cities
G0_distances = dr.load_pkl("G0_distances")
if G0_distances == False:
    G0_distances = dr.calculate_distances(coords, cts)
    dr.save_pkl(G0_distances, "G0_distances")

#Load biggest subgraph
G1 = dr.load_pkl("G1")
if G1 == False:
    G1 = gf.largest_subgraph(G0)
    gf.nid_to_node(G1)
    dr.save_pkl(G1, "G1")

#Dictionary to convert normalized ID number to list index
#norm_id_to_index_dict = dict()
#for i in range(len(list(G0.nodes))):
#    norm_id = list(G0.nodes)[i].norm_id
#    norm_id_to_index_dict[norm_id] = i

#id_in = 3
#index = norm_id_to_index_dict[id_in]
#id_out = list(G0.nodes)[index].norm_id

"""
G0_nid_to_ind = dict()
for i in range(len(list(G0.nodes))):
    norm_id = list(G0.nodes)[i].norm_id
    G0_nid_to_ind[norm_id] = i
    
G1_nid_to_ind = dict()
for i in range(len(list(G1.nodes))):
    norm_id = list(G1.nodes)[i].norm_id
    G1_nid_to_ind[norm_id] = i

G1_nid_to_node = dict()
for node in G1.nodes:
    G1_nid_to_node[node.norm_id] = node
"""

#Plot
#fig = plt.figure(figsize=(8, 6), edgecolor='w')
fig = plt.figure(figsize=(24, 18), edgecolor='w')
m = Basemap(projection='cyl', resolution=None, llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
vis.draw_map(m)

#Count number of links per city
ct_count = dict()
for edge in G0.edges(keys=True, data="city"):
    city = edge[3]
    if not city in ct_count.keys():
        ct_count[city] = 1
    else:
        ct_count[city] = ct_count[city] + 1

#Draw cities
top_20_eu = [
    "Frankfurt Am Main-05-DE",
    "London-ENG-UK",
    "Moscow-48-RU",
    "Kiev-12-UA",
    "Hoofddorp-07-NL",
    "Saint Petersburg-66-RU",
    "Paris-A8-FR",
    "Novosibirsk-53-RU",
    "Milano-09-IT",
    "Amsterdam-NH-NL",
    "Stockholm-26-SE",
    "Z_Rich-ZH-CH",
    "Vienna-09-AT",
    "Munich-02-DE",
    "Madrid-29-ES",
    "Warsaw-78-PL",
    "Moscow-MOW-RU",
    "Slough-ENG-UK",
    "Berlin-16-DE",
    "Prague-52-CZ",
]

highlight = False
for ct in cts:
    #vis.draw_point(m, plt, coords[ct], size = 1.5)
#    if ct_count[ct] > 1000 and highlight:
    if ct in top_20_eu:
        vis.draw_point(m, plt, coords[ct], style = 'ro', size = 1.5 + np.log(ct_count[ct]))
    else:
        vis.draw_point(m, plt, coords[ct], size = 1.5 + np.log(ct_count[ct]))

#Statistics
n_nodes = len(G0.nodes())
n_edges = len(G0.edges())
n_locs = len(cts)

print("Statistics:")
print("Number of AS: " + str(n_nodes))
print("Number of links: " + str(n_edges))
print("Number of locations: " + str(n_locs))

#dr.get_distance("Amsterdam-NH-NL", "New York City-NY-US", G2_distances)

#Save graph