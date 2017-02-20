# Your personal path to data should go here
def get_data_directory_path():
    return ".\\comments\\"


# At some point in the future this list should be replaced with a function that iterates
# over the contents of the data directory. For now use it to test on small pieces of the data.
def get_data_file_names():
    return ["RC_2007-10", "RC_2007-11", "RC_2007-12"]



# This path is relative so should never need to change as long as you don't mess with the directory structure.
def get_profanity_file_name():
    return ".\\example_profanity_map.json"
