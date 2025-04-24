"""Utility functions for red flagger"""

import re


def filter_overlaps_and_sort(word_list: list[str]) -> list[str]:
    """Filters the word list to ensure items are unique within the word list.

    Filtering happens in three steps:
    1) All strings from word_list are broken into word lists, then all strings
        are sorted by their word list length, and recombined into the original
        phrase. This sorts the word_list (sorted_word_list) so that unigrams
        are first, followed by bi, and so on.
    2) Every word from the sorted_word_list is compared to every other word in
        the list. If two phrases in the word_list are identical, the index of
        the longer phrase is added to bad indices for later removal. If
        phrase_b contains phrase_a, phrase_b is not unique and its index
        is added to bad indices for later removal.
    3) The bad_indices list from 2 is used to select only the unique phrases
        in sorted_word_list

    This algorithm also pseudo-sorts the list. First, all the unigrams
    are listed, then the multiword items.
    """
    # Breaks up phrases into word lists, sorts list by length of word list,
    # reforms phrase from word lists (now sorted)
    split_word_list = [x.split() for x in word_list]
    split_word_list.sort(key=len)
    sorted_word_list = [" ".join(word) for word in split_word_list]

    # Compare every phrase from word list, only keep the unique words/phrases
    bad_indices: list[int] = []
    for i in range(len(sorted_word_list)):
        for j in range(i + 1, len(sorted_word_list)):
            if i != j:
                # handles dups in the word list (not caught by elif regex)
                if sorted_word_list[i] == sorted_word_list[j]:
                    if i not in bad_indices and j not in bad_indices:
                        bad_indices.append(j)
                elif (
                    re.search(
                        rf"\b{re.escape(sorted_word_list[i])}\b",
                        sorted_word_list[j],
                        flags=re.IGNORECASE,
                    )
                    is not None
                    and j not in bad_indices
                ):
                    bad_indices.append(j)
    unique_wordlist = [
        phrase
        for i, phrase in enumerate(sorted_word_list)
        if i not in bad_indices
    ]
    return unique_wordlist