"""Unit tests for Dump analysing stuff."""

import unittest
from datetime import date
from analyse_commons_dump import get_categories_from_text,\
    parse_xml_dump,\
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
            ('2005-07-23T01:36:22Z', date(2005, 7, 23)),
        ]
        for value, expected in values:
            self.assertEqual(timestamp_to_date(value), expected)

    def test_parse_xml_dump(self):
        """Test parse_xml_dump."""
        example_dump = 'data/example_dump.xml'
        results = parse_xml_dump(example_dump)
        expected = [
            (u'Kale', date(2005, 7, 23), u'File:Example.jpg'),
            (u'Steinsplitter', date(2013, 5, 1), u'File:Example.jpg'),
            (u'Steinsplitter', date(2013, 5, 1), u'File:Example.jpg'),
            (u'Trijnstel', date(2013, 5, 31), u'File:Example.jpg'),
            (u'Perhelion', date(2013, 4, 23), u'File:Example en.svg'),
            ('', date(2013, 9, 19), u'File:Example en.svg'),
            ('', date(2013, 9, 26), u'File:Example en.svg'),
            (u'Jafeluv', date(2013, 9, 26), u'File:Example en.svg')
        ]
        self.assertEqual(results, expected)


if __name__ == '__main__':
    unittest.main()
