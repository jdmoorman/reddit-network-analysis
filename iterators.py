"""
generators for things
TODO: better docstring
TODO: carefully only use generators for things that make sense to generate.
Don't bother generating things that would be super quick to list out.
"""

import json
import io
import datetime


def iter_single_json_file(file_path):
    """
    Generates json object from each line of the file at the given path
    """

    # TODO: figure out why encoding="utf-8" was here
    with io.open(file_path, 'r', encoding="utf-8") as in_file:
        for line in in_file:
            yield json.loads(line, encoding="utf-8")


def iter_multiple_json_files(file_paths):
    """
    Generates json object from each line of each file in a list of file paths
    """
    for file_path in file_paths:
        for element in iter_single_json_file(file_path):
            yield element

def list_date_strings(start_year, start_month, end_year, end_month):
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

def list_files_from_date_range(fmt_str,
                               start_year, start_month, end_year, end_month):
    """
    Returns a list of fmt_str with date strings for each date in the date range
    inserted via .format(date_str)
    """

    return [fmt_str.format(date_str) for date_str in
            list_date_strings(start_year, start_month, end_year, end_month)]