# Get root node name from tree graph
def get_root(tree):
    for potential_root in sorted(tree.nodes(), reverse=True):
        if not tree.predecessors(potential_root):
            return potential_root

# Recursively print all nodes in a tree with proper indentation and hierarchical structure
def preorder_print(graph, node, key_to_sort="created_utc", depth=0):
    if graph.node[node]["fake"]:
        print(">>>>" * depth + " " * (depth > 0) + str(graph.node[node]))
    else:
        print(">>>>" * depth + " " * (depth > 0) + str(graph.node[node]))
    for child in sorted(graph.successors(node), key=lambda x: graph.node[x][key_to_sort]):
        preorder_print(graph, child, key_to_sort, depth + 1)