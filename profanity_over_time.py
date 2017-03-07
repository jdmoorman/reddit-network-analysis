# noinspection PyUnresolvedReferences
from iterate_over_json_file import execute_on_each_element
import re
import json
import operator
import csv
import swear_word_set_getter

start_year = 2005
start_month = 12

end_year = 2006
end_month = 12

file_pairs = []

# Set up the list of dates to run code on
for i in [1]:
    # dictionary = corpora.Dictionary.load("gensim_dictionary")

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

swear_word_map = {swear:0 for swear in swear_word_set_getter.get_swear_word_set()}

for swear in swear_word_map:
    print(swear)

# Term document matrices for comments and threads
arguments = {
    # "dictionary": dictionary,
    "comment_n": 1,
    "swears": swear_word_map,
    "swear_count": 0,
    "word_count": 0
}

def count_profanity(comment, args):
    word_list = re.findall(r"[\w'-]+", comment["body"].lower())

    args["word_count"] += len(word_list)

    for word in word_list:
        if word in args["swears"]:
            args["swear_count"] += 1
            args["swears"][word] += 1

    pass

prev_swear_count = 0
prev_word_count = 0

totals_file = open("./monthly_swear_and_word_totals.csv", "w", newline="\n", encoding="utf-8")
totals_writer = csv.writer(totals_file)
totals_writer.writerow(["month", "swears", "words", "ratio"])

swears_of_interest = sorted(swear_word_map)
prev_month_counts = {word:0 for word in swears_of_interest}

all_swears_file = open("./individual_swears_monthly.csv", "w", newline="\n", encoding="utf-8")
all_swears_writer = csv.writer(all_swears_file)
all_swears_writer.writerow(["month"]+swears_of_interest)

for file_pair in file_pairs:
    print(file_pair)
    execute_on_each_element(file_pair["comments_file_path"], count_profanity, arguments)
    date = file_pair["comments_file_path"][14:21]

    this_month_swear_count = arguments["swear_count"] - prev_swear_count
    this_month_word_count = arguments["word_count"] - prev_word_count
    this_month_counts = {word:arguments["swears"][word]-prev_month_counts[word] for word in swears_of_interest}

    prev_swear_count = arguments["swear_count"]
    prev_word_count = arguments["word_count"]
    prev_month_counts = {word:arguments["swears"][word] for word in swears_of_interest}

    totals_writer.writerow([date, this_month_swear_count, this_month_word_count, this_month_swear_count/this_month_word_count])
    all_swears_writer.writerow([date]+[this_month_counts[swear] for swear in swears_of_interest])
