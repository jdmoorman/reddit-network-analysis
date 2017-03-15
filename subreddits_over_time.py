import construct_file_pairs
from iterate_over_json_file import execute_on_each_element
import re
import operator
import csv
import swear_word_set_getter

file_pairs = construct_file_pairs.file_pairs_from_date_range(12,2005,12,2010)
swear_word_map = {swear:0 for swear in swear_word_set_getter.get_swear_word_set()}

arguments = {
    "swears": swear_word_map,
    "subreddits": {},
    "over_time": {}
}


def experiment(comment, args):
    subreddit = comment["subreddit"]
    subreddits = args["subreddits"]

    if subreddit not in subreddits:
        subreddits[subreddit] = {
            "comments": 0,
            "profane_comments": 0,
            "swears": 0,
            "words": 0
        }

    word_list = re.findall(r"[\w'-]+", comment["body"].lower())

    subreddits[subreddit]["comments"] += 1

    subreddits[subreddit]["words"] += len(word_list)

    for word in word_list:
        had_swears = False
        if word in args["swears"]:
            subreddits[subreddit]["swears"] += 1
            had_swears = True
        if had_swears:
            subreddits[subreddit]["profane_comments"] += 1


for file_pair in file_pairs:
    print(file_pair)
    execute_on_each_element(file_pair["comments_file_path"], experiment, arguments)

    date = file_pair["comments_file_path"][14:21]

    arguments["over_time"][date] = arguments["subreddits"]
    arguments["subreddits"] = {}

all_subreddits = set()

for date in sorted(arguments["over_time"]):
    for subreddit in arguments["over_time"][date]:
        all_subreddits.add(subreddit)

for month in sorted(arguments["over_time"]):
    for subreddit in all_subreddits:
        if subreddit not in arguments["over_time"][month]:
            arguments["over_time"][month][subreddit] = {
                "comments": 0,
                "profane_comments": 0,
                "swears": 0,
                "words": 0
            }

file = open("./output/comments_per_subreddit.csv", "w", newline="\n", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(["month"] + [subreddit for subreddit in sorted(all_subreddits)])
for month in sorted(arguments["over_time"]):
    writer.writerow([month] + [arguments["over_time"][month][subreddit]["comments"] for subreddit in sorted(all_subreddits)])
file.close()

file = open("./output/profane_comments_per_subreddit.csv", "w", newline="\n", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(["month"] + [subreddit for subreddit in sorted(all_subreddits)])
for month in sorted(arguments["over_time"]):
    writer.writerow([month] + [arguments["over_time"][month][subreddit]["profane_comments"] for subreddit in sorted(all_subreddits)])
file.close()

file = open("./output/swears_per_subreddit.csv", "w", newline="\n", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(["month"] + [subreddit for subreddit in sorted(all_subreddits)])
for month in sorted(arguments["over_time"]):
    writer.writerow([month] + [arguments["over_time"][month][subreddit]["swears"] for subreddit in sorted(all_subreddits)])
file.close()

file = open("./output/words_per_subreddit.csv", "w", newline="\n", encoding="utf-8")
writer = csv.writer(file)
writer.writerow(["month"] + [subreddit for subreddit in sorted(all_subreddits)])
for month in sorted(arguments["over_time"]):
    writer.writerow([month] + [arguments["over_time"][month][subreddit]["words"] for subreddit in sorted(all_subreddits)])
file.close()