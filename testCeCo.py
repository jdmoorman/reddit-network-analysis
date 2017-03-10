# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 16:10:28 2017

@author: the_p
"""

import CentralityAndCommunityAnalysis as CeCo
file1 = open("./testCeCoDeg.txt", "w")
file2 = open("./testCeCoBet.txt", "w")
partition=CeCo.CeCom(userProjG,file1,file2,True)
file1.close()
file2.close()

