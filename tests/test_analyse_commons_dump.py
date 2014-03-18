"""Unit tests for Dump analysing stuff."""

import unittest
from os.path import dirname, join
from datetime import datetime
from wm_metrics.analyse_commons_dump import get_categories_from_text,\
    timestamp_to_date


class TestAnalyseCommonsDump(unittest.TestCase):

    def test_get_categories_from_text(self):
        """Test get_categories_from_text."""
        values = [
            ('None', []),
            ('[[Category:A]]', ['A']),
            ('[[Category:A]] [[Category:B C]]', ['A', 'B C']),
        ]
        for value, expected in values:
            self.assertEqual(get_categories_from_text(value), expected)

    def test_timestamp_to_date(self):
        """Test timestamp_to_date."""
        values = [
            ('2005-07-23T01:36:22Z', datetime(2005, 7, 23, 1, 36, 22)),
        ]
        for value, expected in values:
            self.assertEqual(timestamp_to_date(value), expected)


if __name__ == '__main__':
    unittest.main()
