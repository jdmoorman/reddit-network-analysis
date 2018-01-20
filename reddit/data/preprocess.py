"""
TODO: docstrings

TODO: example usage
"""

from typing import Iterable, List, Set

import pandas as pd

from .iterators import iter_partial_records, iter_json_files

def _partial_records_df(*,
                        paths: List[str],
                        keys: List[str]) -> pd.DataFrame:
    """
    Creates a dataframe with columns corresponding to the specified keys from
    the json files specified by paths, storing one row per line of each file
    """
    return pd.DataFrame(iter_partial_records(paths=paths, keys=keys),
                        columns=keys)

def _full_records_df(*,
                     paths: List[str]) -> pd.DataFrame:
    """
    Creates a dataframe with columns corresponding to all keys present in json
    files specified by paths, storing one row per line of each file
    """
    return pd.DataFrame(iter_json_files(paths=paths))

def records_df(*,
               paths: List[str],
               keys: List[str] = None) -> pd.DataFrame:
    """
    Creates a dataframe from json files at paths, optionally only including
    columns indicated by keys.
    """
    if keys is None:
        return _full_records_df(paths=paths)

    return _partial_records_df(paths=paths,
                               keys=keys)
