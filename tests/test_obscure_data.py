"""Tests various properties of the obscuring/unobscuring functions."""

import unittest

from red_flagger.obscure_data import obscure, unobscure


class TestObscureData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.simple_str = "Hello World!"
        cls.simple_b16 = b"eNr7_8-DIZUhBwjzGRQYwoFkEZCdwqDIAABrSAY7"
        cls.leet_str = "H377o W()\rld<>"
        cls.leet_b16 = b"eNr7_8-DwZjBHAjzGRQYwhk0GDQZeBlyGFIYbBjsGABt1AV1"

    def test_obscure(self):
        obscured = obscure(self.simple_str)
        self.assertEqual(obscured, self.simple_b16)

        # String conversion equivalence.
        self.assertEqual(
            obscured.decode("utf-8"), self.simple_b16.decode("utf-8")
        )

        # Harder case with strange symbols.
        obscured = obscure(self.leet_str)
        self.assertEqual(obscured, self.leet_b16)

    def test_unobscure(self):
        unobscured = unobscure(self.simple_b16)
        self.assertEqual(unobscured, self.simple_str)

        # Harder case with strange symbols.
        unobscured = unobscure(self.leet_b16)
        self.assertEqual(unobscured, self.leet_str)

    def test_reversibility(self):
        self.assertEqual(unobscure(obscure(self.simple_str)), self.simple_str)
        self.assertEqual(unobscure(obscure(self.leet_str)), self.leet_str)

        self.assertEqual(obscure(unobscure(self.simple_b16)), self.simple_b16)
        self.assertEqual(obscure(unobscure(self.leet_b16)), self.leet_b16)

    def test_obscure_determinism(self):
        self.assertEqual(obscure(self.simple_str), obscure(self.simple_str))
        self.assertEqual(obscure(self.leet_str), obscure(self.leet_str))

    def test_unobscure_determinism(self):
        self.assertEqual(
            unobscure(self.simple_b16), unobscure(self.simple_b16)
        )
        self.assertEqual(unobscure(self.leet_b16), unobscure(self.leet_b16))
