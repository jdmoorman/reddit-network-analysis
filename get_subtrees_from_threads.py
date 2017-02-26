def get_root(tree):
    for potential_root in sorted(tree.nodes(), reverse=True):
        if not tree.predecessors(potential_root):
            return potential_root


def get_subtrees_using_criteria(tree, meets_criteria, root=""):
    if not root:
        root = get_root(tree)
        print(root)

    subtree_list = []

    nodes = [root]

    while nodes:
        node = nodes.pop(0)

        if meets_criteria(node):
            subtree_nodes = [node]
            subtree_candidates = sorted(tree.successors(node))
            while subtree_candidates:
                candidate = subtree_candidates.pop(0)

                if meets_criteria(candidate):
                    subtree_nodes.append(candidate)
                    subtree_candidates.extend(sorted(tree.successors(candidate)))
                else:
                    nodes.extend(sorted(tree.successors(candidate)))
            subtree_list.append(tree.subgraph(subtree_nodes))
            print("new subtree found")
        else:
            nodes.extend(sorted(tree.successors(node)))
    return subtree_list
