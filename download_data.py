"""
Example:
    Download reddit data from Dec 2006 to Jan 2007:

        $ python download_data.py 2006 12 2007 1

TODO: verify checksums
"""
from data.data_paths import REMOTE_COMMENTS_FMT_STR, REMOTE_THREADS_FMT_STR, \
    LOCAL_COMMENTS_FMT_STR, LOCAL_THREADS_FMT_STR
from iterators import list_files_from_date_range
from data.download_uncompress_bz2 import get_bz2

def download_data(*date_args):
    """
    Downloads comment and thread data between (inclusive) specified dates

    Arguments:
        start_year  (int)
        start_month (int)
        end_year    (int)
        end_month   (int)

    Example:
        Download reddit data from Dec 2006 to Jan 2007:

            download_data(2006, 12, 2007, 1)

    TODO: better docstring
    TODO: handle missing arguments

    """
    remote_comments_list = list_files_from_date_range(
        REMOTE_COMMENTS_FMT_STR, *date_args)
    local_comments_list = list_files_from_date_range(
        LOCAL_COMMENTS_FMT_STR, *date_args)

    remote_threads_list = list_files_from_date_range(
        REMOTE_THREADS_FMT_STR, *date_args)
    local_threads_list = list_files_from_date_range(
        LOCAL_THREADS_FMT_STR, *date_args)

    # One loop is used to download both comments and threads so that the
    # downloads alternate rather than downloading all the comments then all
    # the threads

    # One set of files per month between the specified dates
    for comments_url, comments_filepath, \
        threads_url, threads_filepath in zip(remote_comments_list,
                                             local_comments_list,
                                             remote_threads_list,
                                             local_threads_list):

        # Download comments, uncompress and store as json at path
        get_bz2(url=comments_url,
                path=comments_filepath)

        # Download threads, uncompress and store as json at path
        get_bz2(url=threads_url,
                path=threads_filepath)

if __name__ == "__main__":
    from sys import argv
    
    download_data(int(argv[1]), int(argv[2]), int(argv[3]), int(argv[4]))
