import string
from collections import Counter
from typing import Iterable

from nltk import ngrams


def initialize_grams() -> tuple[Counter, Counter, Counter]:
    """Helper function to initialize Counters to avoid boilerplate"""
    unigrams = Counter()
    bigrams = Counter()
    trigrams = Counter()
    return unigrams, bigrams, trigrams


def update_grams(words: list[str], unigrams: Counter, bigrams: Counter,
                 trigrams: Counter) -> tuple[Counter, Counter, Counter]:
    """Helper function to update Counter values to avoid boilerplate"""
    unigrams.update(words)
    bigrams.update(ngrams(words, 2))
    trigrams.update(ngrams(words, 3))
    return unigrams, bigrams, trigrams


def clean_token_list(words: Iterable[str]) -> list[str]:
    """Strips terminal punctuation from words"""
    # not doing stopword cleaning because we want multi-word phrases.
    # Warning that this might remove corrupt leet-speak like keywords
    # A fictional example might be something like @u$o<> (would become just u$o)
    return [
        word.lower().strip(string.whitespace + string.punctuation)
        for word in words
    ]


def return_list_of_first_item(
        *args: Iterable[tuple[str, ...]]) -> tuple[list[str], ...]:
    """A function to extract only the first item from a record in a container of containers"""
    processed_args: list[str] = []
    for lst in args:
        only_first = [i[0] for i in lst]
        processed_args.append(only_first)
    return *processed_args,
