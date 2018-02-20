"""
TODO: docstrings
"""

from os.path import join, dirname, abspath

# Hopefully this url never changes
REMOTE_BASE = "http://files.pushshift.io/reddit/"

# If you decide to store data somewhere other than
# reddit-network-analysis/reddit/data put your path here
LOCAL_BASE = dirname(abspath(__file__))

LOCAL_COMMENTS_DIR = join(LOCAL_BASE, "comments")
LOCAL_THREADS_DIR = join(LOCAL_BASE, "threads")

# Comments and threads will be downloaded from these locations
REMOTE_COMMENTS_FMT_STR = join(REMOTE_BASE, "comments", "RC_{}.bz2")
REMOTE_THREADS_FMT_STR = join(REMOTE_BASE, "submissions", "RS_{}.bz2")

# Comments and threads will be stored locally to these locations
LOCAL_COMMENTS_FMT_STR = join(LOCAL_COMMENTS_DIR, "RC_{}.json")
LOCAL_THREADS_FMT_STR = join(LOCAL_THREADS_DIR, "RS_{}.json")
