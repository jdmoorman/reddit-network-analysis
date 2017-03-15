import construct_file_pairs
from iterate_over_json_file import execute_on_each_element
import re
import operator
import csv
import swear_word_set_getter

months = []
subreddits = []

for file_name in ["./output/comments_per_subreddit",
                  "./output/profane_comments_per_subreddit",
                  "./output/swears_per_subreddit",
                  "./output/words_per_subreddit"]:

    print(file_name)
    in_file = open(file_name+".csv", "r", newline="\n", encoding="utf-8")
    out_file = open(file_name+"_sparse.dat", "w", newline="\n", encoding="utf-8")
    reader = csv.reader(in_file)

    header = next(reader)
    columns = {elm:[] for elm in header}

    i = 0
    for row in reader:
        i += 1
        columns["month"] += [row[0]]

        for j in range(1, len(header)):
            columns[header[j]] += [row[j]]
            if row[j] != "0":
                # print(row[i])
                out_file.write(str(i)+"\t"+str(j)+"\t"+str(row[j])+"\n")
    if row[j] == "0":
        out_file.write(str(i)+"\t"+str(j)+"\t"+str(row[j])+"\n")

    months = columns["month"]
    subreddits = header[1:len(header)]

    in_file.close()
    out_file.close()

months_file = open("./output/months.csv", "w", newline="\n", encoding="utf-8")
for month in months:
    months_file.write(month+"\n")
months_file.close()

subreddits_file = open("./output/subreddits.csv", "w", newline="\n", encoding="utf-8")
for subreddit in subreddits:
    subreddits_file.write(subreddit+"\n")
subreddits_file.close()