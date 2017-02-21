# noinspection PyUnresolvedReferences
from iterate_over_json_file import execute_on_each_element
import networkx as nx


# Returns thread trees associated with given subreddit (or all trees if no subreddit specified)
def get_thread_trees(file_pairs, subreddit=""):
    def add_thread_to_maps(thread, args):
        if "name" not in thread:
            thread["name"] = "t3_"+thread["id"]

        args["thread_map"][thread["name"]] = nx.DiGraph(root=[thread["name"]])
        args["thread_map"][thread["name"]].add_node(thread["name"], fake=False)

        for key in args["thread_keys"]:
            args["thread_map"][thread["name"]].node[thread["name"]][key] = thread[key]

    def add_comment_to_maps(comment, args):
        if "name" not in comment:
            comment["name"] = "t1_"+comment["id"]

        # If we have never seen the thread for this comment before, add it.
        if comment["link_id"] not in args["thread_map"]:
            args["thread_map"][comment["link_id"]] = nx.DiGraph(root=[comment["link_id"]])
            args["thread_map"][comment["link_id"]].add_node(comment["link_id"])
            args["thread_map"][comment["link_id"]].node[comment["link_id"]]["fake"] = True
            args["thread_map"][comment["link_id"]].node[comment["link_id"]]["subreddit"] = comment["subreddit"]
            args["thread_map"][comment["link_id"]].node[comment["link_id"]]["subreddit_id"] = comment["subreddit_id"]

        # If we have never seen this comment's parent before, add it.
        if not args["thread_map"][comment["link_id"]].has_node(comment["parent_id"]):
            # Note that we don't know who the parent's parent was so this creates a disconnected component.
            args["thread_map"][comment["link_id"]].add_node(comment["parent_id"])
            args["thread_map"][comment["link_id"]].node[comment["parent_id"]]["fake"] = True
            args["thread_map"][comment["link_id"]].node[comment["parent_id"]]["subreddit"] = comment["subreddit"]
            args["thread_map"][comment["link_id"]].node[comment["parent_id"]]["subreddit_id"] = comment["subreddit_id"]

        args["thread_map"][comment["link_id"]].add_node(comment["name"], fake=False)
        args["thread_map"][comment["link_id"]].add_edge(comment["parent_id"], comment["name"])

        for key in args["comment_keys"]:
            args["thread_map"][comment["link_id"]].node[comment["name"]][key] = comment[key]

    arguments = {
        # Time ordered list of thread IDs, note that there are no comments corresponding to these IDs
        "thread_map": {},

        # List of info to store for each thread
        "thread_keys": ["author", "permalink", "created_utc",
                        "downs", "ups", "score", "subreddit", "subreddit_id", "title", "url"],

        # List of info to store for each comment
        "comment_keys": ["author", "created_utc", "body",
                         "ups", "score", "subreddit", "subreddit_id"],

        "count": 0,

        "current_id": "",

        "error_count": 0
    }

    for file_pair in file_pairs:
        execute_on_each_element(file_pair["threads_file_path"], add_thread_to_maps, arguments, subreddit)
        execute_on_each_element(file_pair["comments_file_path"], add_comment_to_maps, arguments, subreddit)

    return arguments["thread_map"]
