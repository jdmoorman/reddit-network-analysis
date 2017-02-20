import iterate_over_comments


# Returns thread trees associated with given subreddit (or all trees if no subreddit specified)
def get_thread_trees(subreddit=""):

    def add_comment_to_maps(comment, args):
        args["count"] += 1
        if args["count"] % 100000 == 0:
            print(args["count"])

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

        "parentless_count": 0
    }

    iterate_over_comments.execute_on_each_comment(add_comment_to_maps, subreddit, arguments)

    return arguments["thread_map"], arguments["comment_map"]
