# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 13:33:58 2017

@author: the_p
"""
import csv
import itertools
#od = collections.OrderedDict(sorted(CommDist.items()))
def mergedict(a,b):
    a.update(b)
    return a

f=open('SubredditbyCommunity2009.csv','w+')
#CommDistList=[]
#for key in od:
#    CommDistList.append(od[key])
#w=csv.DictWriter(f,od.keys())
#w.writerows(od)
#f.close()
fields = [ 'Community number' ]
fields.extend(list(set(threadSubReddit.values())))
print(fields)
w = csv.DictWriter( f, fields )
w.writeheader()
for k,d in sorted(CommDist.items()):
        w.writerow(mergedict({'Community number': k},d))
f.close()
        