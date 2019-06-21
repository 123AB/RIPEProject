# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:42:56 2019

@author: Brian
"""

import networkx as nx
import numpy as np

#https://www.tutorialsteacher.com/python/private-and-protected-access-modifiers-in-python
class Node:
    def __init__(self, node_id: int):
        self.id = node_id
        self.norm_id = None
        self.approx_ct = None
        self.conf = None
    
    #Sample function
    def print_id(self):
        print(self.id)

    #Set normalized ID
    def set_norm_id(self, normalized_id):
        self.norm_id = normalized_id
    
    #Approximate City
    def approx_city(self, G):
        neighbors = G.neighbors(self)
        ct_dict = dict()
        for neighbor in neighbors:
            for n, (k, v) in enumerate(G[self][neighbor].items()):
                ct = v["city"]
                if not ct in ct_dict.keys():
                    ct_dict[ct] = 1
                else:
                    ct_dict[ct] = ct_dict[ct] + 1
        ct_list = list()
        ct_count = list()
        for n, (k, v) in enumerate(ct_dict.items()):
            ct_list.append(k)
            ct_count.append(v)

        #Sort by Count
        stack_names = np.column_stack((ct_list,))
        stack_count = np.column_stack((ct_count,))
        ind=np.argsort(-stack_count[:,0])
        stack_names = stack_names[ind]
        stack_count = stack_count[ind]
#        components = list(stacked[:,0])

        self.approx_ct = stack_names[0,0]
        self.conf = stack_count[0,0] / (np.sum(stack_count[:,0]) + 1)