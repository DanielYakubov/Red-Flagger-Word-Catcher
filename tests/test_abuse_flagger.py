"""Tests various properties of the obscuring/unobscuring functions which are critical to the lib."""

import unittest

from abuse_flagger.abuse_flagger import AbuseFlagger


class TestObscureData(unittest.TestCase):

    def setUp(self):
        self.abuse_flagger = AbuseFlagger()

    def test_get_wordlist(self):
        self.assertEqual(len(self.abuse_flagger.get_wordlist()), 1912)
        self.assertEqual(self.abuse_flagger.get_wordlist(),
                         self.abuse_flagger._wordlist)

    def test_add_words(self):
        word_1 = "TESTER"
        self.abuse_flagger.add_words([word_1])
        self.assertIn(word_1, self.abuse_flagger.get_wordlist())

    def test_remove_words(self):
        # First, adding a mundane word to avoid any hate open in tests.
        word_1 = "TESTER"
        self.abuse_flagger.add_words([word_1])

        # Removing mundane word.
        self.abuse_flagger.remove_words([word_1])
        self.assertNotIn(word_1, self.abuse_flagger.get_wordlist())

        # Case when word was never there.
        word_2 = "Captain America"
        # Calling without explicit test, showing there's no exception.
        self.abuse_flagger.remove_words([word_2])

        # Removing every word.
        wl = self.abuse_flagger.get_wordlist()
        self.abuse_flagger.remove_words(wl)
        self.assertEqual(self.abuse_flagger.get_wordlist(), [])

    def test_detect_abuse(self):
        # Adding tester words to avoid any hate open in tests.
        words = ["Big Ben", "clocktower", "on-foot"]
        self.abuse_flagger.add_words(words)

        detected_1 = self.abuse_flagger.detect_abuse("", return_words=True)
        self.assertEqual(detected_1, [])

        detected_2 = self.abuse_flagger.detect_abuse(
            "My cat is eating prosciutto.", return_words=True)
        self.assertEqual(detected_2, [])

        detected_3 = self.abuse_flagger.detect_abuse(
            "My cat is eating prosciutto.", return_words=False)
        self.assertFalse(detected_3)

        detected_4 = self.abuse_flagger.detect_abuse(
            "Big ben really is something, huh?", return_words=True)
        self.assertEqual(detected_4, ["Big ben"])

        detected_5 = self.abuse_flagger.detect_abuse(
            "I went to see that clocktower Big Ben, I hate the tube so I go there on-foot.",
            return_words=True)
        self.assertEqual(detected_5, ["clocktower", "Big Ben", "on-foot"])

        detected_6 = self.abuse_flagger.detect_abuse(
            "Big Ben is a clocktower, well, kind of.", return_words=False)
        self.assertTrue(detected_6)
