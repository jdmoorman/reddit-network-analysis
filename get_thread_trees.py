# noinspection PyUnresolvedReferences
from iterate_over_json_file import execute_on_each_element


# Returns thread trees associated with given subreddit (or all trees if no subreddit specified)
def get_thread_trees(file_pairs, subreddit=""):
    def add_thread_to_maps(thread, args):
        if "name" not in thread:
            thread["name"] = "t3_"+thread["id"]

        args["thread_map"][thread["name"]] = {"thread": thread, "children_ids": []}

    def add_comment_to_maps(comment, args):
        if "name" not in comment:
            comment["name"] = "t1_"+comment["id"]

        # If comment's parent exists, add self to list of children.
        if comment["parent_id"] in args["comment_map"]:
            args["comment_map"][comment["parent_id"]]["children_ids"].append(comment["name"])
        else:
            if comment["link_id"] in args["thread_map"]:
                args["thread_map"][comment["link_id"]]["children_ids"].append(comment["name"])
            else:
                args["thread_map"][comment["link_id"]] = {
                    "thread": {
                        "subreddit": comment["subreddit"],
                        "num_comments": 0
                    },
                    "children_ids": [comment["name"]]
                }

        args["comment_map"][comment["name"]] = {"comment": comment, "children_ids": []}
        args["thread_map"][comment["link_id"]]["thread"]["num_comments"] += 1

    arguments = {
        # Maps each comment ID to a time ordered list of its children's IDs
        "comment_map": {},

        # Time ordered list of thread IDs, note that there are no comments corresponding to these IDs
        "thread_map": {},

        "count": 0,

        "current_id": "",

        "error_count": 0
    }

    for file_pair in file_pairs:
        print("begin working on: ", file_pair)
        execute_on_each_element(file_pair["threads_file_path"], add_thread_to_maps, arguments, subreddit)
        execute_on_each_element(file_pair["comments_file_path"], add_comment_to_maps, arguments, subreddit)

    return arguments["thread_map"], arguments["comment_map"]
