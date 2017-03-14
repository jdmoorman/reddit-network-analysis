# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 15:48:39 2017

@author: the_p
"""
import networkx as nx
import community
import operator
import matplotlib.pyplot as plt

#creates degree and betweenness centrality of graph G,
#stores 100 top values of both in file1,file2
#and returns best partition of G
def CeCom(G,file1,file2,plotval=False,cent=False):  
    if cent==True:
        betwCent=nx.algorithms.centrality.betweenness_centrality(G)
        degreeCent=nx.algorithms.centrality.degree_centrality(G)
        sorted_degreeCent = sorted(degreeCent.items(), key=operator.itemgetter(1),reverse=True)
        #sorted_betwCent=sorted(betwCent.items(),key=operator.itemgetter(1),reverse=True)
        file1.write("degreeCent\n")
        for i in  range(100):
            s = str(sorted_degreeCent[i])
            file1.write(s)
            file1.write("\n")
        file2.write("betweenness_cent\n")
        #for i in range(100):
        #    s=str(sorted_betwCent[i])
        #    file2.write(s)
        #    file2.write("\n")
    partition = community.best_partition(G)
    if plotval==True:
        size = float(len(set(partition.values())))
        pos = nx.spring_layout(G)
        count = 0.
        for com in set(partition.values()) :
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys()if partition[nodes] == com]
            nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,node_color = str(count / size))
        nx.draw_networkx_edges(G,pos, alpha=0.5)
        plt.show()
    return partition


    