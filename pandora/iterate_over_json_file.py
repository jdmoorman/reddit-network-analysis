import json


def execute_on_each_element(file_path, to_execute, args_to_pass, subreddit=""):
    with open(file_path, 'r', encoding="utf-8") as in_file:
        for line in in_file:
            element = json.loads(line)
            if subreddit == "" or element["subreddit"] == subreddit:
                to_execute(element, args_to_pass)
