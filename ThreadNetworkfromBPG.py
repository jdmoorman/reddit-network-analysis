# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:38:38 2017

@author: the_p
"""

#import MultiGraphToWeighted
import bipartite_graphs
#from networkx.algorithms import bipartite
import CentralityAndCommunityAnalysis as CeCoA
import community
import construct_file_pairs
import networkx as nx

print("hello world")
file_pairs = construct_file_pairs.file_pairs_from_date_range(12,2005,11,2006)
print("goodbye world")

bipartite_graph = bipartite_graphs.get_comment_count_weighted_bipartite_graph_from_files(file_pairs)

Unigraph = max(nx.connected_component_subgraphs(bipartite_graph), key=len)

print("largest connected component: ", len(Unigraph))
print("full graph: ", len(bipartite_graph))

[author,threads] = bipartite_graphs.get_author_and_thread_nodes(Unigraph)


#weighted grap
threadProjG= bipartite_graphs.projected_graph(Unigraph, threads, bipartite_graphs.weight_by_sum_of_weights_above_thresh)
Unithread = max(nx.connected_component_subgraphs(threadProjG), key=len)
file1 = open("./ProjThreadMaxThresDegreeCentrality.txt", "w")
file2 = open("./ProjThreadMaxThresBetweennessCentrality.txt", "w")
#threadPartition=CeCo.CeCom(threadProjG,file1,file2,plotval=True)
print("projection Completed")
#partition = community.best_partition(G)
threadPartition=CeCoA.CeCom(Unithread,file1,file2,False)
#get subreddit dictionary
#Hi Guys!!!!!!!!!!!!!
threadSubReddit=nx.get_node_attributes(bipartite_graph,'subreddit')
#possible communities
commVals=set(threadPartition.values())
#initialize empty CommDist, at the end get dictionary where {CommDist[i]} gives the
# subreddit frequencies in that given communities
CommDist={k:{} for k in commVals}
for nodethread in threads:
    currPartVal=threadPartition[nodethread]#current partition
    if threadSubReddit[nodethread] not in CommDist[currPartVal]:
        CommDist[currPartVal][threadSubReddit[nodethread]]=1
    else:
        CommDist[currPartVal][threadSubReddit[nodethread]]
        


