import json
import paths


def execute_on_each_comment(to_execute, subreddit, args_to_pass):
    data_directory_path = paths.get_data_directory_path()
    data_file_names = paths.get_data_file_names()
    for data_file_name in data_file_names:
        with open(data_directory_path + data_file_name, 'r', encoding="utf-8") as in_file:
            for line in in_file:
                comment = json.loads(line)
                if subreddit == "" or comment["subreddit"] == subreddit:
                    to_execute(comment, args_to_pass)
