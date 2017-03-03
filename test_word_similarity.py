# noinspection PyUnresolvedReferences
from iterate_over_json_file import execute_on_each_element
import re
import json
from gensim import corpora
import networkx as nx
import get_thread_trees


dictionary = corpora.Dictionary.load("gensim_dictionary")

start_year = 2005
start_month = 12

end_year = 2006
end_month = 5

year = start_year
month = start_month

file_dates = []

while year*100+month <= 100*end_year+end_month:
    file_date = str(year)+"-"+"0"*(2-len(str(month)))+str(month)
    file_dates.append(file_date)
    month += 1
    if month > 12:
        month = 1
        year += 1

file_pairs = [
    {
        "comments_file_path": "./comments/RC_" + date + ".json",
        "threads_file_path": "./submissions/RS_" + date + ".json"
    } for date in file_dates
]

# Term document matrix for threads as documents
# # Optionally pass a string argument with the subreddit into get_thread_trees
# thread_map = get_thread_trees.get_thread_trees(file_pairs)
#
# doc_n = 1
# output_file = open("./threads_term_document.dat", "w")
#
# for head in sorted(thread_map):
#     assert(nx.is_forest(thread_map[head]))
#     thread_string = ""
#     for node, data in thread_map[head].nodes_iter(data=True):
#         thread_string += " " + data["body"]
#     words_in_thread = re.findall(r"[\w'-]+", thread_string.lower())
#     word_vector = dictionary.doc2bow(words_in_thread)
#     for pair in word_vector:
#         output_file.write(str(doc_n)+"\t"+str(pair[0])+"\t"+str(pair[1])+"\n")
#         print(str(doc_n)+"\t"+str(pair[0])+"\t"+str(pair[1])+"\n")

# Term document matrix for comments as documents
# arguments = {"dictionary": dictionary, "doc_n":1, "output_file":open("./comments_term_document.dat", "w")}
#
# def add_words_to_dictionary(comment, args):
#     word_list = re.findall(r"[\w'-]+", comment["body"].lower())
#     word_vector = args["dictionary"].doc2bow(word_list)
#
#     for pair in word_vector:
#         args["output_file"].write(str(args["doc_n"])+"\t"+str(pair[0])+"\t"+str(pair[1])+"\n")
#     args["doc_n"] += 1
#
# for file_pair in file_pairs:
#     execute_on_each_element(file_pair["comments_file_path"], add_words_to_dictionary, arguments)
#
# arguments["output_file"].close()
