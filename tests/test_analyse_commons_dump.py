"""Unit tests for Dump analysing stuff."""

import unittest
from analyse_commons_dump import get_categories_from_text


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


if __name__ == '__main__':
    unittest.main()
