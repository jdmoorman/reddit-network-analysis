# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 13:13:59 2017

@author: the_p
"""


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
 
def histogramdegs2(G):

    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
    bins = np.arange(0, max(degree_sequence), 1)
    # fixed bin size
    plt.xlim([min(degree_sequence)-5, max(degree_sequence)+5])

    plt.hist(degree_sequence, bins=bins, alpha=0.5)

    #print "Degree sequence", degree_sequence
    plt.hist(degree_sequence)
    plt.show
    return True