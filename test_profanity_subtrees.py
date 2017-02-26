import get_thread_trees
import bipartite_graphs
import thread_tree_utils
import get_subtrees_from_threads
import networkx as nx
import warnings
warnings.filterwarnings("ignore", message="pyplot.hold is deprecated")
warnings.filterwarnings("ignore", message="axes.hold is deprecated")
import random
random.seed(1)

# This file is a sandbox for work in progress


file_dates = ["2005-12", "2006-01", "2006-02"]
file_pairs = [
    {
        "comments_file_path": "./comments/RC_" + date + ".json",
        "threads_file_path": "./submissions/RS_" + date + ".json"
    } for date in file_dates
]

# Optionally pass a string argument with the subreddit into get_thread_trees
thread_map = get_thread_trees.get_thread_trees(file_pairs)

def criteria(comment):
    return "it" in comment["body"].lower()

for head in sorted(thread_map):
    assert(nx.is_forest(thread_map[head]))

    if thread_map[head].order() > 20:
        thread_tree_utils.preorder_print(thread_map[head], head)
        subtree_list = get_subtrees_from_threads.get_subtrees_using_criteria(thread_map[head], criteria)
        for tree in subtree_list:
            print()
            print("#nodes:",tree.order())
            thread_tree_utils.preorder_print(tree, thread_tree_utils.get_root(tree))

        # preorder_print(thread_map[head], head)
        # nx.draw_networkx(thread_map[head])
        # plt.show()
        break

# bipartite_graph = bipartite_graphs.get_bipartite_graph_from_threads(thread_map)
#
# largest_component = max(nx.connected_component_subgraphs(bipartite_graph), key=len)
# print("largest connected component: ", len(largest_component))
# print("full graph: ", len(bipartite_graph))


# swear_file_path = paths.get_profanity_file_name()
#
# with open(swear_file_path, 'r') as swear_word_map_file:
#     swear_word_map = json.load(swear_word_map_file)

# # This is a naive way of counting swears. Consider faster less exact regex.
# for key in swear_word_map:
#     for word in swear_word_map[key]:
#         n_swears = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), comment["body"]))
