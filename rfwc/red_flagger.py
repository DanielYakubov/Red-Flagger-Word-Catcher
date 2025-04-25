import os.path
import re
from typing import Union
from collections import Counter

from .obscure_data import unobscure
from .utils import filter_overlaps_and_sort


class RedFlagger:
    DATA_DIR = os.path.join(
        os.path.dirname(__file__), "data/toxic_keywords_b16.txt"
    )

    def __init__(self):
        self._wordlist = self._load_wordlist()
        self._case_map = {
            word.lower(): word for word in self._wordlist
        }  # Map lowercase items to their original case
        self._regex_wordlist = self._load_wordlist_regex(self._wordlist)

    def _load_wordlist(self) -> list[str]:
        """Load in the wordlist from the encoded base16 file.
        Duplicates may exist in read-in set, so filtering at read in"""
        with open(self.DATA_DIR, "rb") as word_list_file:
            return filter_overlaps_and_sort(
                [unobscure(word) for word in word_list_file]
            )

    def _load_wordlist_regex(self, word_list: list[str]) -> str:
        """Convert the wordlist to a regular expression."""
        escaped_word_list = [rf"\b{re.escape(w)}\b" for w in word_list]
        return "|".join(escaped_word_list)

    def get_wordlist(self) -> list[str]:
        """Returns the currently loaded in list of words."""
        return self._wordlist.copy()

    def add_words(self, words: list[str]) -> None:
        """Extend the wordlist with new words.
        This re-triggers duplication and overlap checking.
        """
        # Now filters and sorts the _wordlist; however, no filtering is
        # performed on words parameter so adjust the case_map update so
        # that it also checks if the word we're trying to add was
        # maintained in the word list after filtering overlaps
        self._wordlist.extend(words)
        self._wordlist = filter_overlaps_and_sort(self._wordlist)
        self._case_map.update(
            {word.lower(): word for word in words if word in self._wordlist}
        )
        # Updating the regex.
        self._regex_wordlist = self._load_wordlist_regex(self._wordlist)

    def remove_words(self, words_to_remove: list[str]) -> None:
        """Removes words from the configured wordlist.
        Removed words will no longer be used in future detect_abuse calls.
        """
        self._wordlist = [
            w for w in self._wordlist if w not in words_to_remove
        ]
        self._case_map = {
            k: v for k, v in self._case_map.items() if k not in words_to_remove
        }
        # Updating the regex.
        self._regex_wordlist = self._load_wordlist_regex(self._wordlist)

    def detect_abuse(
        self, document: str, return_words: bool = True
    ) -> Union[list[str], bool]:
        """Uses the internal wordlist to detect harmful words.

        If return_words is True, it returns a list of the detected words.
        Otherwise, a boolean representing if there were any terms
        in the list returned.
        """
        if return_words:
            matches = re.findall(
                self._regex_wordlist, document, flags=re.IGNORECASE
            )
            return [self._case_map[word.lower()] for word in matches]
        return bool(
            re.search(self._regex_wordlist, document, flags=re.IGNORECASE)
        )

    def get_abuse_vector(self, document: str) -> list[int]:
        """Creates a vector with the counts of each word in the wordlist."""
        abuse_words = self.detect_abuse(document)
        word_counts = Counter(abuse_words)
        return [word_counts[w] for w in self.get_wordlist()]
