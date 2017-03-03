# noinspection PyUnresolvedReferences
from iterate_over_json_file import execute_on_each_element
import re
import json
from gensim import corpora


dictionary = corpora.Dictionary.load("gensim_dictionary")

start_year = 2005
start_month = 12

end_year = 2008
end_month = 12

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
    } for date in file_dates
]

arguments = {"dictionary": dictionary, "doc_n":1, "output_file":open("./comments_term_document.dat", "w")}

def add_words_to_dictionary(comment, args):
    word_list = re.findall(r"[\w'-]+", comment["body"].lower())
    word_vector = args["dictionary"].doc2bow(word_list)

    for pair in word_vector:
        args["output_file"].write(str(args["doc_n"])+"\t"+str(pair[0])+"\t"+str(pair[1])+"\n")
    args["doc_n"] += 1

for file_pair in file_pairs:
    execute_on_each_element(file_pair["comments_file_path"], add_words_to_dictionary, arguments)

arguments["output_file"].close()
