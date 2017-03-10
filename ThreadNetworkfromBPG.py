# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:38:38 2017

@author: the_p
"""

import MultiGraphToWeighted
import bipartite_graphs
from networkx.algorithms import bipartite
import CentralityAndCommunityAnalysis as CeCoA

x=largest_component
[author,threads]=bipartite_graphs.get_author_and_thread_nodes(x)
Unigraph=MultiGraphToWeighted.MultToW(x)
#weighted grap
threadProjG= bipartite.projected_graph(Unigraph,threads)
#file1 = open("./threadDegreeCentrality.txt", "w")
#file2 = open("./threadBetweennessCentrality.txt", "w")
#threadPartition=CeCoA.CeCom(threadProjG,file1,file2,plotval=False)



#threadPartition=CeCoA.CeCom(threadProjG,file1,file2,True)

