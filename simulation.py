# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 20:11:06 2019

@author: Brian
"""

import datareader.reader as dr
import graph.graph_functions as gf
import graph.graph_metrics as gm

def remove_cities(G: str, cts: list):
    #Load graph
    #Remove city
    #Save Metrics
    #Repeat
    pass

#Big radius
#sim_dist, sim_size = disaster_radius_large("G1", G0_distances, "Frankfurt Am Main-05-DE")
#sim_dist, sim_size, sim_links, sim_cc, sim_hc = disaster_radius_large("G1", G0_distances, "Frankfurt Am Main-05-DE")
#sim_dist, sim_size, sim_links, sim_hc = disaster_radius_large("G1", G0_distances, "Frankfurt Am Main-05-DE")
def disaster_radius_large(G_str, G_distances, rem_cit):
    G_temp = dr.load_pkl(G_str)

    print(rem_cit)
    out = list()

    a, b = gf.components_distribution(G_temp)
    c_rad = -1
    c_size= a[-1]
    c_links = len(G_temp.edges)
    del G_temp.hop_count
    ss = 1000
    c_hc = gm.hop_count(G_temp, sample_size = ss)
    out.append((c_rad, c_size, c_links, c_hc))
    
    for i in range(0, 2000, 50):
        gf.remove_link_by_radius(G_temp, rem_cit, i, G_distances)
        a, b = gf.components_distribution(G_temp)
        c_rad = i
        c_size= a[-1]
        c_links = len(G_temp.edges)
        del G_temp.hop_count
        c_hc = gm.hop_count(G_temp, sample_size = ss)
        out.append((c_rad, c_size, c_links, c_hc))
        print(i)
        
    for i in range(2000, 30000, 1000):
        gf.remove_link_by_radius(G_temp, rem_cit, i, G_distances)
        a, b = gf.components_distribution(G_temp)
        c_rad = i
        c_size= a[-1]
        c_links = len(G_temp.edges)
        del G_temp.hop_count
        c_hc = gm.hop_count(G_temp, sample_size = ss)
        out.append((c_rad, c_size, c_links, c_hc))
        print(i)
        
        if a[-1] == 1:
            break
    
    return out