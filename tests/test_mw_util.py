"""Unit tests for cat2cohort."""

import unittest
from mw_util import str2cat


class TestMWutil(unittest.TestCase):

    """Test methods from mw_util."""

    def test_str2cat(self):
        """Test str2cat."""
        values = [
            ('A', 'Category:A'),
            ('Category:B', 'Category:B'),
        ]
        for value, expected in values:
            self.assertEqual(str2cat(value), expected)
