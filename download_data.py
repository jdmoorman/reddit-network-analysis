"""
Example:
    Download reddit data from Dec 2006 to Jan 2007:

        $ python download_data.py 12 2006 1 2007

TODO: verify checksums
"""

from data.get_file_sets import from_date_range
from data.download_uncompress_bz2 import get_bz2

def download_data(start_month=12,
                  start_year=2005,
                  end_month=None,
                  end_year=None):
    """
    TODO: better docstring
    TODO: handle missing arguments

    Downloads comment and thread data between specified dates into ./data
    """

    # One set of files per month between the specified dates
    for file_set in from_date_range(start_month=start_month,
                                    start_year=start_year,
                                    end_month=end_month,
                                    end_year=end_year):

        # Download comments, uncompress and store as json at path
        get_bz2(url=file_set["remote_comments"],
                path=file_set["local_comments"])

        # Download threads, uncompress and store as json at path
        get_bz2(url=file_set["remote_threads"],
                path=file_set["local_threads"])

if __name__ == "__main__":
    from sys import argv
    
    download_data(start_month=int(argv[1]),
                  start_year=int(argv[2]),
                  end_month=int(argv[3]),
                  end_year=int(argv[4]))
