"""Utility functions for red flagger"""

def filter_overlaps_and_sort(word_list: list[str]) -> list[str]:
    """Filters the word list to ensure items are unique within the word list.

    Filtering happens in two steps:
    1) All the single gram items are extracted into a list, iff they are unique to the list. Multi-words are stored.
    2) The multi-word container is iterated and added to the unique words list iff the multi-words do not contain
        existing single words.

    This algorithm also pseudo-sorts the list. First, all the unigrams are listed, then the multiword items.
    """
    # NOT using a set here, want to be careful about determinism & insertion order.
    unique_words: list[str] = []
    multi_words: list[tuple[str, str, ...]] = []

    # gets unigrams
    split_word_list = [x.split() for x in word_list]
    [unique_words.append(x[0]) for x in split_word_list if len(x) == 1 and x[0] not in unique_words]
    [multi_words.append(x) for x in split_word_list if len(x) > 1 and x not in multi_words]

    # checks for overlap with longer sequences, appends to unique if not in unique
    good_multi = [multi_word_tuple for multi_word_tuple in multi_words if all([word not in unique_words for word in multi_word_tuple])]
    [unique_words.append(" ".join(x)) for x in good_multi]

    return unique_words
