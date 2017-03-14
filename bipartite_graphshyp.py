import networkx as nx
from iterate_over_json_file import execute_on_each_element
import swear_word_set_getter
import re


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


def get_swear_count_weighted_bipartite_graph_from_files(file_pairs):
    # Term document matrices for comments and threads
    arguments = {
        "swears": swear_word_set_getter.get_swear_word_set(),
        "author_map": {},
        "thread_map": {},
        "graph": nx.Graph(),
        "deleted_author_count":0
    }

    def add_comment_to_graph(comment, args):
        word_list = re.findall(r"[\w'-]+", comment["body"].lower())
        swears = args["swears"]
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

        swear_count = 0
        for word in word_list:
            if word in swears:
                swear_count += 1
        if(swear_count>0):
            if graph.has_edge(author, thread):
                graph.edge[author][thread]["weight"] += swear_count
            else:
                graph.add_edge(author, thread, weight=swear_count)

    for file_pair in file_pairs:
        print(file_pair)
        execute_on_each_element(file_pair["comments_file_path"], add_comment_to_graph, arguments)

    return arguments["graph"]

def get_profane_comment_count_weighted_bipartite_graph_from_files(file_pairs):
    # Term document matrices for comments and threads
    arguments = {
        "swears": swear_word_set_getter.get_swear_word_set(),
        "author_map": {},
        "thread_map": {},
        "graph": nx.Graph(),
        "deleted_author_count":0
    }

    def add_comment_to_graph(comment, args):
        word_list = re.findall(r"[\w'-]+", comment["body"].lower())
        swears = args["swears"]
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

        swore = 0
        for word in word_list:
            if word in swears:
                swore = 1
                break

        if graph.has_edge(author, thread):
            graph.edge[author][thread]["weight"] += swore
        else:
            graph.add_edge(author, thread, weight=swore)

    for file_pair in file_pairs:
        print(file_pair)
        execute_on_each_element(file_pair["comments_file_path"], add_comment_to_graph, arguments)

    return arguments["graph"]

def weight_by_sum_of_weights_above_thresh(graph, node, neigh1, neigh2):
    if graph.edge[node][neigh1]["weight"] + graph.edge[node][neigh2]["weight"] > 10:
        return 1/(len(graph.neighbors(node)) )
    else:
        return 0

def projected_graph(bi_graph, nodes, weight_function):
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node)
        for attribute in bi_graph.node[node]:
            graph.node[node][attribute] = bi_graph.node[node][attribute]
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