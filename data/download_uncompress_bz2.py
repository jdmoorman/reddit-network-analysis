"""
TODO: docstrings
TODO: consider leaving files compressed until you need to read them.
TODO: add requests library to dependencies
"""

from __future__ import print_function

import requests
import bz2

def get_bz2(url=None, path=None):
    print("downloading", url)
    r = requests.get(url, stream=True)
    with open(path, 'wb') as out_file:
        decompressor = bz2.BZ2Decompressor()
        try:
            # TODO: is this chunk size reasonable?
            for chunk in r.iter_content(chunk_size=100*1024):
                if chunk:
                    out_file.write(decompressor.decompress(chunk))
        except (OSError, IOError) as e:
            # This typically occurs when a requested file is not on the server.
            # Check that a file exists at the given url.
            print("Remote file not found. Writing empty file.")
