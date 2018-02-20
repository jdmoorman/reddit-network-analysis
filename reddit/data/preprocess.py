"""
TODO: docstrings

TODO: example usage
"""

from typing import Iterable, List, Set, Dict, Tuple

import pandas as pd
import glob
import os.path as osp

from .iterators import iter_partial_records, iter_json_files, merge_lists
from .experiment import Experiment
from .paths import LOCAL_COMMENTS_DIR, LOCAL_THREADS_DIR



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

def extract_terms_by_document(*,
                              name: str,
                              term_key: str,
                              doc_key: str,
                              dir_path: str,
                              verbose: bool = True,
                              existing: bool = True) -> None:
    """
    For each file full of comments or threads, extracts the entry corresponding
    to the given key, and subreddit of each record. Creates a file
    corresponding to the subreddit, and stores a list of the authors who
    posted to that subreddit.
    """
    
    paths = sorted(glob.glob(osp.join(dir_path, "*")))

    for path in paths:
        date = osp.splitext(osp.basename(path))[0]

        exp = Experiment(name=osp.join(name, date), existing=True)

        if exp.glob("*"):
            if verbose:
                print("skipping", path, "already extracted")
            continue


        for record in iter_partial_records(paths=[path],
                                           keys=[term_key, doc_key]):
            term = record[0]
            doc = record[1]
            with exp.open(doc, "a") as f:
                f.write(term + "\n")