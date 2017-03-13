# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:26:37 2017

@author: the_p
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:38:38 2017

@author: the_p
"""

#import MultiGraphToWeighted
import bipartite_graphshyp
#from networkx.algorithms import bipartite
import CentralityAndCommunityAnalysis as CeCoA
import construct_file_pairs
import networkx as nx
import hDe
#import matplotlib.pyplot as plt


print("hello world")
file_pairs = construct_file_pairs.file_pairs_from_date_range(1,2009,1,2009)
print("goodbye world")

bipartite_swear =  bipartite_graphshyp.get_swear_count_weighted_bipartite_graph_from_files(file_pairs)
bipartite_comments=bipartite_graphshyp.get_comment_count_weighted_bipartite_graph_from_files(file_pairs)
#bipartitewithout subreddit: bipSansRedd
bipSansRedd=bipartite_comments.copy()
bipSwearSansRedd=bipartite_swear.copy()
threadSubReddit1=nx.get_node_attributes(bipartite_swear,'subreddit')
for thread in threadSubReddit1:
    if ((threadSubReddit1[thread]=='reddit.com')or (threadSubReddit1[thread]=='programming')):
        bipSwearSansRedd.remove_node(thread)
        
 #for the general comment graph       
threadSubReddit1=nx.get_node_attributes(bipartite_swear,'subreddit')
for thread in threadSubReddit1:
    if ((threadSubReddit1[thread]=='reddit.com')or (threadSubReddit1[thread]=='programming')):
        bipSansRedd.remove_node(thread)
#



#Unigraph = max(nx.connected_component_subgraphs(bipartite_graph), key=len)
# repeat without reddit.com
Unigraph= max(nx.connected_component_subgraphs(bipartite_swear), key=len)
UnigraphSans = max(nx.connected_component_subgraphs(bipSwearSansRedd), key=len)
Unigraphcomments= max(nx.connected_component_subgraphs(bipartite_comments), key=len)
UnigraphcommentsSans= max(nx.connected_component_subgraphs(bipSansRedd), key=len)

print("bipartite graph(not restricted to swear graph")
print("largest connected component with reddit.com: ", len(Unigraphcomments))
print("largest connected component WITHOUT reddit.com: ", len(UnigraphcommentsSans))

print("Swear bipartite graphs")
print("largest connected component with reddit.com: ", len(Unigraph))
print("full graph: ", len(bipartite_swear))
print("largest connected component WITHOUT reddit.com: ", len(UnigraphSans))


[author,threads] = bipartite_graphshyp.get_author_and_thread_nodes(Unigraph)


#weighted grap
threadProjG= bipartite_graphshyp.projected_graph(Unigraph, threads, bipartite_graphshyp.weight_by_sum_of_weights_above_thresh)
Unithread = max(nx.connected_component_subgraphs(threadProjG), key=len)
file1 = open("./ProjThreadMaxThresDegreeCentrality.txt", "w")
file2 = open("./ProjThreadMaxThresBetweennessCentrality.txt", "w")
#threadPartition=CeCo.CeCom(threadProjG,file1,file2,plotval=True)
print("projection Completed")
#partition = community.best_partition(G)
threadPartition=CeCoA.CeCom(Unithread,file1,file2,False)
print("partition Completed")
#get subreddit dictionary
#bipartite_graph changed to bipartite_swear
threadSubReddit=nx.get_node_attributes(bipartite_swear,'subreddit')

#Hi Guys!!!!!!!!!!!!!
#possible communities
commVals=set(threadPartition.values())
#initialize empty CommDist, at the end get dictionary where {CommDist[i]} gives the
# subreddit frequencies in that given communities

#threads in the maximal connected component of projected graph
threadsMax=Unithread.nodes()
CommDist={k:{} for k in commVals}
subredditFreq={k:0 for k in set(threadSubReddit.values())}
for nodethread in threadsMax:
    nodeSubR=threadSubReddit[nodethread]
    subredditFreq[nodeSubR]+=1
for nodethread in threadsMax:
    currPartVal=threadPartition[nodethread]
    #current partition
    nodeSubR=threadSubReddit[nodethread]
    if threadSubReddit[nodethread] not in CommDist[currPartVal]:
        CommDist[currPartVal][threadSubReddit[nodethread]]=1
    else:
        CommDist[currPartVal][threadSubReddit[nodethread]]+=1
        #prints degree histogram
hDe.histogramdegs2(Unithread)
