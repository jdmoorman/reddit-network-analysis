"""
TODO: docstrings

TODO: example usage
"""

from typing import Iterable, List, Set, Dict, Tuple

import pandas as pd
import scipy.sparse as sparse

from .iterators import iter_partial_records, iter_json_files

def level_sets(*,
               paths: List[str],
               keys: List[str]) -> List[Set[str]]:
    """
    For each desired key, get the set of all possible corresponding values
    """
    level_sets: List[Set[str]] = [set() for key in keys]

    for record in iter_partial_records(paths=paths, keys=keys):
        for i, level in enumerate(record):
            level_sets[i].add(level)

    return level_sets

def td_matrix(*,
              paths: List[str],
              term_key: str,
              doc_key: str) -> sparse.spmatrix:
    keys = [term_key, doc_key]
    levels = level_sets(paths=paths, keys=keys)

    M = len(levels[0])
    N = len(levels[1])
    
    terms = {term: i for i, term in enumerate(levels[0])}
    docs = {doc: i for i, doc in enumerate(levels[1])}

    tf = sparse.lil_matrix((M, N))

    for record in iter_partial_records(paths=paths, keys=keys):
        tf[terms[record[0]], docs[record[1]]] += 1

    return tf

def td_matrix2(*,
              paths: List[str],
              term_key: str,
              doc_key: str) -> sparse.spmatrix:
    n_terms = 0
    terms: Dict[str, int] = {}

    n_docs = 0
    docs: Dict[str, int] = {}

    td_records: Dict[Tuple[int, int], int] = {}

    # for each record
    for record in iter_partial_records(paths=paths, keys=[term_key, doc_key]):
        term = record[0]
        doc = record[1]

        if term not in terms:
            terms[term] = n_terms
            n_terms += 1

        if doc not in docs:
            docs[doc] = n_docs
            n_docs += 1
        
        term_i = terms[term]
        doc_i = docs[doc]

        if (term_i, doc_i) not in td_records:
            td_records[(term_i, doc_i)] = 0
        
        td_records[(term_i, doc_i)] += 1

    M = len(terms)
    N = len(docs)
    
    td = sparse.dok_matrix((M, N))

    for td_id, val in td_records.items():
        td[td_id] = val

    return td

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