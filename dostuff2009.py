import get_thread_trees2009
import bipartite_graphs
import networkx as nx
import matplotlib.pyplot as plt
import thread_tree_utils
import warnings
import construct_file_pairs
warnings.filterwarnings("ignore", message="pyplot.hold is deprecated")
warnings.filterwarnings("ignore", message="axes.hold is deprecated")


# This file is a sandbox for work in progress


file_pairs = construct_file_pairs.file_pairs_from_date_range(1,2009,1,2009)


list_of_ids = ['t3_7mqez', 't3_7qj9j', 't3_7nbbd']

thread_map = get_thread_trees.get_thread_trees(file_pairs)

for head in sorted(thread_map):
    if head in list_of_ids:
        print()
        print(head)
        thread_tree_utils.preorder_print(thread_map[head], head)
    assert(nx.is_forest(thread_map[head]))

# # Recursively print all comments in a thread with proper indentation
# def preorder_print(graph, node, key_to_sort="created_utc", depth=0):
#     if graph.node[node]["fake"]:
#         print(">>>>" * depth + " " * (depth > 0) + str(graph.node[node]))
#     else:
#         print(">>>>" * depth + " " * (depth > 0) + str(graph.node[node]))
#     for child in sorted(graph.successors(node), key=lambda x: graph.node[x][key_to_sort]):
#         preorder_print(graph, child, key_to_sort, depth+1)


    # if thread_map[head].order() > 20:
    #     preorder_print(thread_map[head], head)
    #     nx.draw_networkx(thread_map[head])
    #     plt.show()
    #     break


# swear_file_path = paths.get_profanity_file_name()
#
# with open(swear_file_path, 'r') as swear_word_map_file:
#     swear_word_map = json.load(swear_word_map_file)

# # This is a naive way of counting swears. Consider faster less exact regex.
# for key in swear_word_map:
#     for word in swear_word_map[key]:
#         n_swears = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), comment["body"]))
