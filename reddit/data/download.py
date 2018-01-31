"""
TODO: docstrings
TODO: verify checksums
"""
import bz2
import requests

from .iterators import list_date_strings, format_each, merge_lists

from .paths import REMOTE_COMMENTS_FMT_STR, REMOTE_THREADS_FMT_STR, \
                   LOCAL_COMMENTS_FMT_STR, LOCAL_THREADS_FMT_STR

from typing import List

def download_comments_and_threads(*,
                                  date_strings: List[str],
                                  verbose: bool = True) -> None:
    """
    Downloads comment and thread data

    TODO: better docstring
    TODO: handle missing arguments

    """

    comment_urls = format_each(*date_strings, fmt_str=REMOTE_COMMENTS_FMT_STR)
    comment_paths = format_each(*date_strings, fmt_str=LOCAL_COMMENTS_FMT_STR)

    thread_urls = format_each(*date_strings, fmt_str=REMOTE_THREADS_FMT_STR)
    thread_paths = format_each(*date_strings, fmt_str=LOCAL_THREADS_FMT_STR)

    download_bz2s(urls=merge_lists(comment_urls, thread_urls),
                  paths=merge_lists(comment_paths, thread_paths),
                  verbose=verbose)

def download_bz2(*,
                 url: str,
                 path: str,
                 verbose: bool = True) -> None:
    """
    Downloads bz2 file from url, uncompresses file into path.
    """

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

def download_bz2s(*,
                  urls: List[str],
                  paths: List[str],
                  verbose: bool = True) -> None:
    """
    Download a list of bz2 files, uncompress to corresponding list of paths
    """
    for url, path in zip(urls, paths):
        if verbose:
            print("downloading", url)

        download_bz2(url=url,
                     path=path,
                     verbose=verbose)