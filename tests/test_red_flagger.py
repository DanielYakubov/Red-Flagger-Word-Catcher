"""Tests various properties of the obscuring/unobscuring functions which are critical to the lib."""

import unittest

from red_flagger.red_flagger import RedFlagger


class TestRedFlagger(unittest.TestCase):

    def setUp(self):
        self.red_flagger = RedFlagger()

    def test_get_wordlist(self):
        self.assertEqual(len(self.red_flagger.get_wordlist()), 1912)
        self.assertEqual(self.red_flagger.get_wordlist(),
                         self.red_flagger._wordlist)

    def test_add_words(self):
        word_1 = "TESTER"
        self.red_flagger.add_words([word_1])
        self.assertIn(word_1, self.red_flagger.get_wordlist())

    def test_remove_words(self):
        # First, adding a mundane word to avoid any hate open in tests.
        word_1 = "TESTER"
        self.red_flagger.add_words([word_1])

        # Removing mundane word.
        self.red_flagger.remove_words([word_1])
        self.assertNotIn(word_1, self.red_flagger.get_wordlist())

        # Case when word was never there.
        word_2 = "Captain America"
        # Calling without explicit test, showing there's no exception.
        self.red_flagger.remove_words([word_2])

        # Removing every word.
        wl = self.red_flagger.get_wordlist()
        self.red_flagger.remove_words(wl)
        self.assertEqual(self.red_flagger.get_wordlist(), [])

    def test_detect_abuse(self):
        # Adding tester words to avoid any hate open in tests.
        words = ["Big Ben", "clocktower", "on-foot"]
        self.red_flagger.add_words(words)

        detected_1 = self.red_flagger.detect_abuse("", return_words=True)
        self.assertEqual(detected_1, [])

        detected_2 = self.red_flagger.detect_abuse(
            "My cat is eating prosciutto.", return_words=True)
        self.assertEqual(detected_2, [])

        detected_3 = self.red_flagger.detect_abuse(
            "My cat is eating prosciutto.", return_words=False)
        self.assertFalse(detected_3)

        detected_4 = self.red_flagger.detect_abuse(
            "Big ben really is something, huh?", return_words=True)
        self.assertEqual(detected_4, ["Big ben"])

        detected_5 = self.red_flagger.detect_abuse(
            "I went to see that clocktower Big Ben, I hate the tube so I go there on-foot.",
            return_words=True)
        self.assertEqual(detected_5, ["clocktower", "Big Ben", "on-foot"])

        detected_6 = self.red_flagger.detect_abuse(
            "Big Ben is a clocktower, well, kind of.", return_words=False)
        self.assertTrue(detected_6)

    def test_get_abuse_vector(self):
        wl = self.red_flagger.get_wordlist()
        self.red_flagger.remove_words(wl)

        words = ["Big Ben", "clocktower", "on-foot"]
        self.red_flagger.add_words(words)
        
        self.assertEqual(len(self.red_flagger.get_abuse_vector("")), len(words))

        no_matches = self.red_flagger.get_abuse_vector("The Eiffel Tower looks great at night")
        self.assertEqual(no_matches, [0, 0, 0])
        
        single_match = self.red_flagger.get_abuse_vector("I can see Big Ben!")
        self.assertEqual(single_match, [1, 0, 0])

        wrong_case = self.red_flagger.get_abuse_vector("I can see big ben!") # Test with changed casing
        self.assertEqual(wrong_case, [1, 0, 0])

        multi_matches = self.red_flagger.get_abuse_vector("My favourite clocktower is Big Ben. I can see that clocktower from my home!")
        self.assertEqual(multi_matches, [1, 2, 0])
