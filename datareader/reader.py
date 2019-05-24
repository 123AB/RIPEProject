# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:47:44 2019

@author: Brian
"""

import networkx as nx

def load_graph_data(data_path):
    G = nx.MultiGraph()
    with open(data_path) as f:
        for x in f:
            content = x.strip()
            spl = content.split("|")
            node1 = int(spl.pop(0))
            node2 = int(spl.pop(0))
            
            for ed in spl:
                temp = ed.split(",")
                ct = temp[0]
                G.add_edge(node1, node2, city = ct)
    return G

def load_loc_data(data_path):
    coords = dict()
    cts = list()
    with open(data_path) as f:
        for x in f:
            content = x.strip()
            spl = content.split("|")
            ct = spl[0]
            lat = float(spl[5])
            lon = float(spl[6])
            cts.append(ct)
            coords[ct] = (lon, lat)
    return coords, cts