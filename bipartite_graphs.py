"""
TODO: docstrings

TODO: example usage
"""
from __future__ import print_function

import pandas as pd


def files_to_polyad_counts(iter_json=None, count_id="count",
                           vert_keys=None, attr_keys=None):
    """
    Counts the number of times a given polyad occurs in a list of json objects.

    TODO: mention it's important one of the keys be author most of the time
    TODO: docstrings
    TODO: require file_sets
    TODO: use dataframes properly
    TODO: example usage
    """
    attr_keys = attr_keys or []
    polyad_dict = {}

    for elm in iter_json:
        # TODO: this is weirdly important for the single record edgecase
        if len(vert_keys) > 1:
            verts = tuple([elm[key] for key in vert_keys])
        else:
            verts = elm[vert_keys[0]]

        if verts not in polyad_dict:
            polyad_dict[verts] = [elm[key] for key in attr_keys] + [1]
        else:
            polyad_dict[verts][-1] += 1

    polyad_df = pd.DataFrame.from_dict(polyad_dict, orient='index')
    # TODO: tuple() here necessary?
    polyad_df.columns = tuple(attr_keys + [count_id])
    if len(vert_keys) > 1:
        new_index = pd.MultiIndex.from_tuples(polyad_df.index)
        # TODO: tuple() here necessary?
        new_index.rename(tuple(vert_keys), inplace=True)
        polyad_df.set_index(new_index, inplace=True)
    else:
        polyad_df.index.rename(vert_keys[0], inplace=True)

    polyad_df.sort_index(inplace=True)

    return polyad_df


if __name__ == "__main__":
    """
    TODO: by default this should get the comment count weighted bipartite graph
    TODO: move this stuff to an example notebook for convenience
    """

    # temporary sandbox for testing
    from iterators import list_files_from_date_range, iter_multiple_json_files
    from data.data_paths import LOCAL_COMMENTS_FMT_STR
    from sys import argv

    comment_files = list_files_from_date_range(
        LOCAL_COMMENTS_FMT_STR,
        int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4]))

    edge_df = files_to_polyad_counts(
        iter_json=iter_multiple_json_files(comment_files),
        vert_keys=["author", "link_id"])

    print(edge_df)
