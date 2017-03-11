# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 13:13:21 2017

@author: the_p
"""

import networkx as nx
import numpy 
def histogramdegs2(G):
    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
    #print "Degree sequence", degree_sequence
    dmax=max(degree_sequence)
    print(dmax)
    numpy.histogram(degree_sequence)
    return True