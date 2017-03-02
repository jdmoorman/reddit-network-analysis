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
betwCent=nx.algorithms.centrality.betweenness_centrality(userProjG,weight='weight')
degreeCent=nx.algorithms.centrality.degree_centrality(userProjG)
#no weights, find how to do with weights
maximum = max(degreeCent, key=degreeCent.get)
print(maximum)
import operator
sorted_degreeCent = sorted(degreeCent.items(), key=operator.itemgetter(1),reverse=True)
sorted_betwCent=sorted(betwCent.items(),key=operator.itemgetter(1),reverse=True)
for i in range(10):
    print(sorted_degreeCent[i])
file = open("./sortresultsdegreeCent.txt", "w")
file.write("degreeCent\n")

for i in  range(100):
    s = str(sorted_degreeCent[i])
    file.write(s)
    file.write("\n")
file.close()
file = open("./sortresultsbetwCent.txt", "w")
file.write("betweenness_cent\n")
for i in range(100):
    s=str(sorted_betwCent[i])
    file.write(s)
    file.write("\n")
file.close()
import community
import matplotlib.pyplot as plt
partition = community.best_partition(userProjG)
size = float(len(set(partition.values())))
pos = nx.spring_layout(userProjG)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(userProjG, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()
