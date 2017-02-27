# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 14:02:17 2017

@author: the_p
"""
import networkx as nx
import MultiGraphToWeighted
x=largest_component
import bipartite_graphs
[author,threads]=bipartite_graphs.get_author_and_thread_nodes(x)
Unigraph=MultiGraphToWeighted.MultToW(x)
#weighted grap
from networkx.algorithms import bipartite
userProjG= bipartite.projected_graph(Unigraph,author)
#nx.algorithms.centrality.betweenness_centrality(userProjG,weight='weight')
degreeCent=nx.algorithms.centrality.degree_centrality(userProjG)
#no weights, find how to do with weights
maximum = max(degreeCent, key=degreeCent.get)
print(maximum)