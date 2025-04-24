"""Tests various properties of the util functions which are critical to the lib."""

import unittest

from red_flagger.utils import filter_overlaps_and_sort


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.wordlist = [
            "cat", "cats", "a cat", "a cat catches mice",
            "The groom waited at the altar", "Cats groom", "dog",
            "The Cat Napped", "the Cat caught a mouse", "a dog chased the bus",
            "the Dog caught the cat", "the cat",
            "The groom waited at the altar"
        ]

    def test_filter_overlaps_and_sort(self):
        """Cat,dog,and cats are unigrams so any multigram containing them should be filtered out. Duplicates also filtered"""
        expected_result = [
            "cat", "cats", "dog", "the groom waited at the altar"
        ]
        actual_result = filter_overlaps_and_sort(self.wordlist)
        self.assertEqual(expected_result, actual_result)
