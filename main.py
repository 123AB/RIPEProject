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
import simulation as sim

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

#Count number of links per city
ct_count = dict()
for edge in G0.edges(keys=True, data="city"):
    city = edge[3]
    if not city in ct_count.keys():
        ct_count[city] = 1
    else:
        ct_count[city] = ct_count[city] + 1

#Biggest European Cities
top_20_eu = [
    "Frankfurt Am Main-05-DE",
    "London-ENG-UK",
    "Moscow-48-RU",
    "Kiev-12-UA",
    "Hoofddorp-07-NL",
    "Saint Petersburg-66-RU",
    "Paris-A8-FR",
#    "Novosibirsk-53-RU",
    "Milano-09-IT",
    "Amsterdam-NH-NL",
    "Stockholm-26-SE",
#    "Z_Rich-ZH-CH",
#    "Vienna-09-AT",
#    "Munich-02-DE",
#    "Madrid-29-ES",
#    "Warsaw-78-PL",
#    "Moscow-MOW-RU",
#    "Slough-ENG-UK",
#    "Berlin-16-DE",
#    "Prague-52-CZ",
]

text = True
highlight = [
    "Frankfurt Am Main-05-DE",
    "San Juan-127-PR",
    "Tokyo-13-JP",
    "Moscow-48-RU",
    "Novosibirsk-53-RU"
]

#highlight = top_20_eu
#highlight = []

#1 on, 0 off
sizeadd = 1

#http://math.loyola.edu/~loberbro/matlab/html/colorsInMatlab.html
#hlc = [0, 0.4470, 0.7410]
hlc = [0.8500, 0.3250, 0.0980]

#Plot Relief
#fig = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution=None, llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
vis.draw_map(m)

#First pass normal, second pass highlight
for ct in cts:
    if not ct in highlight:
        vis.draw_point(m, plt, coords[ct], size = 1.5 + sizeadd*np.log(ct_count[ct]))

for ct in highlight:
    vis.draw_point(m, plt, coords[ct], color=hlc, size = 1.5 + sizeadd*np.log(ct_count[ct]))

if text:
    for ct in highlight:
        temp = ct.split('-')
        temp.pop(-1)
        temp.pop(-1)
        temp = "-".join(temp)
        vis.addtext(m, plt, coords[ct], temp, hlc, 8)

#Simple Map
plt.figure()
m2 = Basemap(projection='cyl', resolution='l', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)
vis.draw_map_simple(m2)

#First pass normal, second pass highlight
for ct in cts:
    if not ct in highlight:
        vis.draw_point(m2, plt, coords[ct], size = 1.5 + sizeadd*np.log(ct_count[ct]))

for ct in highlight:
    vis.draw_point(m2, plt, coords[ct], color=hlc, size = 1.5 + sizeadd*np.log(ct_count[ct]))

if text:
    for ct in highlight:
        temp = ct.split('-')
        temp.pop(-1)
        temp.pop(-1)
        temp = "-".join(temp)
        vis.addtext(m, plt, coords[ct], temp, hlc, 8)

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