# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:36:12 2019

@author: Brian
"""

from itertools import chain
import numpy as np

#https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
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

#https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
def draw_point(m, p, coord, style = 'o', color=[0, 0, 0], size = 1):
    x, y = m(coord[0],coord[1])
    p.plot(x, y, style, color=color, markersize=size)

def addtext(m, p, coord, text, color, size):
    x, y = m(coord[0],coord[1])
    p.text(x, y, '  '+text, color=color, fontsize=size);
    
#Draw a black and white map
def draw_map_simple(m):
    m.drawcoastlines(linewidth=1, linestyle='solid', color=[0.5,0.5,0.5])