"""
Generators for files where each line of each file is a json object
"""

import json


def iter_single_json_file(file_path):
    """
    Generates json object from each line of the file at the given path
    """

    # TODO: figure out why encoding="utf-8" was here
    with open(file_path, 'r') as in_file:
        for line in in_file:
            yield json.loads(line)


def iter_multiple_json_files(file_paths):
    """
    Generates json object from each line of each file in a list of file paths
    """
    for file_path in file_paths:
        for element in iter_single_json_file(file_path):
            yield element
