import thread_tree_utils


def get_subtrees_using_criteria(tree, meets_criteria, root=""):
    if not root:
        root = thread_tree_utils.get_root(tree)
        print(root)

    subtree_list = []
    nodes = [root]
    while nodes:
        node = nodes.pop(0)
        if meets_criteria(tree.node[node]):
            subtree_nodes = [node]
            subtree_candidates = sorted(tree.successors(node))
            while subtree_candidates:
                candidate = subtree_candidates.pop(0)
                if meets_criteria(tree.node[candidate]):
                    subtree_nodes.append(candidate)
                    subtree_candidates.extend(sorted(tree.successors(candidate)))
                else:
                    nodes.extend(sorted(tree.successors(candidate)))
            subtree_list.append(tree.subgraph(subtree_nodes))
        else:
            nodes.extend(sorted(tree.successors(node)))
    return subtree_list
