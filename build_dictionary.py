# noinspection PyUnresolvedReferences
from iterate_over_json_file import execute_on_each_element
import re
import json
import warnings
warnings.filterwarnings("ignore", message="pyplot.hold is deprecated")
warnings.filterwarnings("ignore", message="axes.hold is deprecated")


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

print(file_dates)

arguments = {"dictionary": {}}


def add_words_to_dictionary(comment, args):
    words = re.findall(r"[\w'-]+", comment["body"].lower())
    for word in words:
        if word not in args["dictionary"]:
            args["dictionary"][word] = 1
        else:
            args["dictionary"][word] += 1

for file_pair in file_pairs:
    execute_on_each_element(file_pair["comments_file_path"], add_words_to_dictionary, arguments)

with open('./dictionary.json', 'w') as fp:
    json.dump(arguments["dictionary"], fp)
