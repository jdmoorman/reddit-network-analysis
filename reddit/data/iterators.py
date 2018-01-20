"""
generators for things
TODO: better docstring
TODO: carefully only use generators for things that make sense to generate.
Don't bother generating things that would be super quick to list out.
"""

from typing import List, Iterator, Iterable, Any

import ujson as json
import io
import datetime

import pandas as pd

def iter_json_file(path: str) -> Iterator[dict]:
    """
    Generates json object from each line of the file at the given path
    """

    # TODO: figure out why encoding="utf-8" was here
    with io.open(path, 'r') as in_file:
        for line in in_file:
            yield json.loads(line)

def iter_json_files(paths: List[str]) -> Iterator[dict]:
    """
    Generates dict from json on each line of each file in a list of paths
    """
    for path in paths:
        for element in iter_json_file(path):
            yield element

def iter_partial_records(*,
                         paths: List[str],
                         keys: List[str]) -> Iterator[List[Any]]:
    """
    Generates lists of values corresponding to the given list of keys from each
    line of the json files specified in paths.
    """
    for elm in iter_json_files(paths):
        yield [elm[key] for key in keys]

def list_date_strings(*,
                      start_year: int,
                      start_month: int,
                      end_year: int,
                      end_month: int) -> List[str]:
    """
    Returns list of date strings for each month between the specified start
    and end months (inclusive). Uses the format YYYY-MM.
    """

    month = start_month
    year = start_year

    date_strings = []

    while year * 100 + month <= 100 * end_year + end_month:
        date_strings.append(datetime.date(year, month, 1).strftime("%Y-%m"))

        month += 1
        if month > 12:
            month = 1
            year += 1

    return date_strings

def format_each(*fmt_specs: Iterable,
                fmt_str: str) -> List[str]:
    """
    Apply same format string to each arg set in a list
    """
    return [fmt_str.format(fmt_spec) for fmt_spec in fmt_specs]
