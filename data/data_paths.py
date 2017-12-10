from base_paths import REMOTE_BASE, LOCAL_BASE
from os.path import join

REMOTE_COMMENTS_FMT_STR = join(REMOTE_BASE, "comments", "RC_{}.bz2")
REMOTE_THREADS_FMT_STR = join(REMOTE_BASE, "submissions", "RS_{}.bz2")

LOCAL_COMMENTS_FMT_STR = join(LOCAL_BASE, "comments", "RC_{}.json")
LOCAL_THREADS_FMT_STR = join(LOCAL_BASE, "submissions", "RS_{}.json")