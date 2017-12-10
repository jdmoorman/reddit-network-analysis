"""
TODO: docstrings
"""

from __future__ import print_function

from os.path import abspath, dirname, join

REMOTE_BASE = "http://files.pushshift.io/reddit/"

# TODO: abstract this out to configurable location.
LOCAL_BASE = abspath(dirname(__file__))

def from_date_range(start_month=None,
                    start_year=None,
                    end_month=None,
                    end_year=None):
    
    if not (start_month and start_year and end_month and end_year):
        print("all arguments required")
        return []

    # TODO: use proper date library to clean this up.
    year = start_year
    month = start_month

    file_pairs = []

    while year * 100 + month <= 100 * end_year + end_month:
        # TODO: gross. clean this up.
        date = str(year) + "-" + "0" * (2 - len(str(month))) + str(month)

        file_pairs.append({
            "local_comments": join(LOCAL_BASE,
                              "comments", "RC_" + date + ".json"),
            "local_threads": join(LOCAL_BASE,
                              "submissions", "RS_" + date + ".json"),
            "remote_comments": join(REMOTE_BASE,
                              "comments", "RC_" + date + ".bz2"),
            "remote_threads": join(REMOTE_BASE,
                              "submissions", "RS_" + date + ".bz2"),
        })

        month += 1
        if month > 12:
            month = 1
            year += 1

    return file_pairs
