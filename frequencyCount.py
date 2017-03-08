# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 18:23:14 2017

@author: the_p
"""
import re
import networkx as nx
from gensim import corpora
def freqCount(thread_map):
    dictionary = corpora.Dictionary.load("gensim_dictionary")
    maptofreq=dict()
    for head in sorted(thread_map):
        assert(nx.is_forest(thread_map[head]))
        thread_string = ""
        for node, data in thread_map[head].nodes_iter(data=True):
            thread_string += " " + data["body"]
        words_in_thread = re.findall(r"[\w'-]+", thread_string.lower())
        word_vector = dictionary.doc2bow(words_in_thread)
        maptofreq[head]=word_vector
    return maptofreq
