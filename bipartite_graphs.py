import networkx as nx
from iterate_over_json_file import execute_on_each_element
import swear_word_set_getter


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


def get_swear_weighted_bipartite_graph_from_files(file_pairs):
    # Term document matrices for comments and threads
    arguments = {
        "swears": swear_word_set_getter.get_swear_word_set(),
        "user_set": set(),
        "thread_set": set(),
        "graph": nx.Graph()
    }

    def add_comment_to_graph(comment, args):
        pass

    for file_pair in file_pairs:
        print(file_pair)
        execute_on_each_element(file_pair["comments_file_path"], add_comment_to_graph, arguments)

    return arguments["graph"]