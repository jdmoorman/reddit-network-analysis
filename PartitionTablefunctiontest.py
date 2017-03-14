# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:26:22 2017

@author: the_p
"""

import PartitionTableWriter as ptabW
f=open('SubredditbyCommunitywithoutRed06.csv','w+')
ptabW.CommuSubRedFreq_Csv(f,CommDist)
f.close()