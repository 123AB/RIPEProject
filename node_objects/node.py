# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:42:56 2019

@author: Brian
"""

import networkx as nx
import numpy as np

class Node:
    def __init__(self, id: int):
        self.id = id
    
    #Sample function
    def print_id(self):
        print(self.id)
