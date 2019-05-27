# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:42:56 2019

@author: Brian
"""

import networkx as nx
import numpy as np

class Node:
    def __init__(self, node_id: int):
        self.id = node_id
    
    #Sample function
    def print_id(self):
        print(self.id)
