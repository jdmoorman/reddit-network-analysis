"""
TODO: docstrings
TODO: verify checksums
"""
import bz2
import requests

from .iterators import list_date_strings, format_each

from .paths import REMOTE_COMMENTS_FMT_STR, REMOTE_THREADS_FMT_STR, \
                   LOCAL_COMMENTS_FMT_STR, LOCAL_THREADS_FMT_STR

def download_data(*,
                  start_year: int,
                  start_month: int,
                  end_year: int,
                  end_month: int) -> None:
    """
    Downloads comment and thread data between specified dates, inclusive

    Example:
        Download reddit data from Dec 2006 to Jan 2007:

            download_data(2006, 12, 2007, 1)

    TODO: better docstring
    TODO: handle missing arguments

    """
    date_strings = list_date_strings(start_year=start_year,
                                     start_month=start_month,
                                     end_year=end_year,
                                     end_month=end_month)

    comment_urls = format_each(*date_strings, fmt_str=REMOTE_COMMENTS_FMT_STR)
    comment_paths = format_each(*date_strings, fmt_str=LOCAL_COMMENTS_FMT_STR)

    thread_urls = format_each(*date_strings, fmt_str=REMOTE_THREADS_FMT_STR)
    thread_paths = format_each(*date_strings, fmt_str=LOCAL_THREADS_FMT_STR)

    # One loop is used to download both comments and threads so that the
    # downloads alternate rather than downloading all the comments then all
    # the threads

    # One set of files per month between the specified dates
    for comments_url, comments_path, threads_url, threads_path in \
            zip(comment_urls, comment_paths, thread_urls, thread_paths):

        download_bz2(url=comments_url,
                     path=comments_path)

        download_bz2(url=threads_url,
                     path=threads_path)


def download_bz2(*,
                 url: str,
                 path: str,
                 verbose: bool = True) -> None:
    """
    Downloads bz2 file from url, uncompresses file into path.
    """

    if verbose:
        print("downloading", url)

    req = requests.get(url, stream=True)
    with open(path, 'wb') as out_file:
        decompressor = bz2.BZ2Decompressor()
        try:
            # TODO: is this chunk size reasonable?
            for chunk in req.iter_content(chunk_size=100*1024):
                if chunk:
                    out_file.write(decompressor.decompress(chunk))
        except (OSError, IOError):
            # This typically occurs when a requested file is not on the server.
            # Check that a file exists at the given url.
            if verbose:
                print("Remote file not found. Writing empty file.")
