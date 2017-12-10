"""
TODO: docstrings

TODO: example usage
"""
from __future__ import print_function

from data.get_file_sets import from_date_range
from iterate_over_json import iter_multiple_json_files
import pandas as pd


def files_to_polyad_counts(file_paths=None, count_id="count",
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

    for elm in iter_multiple_json_files(file_paths):
        verts = tuple([elm[key] for key in vert_keys])
        if verts not in polyad_dict:
            polyad_dict[verts] = [elm[key] for key in attr_keys] + [1]
        else:
            polyad_dict[verts][-1] += 1

    polyad_df = pd.DataFrame.from_dict(polyad_dict, orient='index')
    polyad_df.columns = tuple(attr_keys + [count_id])
    new_index = pd.MultiIndex.from_tuples(polyad_df.index)
    new_index.rename(tuple(vert_keys) if len(vert_keys) > 1 else vert_keys[0],
                     inplace=True)
    polyad_df.set_index(new_index, inplace=True)
    polyad_df.sort_index(inplace=True)

    return polyad_df


if __name__ == "__main__":
    """
    TODO: by default this should get the comment count weighted bipartite graph
    TODO: move this stuff to an example notebook for convenience
    """

    # temporary sandbox for testing
    from sys import argv

    file_sets = from_date_range(start_month=int(argv[1]),
                                start_year=int(argv[2]),
                                end_month=int(argv[3]),
                                end_year=int(argv[4]))

    comment_files = [file_set["local_comments"] for file_set in file_sets]

    edge_df = files_to_polyad_counts(file_paths=comment_files,
                                     vert_keys=["author", "subreddit_id"])

    sr_df = files_to_polyad_counts(file_paths=comment_files,
                                   vert_keys=["subreddit_id"],
                                   attr_keys=["subreddit"])

    thread_df = files_to_polyad_counts(file_paths=comment_files,
                                       vert_keys=["link_id"],
                                       attr_keys=["subreddit_id"])

    print(edge_df)
    print(sr_df)
    print(thread_df)

    exit()
