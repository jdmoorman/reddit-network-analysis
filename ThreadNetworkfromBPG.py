# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:38:38 2017

@author: the_p
"""

import MultiGraphToWeighted
import bipartite_graphs
from networkx.algorithms import bipartite
import CentralityAndCommunityAnalysis as CeCo
import construct_file_pairs
import networkx as nx

print("hello world")
file_pairs = construct_file_pairs.file_pairs_from_date_range(12,2005,12,2006)
print("goodbye world")

bipartite_graph = bipartite_graphs.get_comment_count_weighted_bipartite_graph_from_files(file_pairs)

x = max(nx.connected_component_subgraphs(bipartite_graph), key=len)


print("largest connected component: ", len(x))
print("full graph: ", len(bipartite_graph))

# [author,threads]=bipartite_graphs.get_author_and_thread_nodes(x)
# Unigraph=MultiGraphToWeighted.MultToW(x)


#weighted grap
# threadProjG= bipartite.projected_graph(Unigraph,threads)
#file1 = open("./threadDegreeCentrality.txt", "w")
#file2 = open("./threadBetweennessCentrality.txt", "w")
#threadPartition=CeCoA.CeCom(threadProjG,file1,file2,plotval=False)



#threadPartition=CeCoA.CeCom(threadProjG,file1,file2,True)

