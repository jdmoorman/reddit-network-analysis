import get_thread_trees
import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", message="pyplot.hold is deprecated")
warnings.filterwarnings("ignore", message="axes.hold is deprecated")

# This file is a sandbox for work in progress

file_dates = ["2005-12", "2006-01", "2006-02"]
file_pairs = [
    {
        "comments_file_path": ".\\comments\\RC_" + date + ".json",
        "threads_file_path": ".\\submissions\\RS_" + date + ".json"
    } for date in file_dates
]

# Optionally pass a string argument with the subreddit into get_thread_trees
thread_map, comment_map = get_thread_trees.get_thread_trees(file_pairs)

count = 0
for head in sorted(thread_map):
    if thread_map[head].order() < 4:
        continue

    count += 1
    if count > 1:
        break

    nx.draw(thread_map[head])
    plt.show()

    print(thread_map[head].successors(head))

    # print()
    # print(head, thread_map[head]["thread"]["subreddit"], thread_map[head])
    # comment_ids = list(thread_map[head]["children_ids"])
    # past_levels = [1]*len(thread_map[head]["children_ids"])
    # curr_level = 1
    #
    # while len(comment_ids) > 0:
    #     comment_id = comment_ids.pop(0)
    #     level = past_levels.pop(0)
    #     print(">>>>"*level,
    # comment_id, comment_map[comment_id]["comment"]["author"], comment_map[comment_id]["comment"])
    #     print("----"*level, comment_map[comment_id]["comment"]["body"].replace("\n", ""))
    #     comment_ids[0:0] = comment_map[comment_id]["children_ids"]
    #     past_levels[0:0] = [level+1]*len(comment_map[comment_id]["children_ids"])

print(len(thread_map), len(comment_map))

# swear_file_path = paths.get_profanity_file_name()
#
# with open(swear_file_path, 'r') as swear_word_map_file:
#     swear_word_map = json.load(swear_word_map_file)

# # This is a naive way of counting swears. Consider faster less exact regex.
# for key in swear_word_map:
#     for word in swear_word_map[key]:
#         n_swears = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), comment["body"]))
