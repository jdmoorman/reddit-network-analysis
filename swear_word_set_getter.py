import csv


def get_swear_word_set():
    with open("./swearword-list_both_trimmed.csv", 'r') as swear_word_map_file:
        swear_reader = csv.reader(swear_word_map_file, quotechar='|')
        next(swear_reader)
        return set([row[0].strip() for row in swear_reader])