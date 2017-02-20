import iterate_over_json_file


# Returns thread trees associated with given subreddit (or all trees if no subreddit specified)
def get_thread_trees(file_pairs, subreddit=""):
    def add_thread_to_maps(thread, args):
        args["count"] += 1
        if args["count"] % 100000 == 0:
            print(args["count"])

        if "name" not in thread:
            thread["name"] = "t3_"+thread["id"]

        args["thread_map"][thread["name"]] = {"thread": thread, "children_ids": []}

    def add_comment_to_maps(comment, args):
        args["count"] += 1
        if args["count"] % 100000 == 0:
            print(args["count"])

        if "name" not in comment:
            comment["name"] = "t1_"+comment["id"]

        # If comment's parent exists, add self to list of children.
        if comment["parent_id"] in args["comment_map"]:
            args["comment_map"][comment["parent_id"]]["children_ids"].append(comment["name"])
        else:
            if comment["link_id"] in args["thread_map"]:
                args["thread_map"][comment["link_id"]]["children_ids"].append(comment["name"])
            else:
                args["thread_map"][comment["link_id"]] = {"children_ids": [comment["name"]]}

        args["comment_map"][comment["name"]] = {"comment": comment, "children_ids": []}

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
        threads_file_path = file_pair["threads_file_path"]
        comments_file_path = file_pair["comments_file_path"]
        iterate_over_json_file.execute_on_each_element(threads_file_path, add_thread_to_maps, arguments, subreddit)
        iterate_over_json_file.execute_on_each_element(comments_file_path, add_comment_to_maps, arguments, subreddit)

    return arguments["thread_map"], arguments["comment_map"]
