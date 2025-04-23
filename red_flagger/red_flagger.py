import os.path
import re
from typing import Union
from collections import Counter

from red_flagger.obscure_data import unobscure


class RedFlagger:
    DATA_DIR = os.path.join(os.path.dirname(__file__),
                            "data/toxic_keywords_b16.txt")

    def __init__(self):
        self._wordlist = self._load_wordlist()
        self._regex_wordlist = self._load_wordlist_regex(self._wordlist)

    def _load_wordlist(self) -> list[str]:
        """Load in the wordlist from the encoded base16 file."""
        with open(self.DATA_DIR, "rb") as word_list_file:
            return [unobscure(word) for word in word_list_file]

    def _load_wordlist_regex(self, word_list: list[str]) -> str:
        """Convert the wordlist to a regular expression."""
        escaped_word_list = [fr"\b{re.escape(w)}\b" for w in word_list]
        return "|".join(escaped_word_list)

    def get_wordlist(self) -> list[str]:
        """Returns the currently loaded in list of words."""
        return self._wordlist.copy()

    def add_words(self, words: list[str]) -> None:
        """Extend the wordlist with new words. This re-triggers duplication and overlap checking."""
        # TODO dupe & overlap filtering (borrow from data_building)
        self._wordlist.extend(words)
        # Updating the regex.
        self._regex_wordlist = self._load_wordlist_regex(self._wordlist)

    def remove_words(self, words_to_remove: list[str]) -> None:
        """Removes words from the configured wordlist. Removed words will no longer be used in
        future detect_abuse calls."""
        self._wordlist = [w for w in self._wordlist if w not in words_to_remove]
        # Updating the regex.
        self._regex_wordlist = self._load_wordlist_regex(self._wordlist)

    def detect_abuse(self,
                     document: str,
                     return_words: bool = True) -> Union[list[str], bool]:
        """Uses the internal wordlist to detect harmful words.

         If return_words is True, it returns a list of the detected words.
         Otherwise, a boolean representing if there were any terms in the list is returned.
        """
        if return_words:
            return re.findall(self._regex_wordlist,
                              document,
                              flags=re.IGNORECASE)
        return bool(re.search(self._regex_wordlist, document, flags=re.IGNORECASE))
    
    def get_abuse_vector(self, document: str) -> list[int]:
        """Creates a vector with the counts of each word in the wordlist.
        We have to convert input to lowercase as `detect_abuse` returns a list of words matching their original casing.
        """
        abuse_words = self.detect_abuse(document.lower())
        word_counts = Counter(abuse_words)
        return [word_counts[w] for w in self.get_wordlist()]

