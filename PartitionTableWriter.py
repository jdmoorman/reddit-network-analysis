# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:25:41 2017

@author: the_p
"""

import csv
import itertools
#od = collections.OrderedDict(sorted(CommDist.items()))
def mergedict(a,b):
    a.update(b)
    return a
def CommuSubRedFreq_Csv(file,CommDist):
    fields = [ 'Community number' ]
    setsubreddits=set()
    for k in CommDist:
        setsubreddits=setsubreddits|set(CommDist[k].keys())
    fields.extend(list(setsubreddits))
    w = csv.DictWriter( file, fields )
    w.writeheader()
    for k,d in sorted(CommDist.items()):
        w.writerow(mergedict({'Community number': k},d))
    return True