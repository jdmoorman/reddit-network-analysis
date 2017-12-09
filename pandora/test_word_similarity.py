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
end_month = 1

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

# Term document matrices for comments and threads
arguments = {
    "dictionary": dictionary,
    "comment_n": 1,
    "comment_td_file": open("./comments_term_document.dat", "w"),
    "thread_map": {}
}

def add_words_to_td_matrices(comment, args):
    word_list = re.findall(r"[\w'-]+", comment["body"].lower())
    word_vector = args["dictionary"].doc2bow(word_list)

    for pair in word_vector:
        args["comment_td_file"].write(str(args["comment_n"])+"\t"+str(pair[0])+"\t"+str(pair[1])+"\n")
    args["comment_n"] += 1

    if comment["link_id"] not in args["thread_map"]:
        args["thread_map"][comment["link_id"]] = {}

    for pair in word_vector:
        if pair[0] not in args["thread_map"][comment["link_id"]]:
            args["thread_map"][comment["link_id"]][pair[0]] = pair[1]
        else:
            args["thread_map"][comment["link_id"]][pair[0]] += pair[1]

thread_td_file = open("./threads_term_document.dat", 'w')
thread_n = 1


for file_pair in file_pairs:
    print(file_pair)
    execute_on_each_element(file_pair["comments_file_path"], add_words_to_td_matrices, arguments)
    for thread in arguments["thread_map"]:
        for word_key in arguments["thread_map"][thread]:
            thread_td_file.write(str(thread_n)+"\t"+str(word_key)+"\t"+str(arguments["thread_map"][thread][word_key])+"\n")
        thread_n += 1
    arguments["thread_map"] = {}

print(thread_n)

thread_td_file.close()
arguments["comment_td_file"].close()
