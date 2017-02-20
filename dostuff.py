import json
import paths
import networkx
import get_thread_trees

# This file is a sandbox for work in progress

# Optionally pass a string argument with the subreddit into get_thread_trees
thread_map, comment_map = get_thread_trees.get_thread_trees()

count = 0
for head in sorted(thread_map):
    if head != "t3_5yba3":
        continue
    print()
    print(head, comment_map[thread_map[head]["children_ids"][0]]["comment"]["subreddit"])
    comment = comment_map[thread_map[head]["children_ids"][0]]["comment"]
    comment_ids = list(thread_map[head]["children_ids"])
    past_levels = [1]*len(thread_map[head]["children_ids"])
    curr_level = 1

    while len(comment_ids) > 0:
        comment_id = comment_ids.pop(0)
        level = past_levels.pop(0)
        print(">>>>"*level, comment_id, comment_map[comment_id]["comment"]["author"])
        print("----"*level, comment_map[comment_id]["comment"]["body"].replace("\n", ""))
        comment_ids[0:0] = comment_map[comment_id]["children_ids"]
        past_levels[0:0] = [level+1]*len(comment_map[comment_id]["children_ids"])

    break

print(len(thread_map), len(comment_map))


# swear_file_path = paths.get_profanity_file_name()
#
# with open(swear_file_path, 'r') as swear_word_map_file:
#     swear_word_map = json.load(swear_word_map_file)

# # This is a naive way of counting swears. Consider faster less exact regex.
# for key in swear_word_map:
#     for word in swear_word_map[key]:
#         n_swears = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), comment["body"]))
