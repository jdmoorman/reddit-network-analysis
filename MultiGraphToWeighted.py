# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 15:15:14 2017

@author: the_p
"""

import networkx as nx
def MultToW(M):

    # create weighted graph from M
    G = nx.Graph()
    for u,v,data in M.edges_iter(data=True):
        w = data['weight'] if 'weight' in data else 1.0
        if G.has_edge(u,v):
            G[u][v]['weight'] += w
        else:
            G.add_edge(u, v, weight=w)
    return G