import swear_word_set_getter
from gensim import corpora


def get_swear_dictionary_key_map():
    swear_set = swear_word_set_getter.get_swear_word_set()
    dictionary = corpora.Dictionary.load("gensim_dictionary")

    word_key_map = {}

    for key, value in dictionary.iteritems():
        if value in swear_set:
            word_key_map[value] = key

    return word_key_map