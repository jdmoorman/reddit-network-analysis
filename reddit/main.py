"""
Playground for stuff
"""

from data.download import download_comments_and_threads
from data.paths import LOCAL_COMMENTS_FMT_STR
from data.iterators import list_date_strings, format_each
from data.preprocess import records_df
import pandas as pd
import time

if __name__ == "__main__":
    from sys import argv

    start_year=int(argv[1])
    start_month=int(argv[2])
    end_year=int(argv[3])
    end_month=int(argv[4])

    download_comments_and_threads(start_year=start_year,
                                  start_month=start_month,
                                  end_year=end_year,
                                  end_month=end_month)

    date_strings = list_date_strings(start_year=start_year,
                                     start_month=start_month,
                                     end_year=end_year,
                                     end_month=end_month)
    comment_paths = format_each(*date_strings, fmt_str=LOCAL_COMMENTS_FMT_STR)

    start = time.time()
    mid = time.time()
    full_df = records_df(paths=comment_paths)
    end = time.time()

    print(mid-start)
    print(end-mid)