from os.path import dirname, abspath

# Hopefully this url never changes
REMOTE_BASE = "http://files.pushshift.io/reddit/"

# If you decide to store data somewhere other than reddit-network-analysis/data
# put your path here
LOCAL_BASE = "/Volumes/Wanton/"
LOCAL_BASE = dirname(abspath(__file__))