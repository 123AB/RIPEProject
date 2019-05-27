# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:01:11 2019

@author: Brian
"""

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#from visualizer.drawmap import *
#reload?
import visualizer.drawmap as vis
import datareader.reader as dr

#Load graph data
G2 = dr.reload_graph("G2")
if G2 == False:
    graph_data_path = "data\\201603.as-rel-geo.txt"
    G2 = dr.load_graph_data(graph_data_path)

#Load location data
loc_data_path = "data\\201603.locations.txt"
coords, cts = dr.load_loc_data(loc_data_path)


#Plot
fig = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution=None, llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
vis.draw_map(m)

#Draw cities
for ct in cts:
    vis.draw_point(m, plt, coords[ct])

#Statistics
n_nodes = len(G2.nodes())
n_edges = len(G2.edges())
n_locs = len(cts)

print("Statistics:")
print("Number of AS: " + str(n_nodes))
print("Number of links: " + str(n_edges))
print("Number of locations: " + str(n_locs))

#Save graph
dr.save_graph(G2, "G2")