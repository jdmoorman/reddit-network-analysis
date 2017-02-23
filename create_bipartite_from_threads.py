import networkx as nx


def get_bipartite_graph(thread_map):
    fake_count = 0
    deleted_count = 0
    bi_graph = nx.MultiGraph()

    for thread in sorted(thread_map):
        bi_graph.add_node(thread)
        for node in thread_map[thread].nodes():

            author = thread_map[thread].node[node]["author"]

            # If author is fake or deleted then make sure they are
            # differentiated from all the other fake and deleted users
            if author == "[fake]":
                author = "[fake"+str(fake_count)+"]"
                fake_count += 1
            elif author == "[deleted]":
                author = "[deleted"+str(deleted_count)+"]"
                deleted_count += 1

            if not bi_graph.has_node(author):
                bi_graph.add_node(author)

            bi_graph.add_edge(author, thread, comment=thread_map[thread].node[node]["body"])

    return bi_graph
