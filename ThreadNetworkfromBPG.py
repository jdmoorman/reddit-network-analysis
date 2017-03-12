# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:38:38 2017

@author: the_p
"""

#import MultiGraphToWeighted
import bipartite_graphshyp
#from networkx.algorithms import bipartite
import CentralityAndCommunityAnalysis as CeCoA
import community
import construct_file_pairs
import networkx as nx
import hDe
import matplotlib.pyplot as plt


print("hello world")
file_pairs = construct_file_pairs.file_pairs_from_date_range(1,2009,1,2009)
print("goodbye world")

bipartite_graph = bipartite_graphshyp.get_comment_count_weighted_bipartite_graph_from_files(file_pairs)
#bipartitewithout subreddit: bipSansRedd
bipSansRedd=bipartite_graph
#threadSubReddit1=nx.get_node_attributes(bipartite_graph,'subreddit')
#for thread in threadSubReddit1:
#    if ((threadSubReddit1[thread]=='reddit.com')or (threadSubReddit1[thread]=='programming')):
#        bipSansRedd.remove_node(thread)

#Unigraph = max(nx.connected_component_subgraphs(bipartite_graph), key=len)
# repeat without reddit.com
Unigraph = max(nx.connected_component_subgraphs(bipSansRedd), key=len)

print("largest connected component: ", len(Unigraph))
print("full graph: ", len(bipartite_graph))

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
threadSubReddit=nx.get_node_attributes(bipartite_graph,'subreddit')

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
#experiment with single pie chart, with legend
#fig = plt.figure()
#p1=fig.add_subplot(1,1,1)
#lvalues=[]
#lkey=[]
#for key in CommDist[0]:
#        lkey.append(key)
#        lvalues.append(CommDist[0][key])
#p1.pie(lvalues)
#p1.legend(lkey,loc=2,bbox_to_anchor=(1, 1))
#fig.show()
#experiment ended


#for k in range(0,4):
#    p1 = fig.add_subplot(2,2,k+1)
#    lvalues=[]
#    lkey=[]
#    for key in CommDist[k]:
#        lkey.append(key)
#        lvalues.append(CommDist[k][key])
#    p1.pie(lvalues)
#    p1.legend(lkey,loc="lower left")

#fig.savefig("pies.png")
#fig.show()

        


