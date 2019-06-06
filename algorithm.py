# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:48:15 2019

@author: 14496
"""
import networkx as nx

def checkSpread(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

"""
def shorestPath(G, initial):
      visited = {initial: 0}
      path = {}

      nodes = set(G.nodes)

      while nodes: 
          min_node = None
          for node in nodes:
              if node in visited:
                  if min_node is None:
                      min_node = node
                  elif visited[node] < visited[min_node]:
                          min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in G.edges[min_node]:
            weight = current_weight + G.distance[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node
    return visited, path
"""

def clustering_coefficient(G, node):
    CC = nx.clustering(G,node)
    return CC
