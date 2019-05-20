# -*- coding: utf-8 -*-
"""
Created on Mon May 20 16:01:11 2019

@author: Brian
"""

import networkx as nx

#Load graph data
graph_data_path = "data\\201603.as-rel-geo.txt"

G2 = nx.MultiGraph()

with open(graph_data_path) as f:
    for x in f:
        content = x.strip()
        spl = content.split("|")
        node1 = spl.pop(0)
        node2 = spl.pop(0)
        
        for ed in spl:
            temp = ed.split(",")
            ct = temp[0]
            G2.add_edge(node1, node2, city = ct)

#Load location data
loc_data_path = "data\\201603.locations.txt"
coords = dict()
cts = list()

with open(loc_data_path) as f:
    for x in f:
        content = x.strip()
        spl = content.split("|")
        ct = spl[0]
        lat = float(spl[5])
        lon = float(spl[6])
        cts.append(ct)
        coords[ct] = (lon, lat)

#Basemap
#https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html

from itertools import chain
import numpy as np

def draw_map(m, scale=0.2):
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)
    
    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution=None, llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, )
draw_map(m)

#Draw cities
for ct in cts:
    x, y = m(coords[ct][0],coords[ct][1])
    plt.plot(x, y, 'ok', markersize=1)
