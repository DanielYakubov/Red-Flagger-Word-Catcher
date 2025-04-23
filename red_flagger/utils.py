"""Utility functions for red flagger"""


def filter_overlaps_and_sort(word_list: list[str]) -> list[str]:
    """Filters the word list to ensure items are unique within the word list.

    Filtering happens in two steps:
    1) All the single gram items are extracted into a list, iff they are unique to the list. Multi-words are stored.
    2) Multi-words are composed into strings. Each string is compared against every other string, and if the shorter string is
        a sub-string of the longest, the longest is removed from the multi-word (not mult-string) container.
    3) The multi-word container is iterated and added to the unique words list iff the multi-words do not contain
        existing single words.

    This algorithm also pseudo-sorts the list. First, all the unigrams are listed, then the multiword items.
    """
    # NOT using a set here, want to be careful about determinism & insertion order.
    unique_words: list[str] = []
    multi_words: list[tuple[str, str, ...]] = []
    multi_word_strings: list[str] = []

    # gets unigrams, parses phrases (multi words)
    split_word_list = [x.split() for x in word_list]
    [
        unique_words.append(x[0]) for x in split_word_list
        if len(x) == 1 and x[0] not in unique_words
    ]
    [
        multi_words.append(x) for x in split_word_list
        if len(x) > 1 and x not in multi_words
    ]

    #join tuples to form string for easier comparison of multi-word phrases
    [multi_word_strings.append(" ".join(x)) for x in multi_words]
    bad_indices = []

    #I'm sure this could be cleaned up with a list comprehension but my brain is dead atm
    #compare every multi-word string to each other; if one is a substring of the other,append the longer phrase index to remove
    for i in range(len(multi_word_strings)):
        for j in range(len(multi_word_strings)):
            if multi_word_strings[j] in multi_word_strings[
                    i] and i != j and i not in bad_indices:
                bad_indices.append(i)

    #Use the bad indices from earlier comparison to remove phrases from multi-words that are covered by shorter phrase
    #for example "a dog walks" would be removed if "a dog" was part of the same multiword set
    multi_words = [
        multi_word_tuple for i, multi_word_tuple in enumerate(multi_words)
        if i not in bad_indices
    ]
    # checks unigrams in unique against every word in each phrase, stores only phrases with no uni-gram match
    #for example "a dog" would be removed if "dog" was part of the unique word set
    good_multi = [  #checks unigram (unique words) against multi words
        multi_word_tuple for multi_word_tuple in multi_words
        if all([word not in unique_words for word in multi_word_tuple])
    ]

    [unique_words.append(" ".join(x)) for x in good_multi]

    return unique_words
