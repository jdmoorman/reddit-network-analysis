"""
TODO: docstrings

TODO: example usage
"""
from __future__ import print_function

import networkx as nx
from data.get_file_sets import from_date_range
from iterate_over_json import iter_multiple_json_files
import re
import pandas as pd


def get_bipartite_graph_from_threads(thread_map):
    fake_or_deleted_count = 0
    bi_graph = nx.MultiGraph()

    for thread in sorted(thread_map):
        bi_graph.add_node(thread, bipartite="thread")
        for node in thread_map[thread].nodes():

            author = thread_map[thread].node[node]["author"]

            # If author is fake or deleted then make sure they are
            # differentiated from all the other fake and deleted users
            if author == "[fake]" or author == "[deleted]":
                author = author[0:-1] + str(fake_or_deleted_count) + author[-1]
                fake_or_deleted_count += 1

            if not bi_graph.has_node(author):
                bi_graph.add_node(author, bipartite="author")

            bi_graph.add_edge(author, thread, comment=thread_map[thread].node[node]["body"])

    assert(nx.is_bipartite(bi_graph))

    return bi_graph


def get_author_and_thread_nodes(bi_graph):
    author_nodes = set(n for n, d in bi_graph.nodes(data=True) if d["bipartite"] == "author")
    thread_nodes = set(bi_graph) - author_nodes
    return author_nodes, thread_nodes


def get_comment_count_weighted_bipartite_graph_from_files(file_pairs):
    # Term document matrices for comments and threads
    arguments = {
        "swears": swear_word_set_getter.get_swear_word_set(),
        "author_map": {},
        "thread_map": {},
        "graph": nx.Graph(),
        "deleted_author_count":0
    }

    def add_comment_to_graph(comment, args):
        author = comment["author"]
        thread = comment["link_id"]
        author_map = args["author_map"]
        thread_map = args["thread_map"]
        graph = args["graph"]

        if author == "[deleted]":
            author += str(args["deleted_author_count"])
            args["deleted_author_count"] += 1
            return

        if author not in author_map:
            author_map[author] = 1
            graph.add_node(author, bipartite="author")
        else:
            author_map[author] += 1

        if thread not in thread_map:
            thread_map[thread] = 1
            graph.add_node(thread, bipartite="thread",subreddit=comment['subreddit'])
        else:
            thread_map[thread] += 1

        if graph.has_edge(author, thread):
            graph.edge[author][thread]["weight"] += 1
        else:
            graph.add_edge(author, thread, weight=1)

    for file_pair in file_pairs:
        print(file_pair)
        execute_on_each_element(file_pair["comments_file_path"], add_comment_to_graph, arguments)

    return arguments["graph"]


def weight_by_sum_of_weights_above_thresh(graph, node, neigh1, neigh2):
    if graph.edge[node][neigh1]["weight"] + graph.edge[node][neigh2]["weight"] > 10:
        return 1
    else:
        return 0


def projected_graph(bi_graph, nodes, weight_function):
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node)
    for node in set(bi_graph)-nodes:
        for neigh1 in bi_graph.neighbors(node):
            for neigh2 in bi_graph.neighbors(node):
                if neigh1 == neigh2:
                    continue
                weight = weight_function(bi_graph, node, neigh1, neigh2)
                if weight == 0:
                    continue
                if graph.has_edge(neigh1, neigh2):
                    graph.edge[neigh1][neigh2]["weight"] += weight
                else:
                    graph.add_edge(neigh1,neigh2,weight=weight)
    return graph


def files_to_edgecounts(file_paths=None, edge_attr_keys=None,
                        vert1_key=None, vert2_key=None,
                        count_id="count"):
    """
    TODO: mention it's important one of the keys be author most of the time
    TODO: docstrings
    TODO: require file_sets
    TODO: use dataframes properly
    TODO: example usage
    """
    edge_attr_keys = edge_attr_keys or []
    edge_dict = {}

    for elm in iter_multiple_json_files(file_paths):
        verts = (elm[vert1_key], elm[vert2_key])
        if verts not in edge_dict:
            edge_dict[verts] = [elm[key] for key in edge_attr_keys] + [1]
        else:
            edge_dict[verts][-1] += 1

    edge_df = pd.DataFrame.from_dict(edge_dict, orient='index')
    edge_df.columns = edge_attr_keys + [count_id]
    edge_df.set_index(pd.MultiIndex.from_tuples(edge_df.index), inplace=True)
    edge_df.index.rename([vert1_key, vert2_key], inplace=True)
    edge_df.sort_index(inplace=True)

    return edge_df

def files_to_vertex_attributes(file_paths=None, vert_key=None,
                               attr_keys=None):
    attr_keys = attr_keys or []
    attr_dict = {}

    for elm in iter_multiple_json_files(file_paths):
        vert = elm[vert_key]
        attr_dict[vert] = [elm[key] for key in attr_keys]

    attr_df = pd.DataFrame.from_dict(attr_dict, orient='index')
    attr_df.index.rename(vert_key, inplace=True)
    attr_df.columns = attr_keys
    attr_df.sort_index(inplace=True)

    return attr_df


if __name__ == "__main__":
    """
    TODO: by default this should get the comment count weighted bipartite graph
    """

    # temporary sandbox for testing
    from sys import argv

    file_sets = from_date_range(start_month=int(argv[1]),
                                start_year=int(argv[2]),
                                end_month=int(argv[3]),
                                end_year=int(argv[4]))

    comment_files = [file_set["local_comments"] for file_set in file_sets]

    edge_df = files_to_edgecounts(file_paths=comment_files,
                                  vert1_key="author",
                                  vert2_key="subreddit")

    thread_df = files_to_vertex_attributes(file_paths=comment_files,
                                           vert_key="link_id",
                                           attr_keys=["subreddit"])

    sr_df = files_to_vertex_attributes(file_paths=comment_files,
                                       vert_key="subreddit_id",
                                       attr_keys=["subreddit"])

    print(edge_df)
    print(thread_df)
    print(sr_df)

                


    