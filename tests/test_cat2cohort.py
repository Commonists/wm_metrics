"""Unit tests for cat2cohort."""

import unittest
from wm_metrics.cat2cohort import api_url, _make_CSV_line


class TestCat2Cohort(unittest.TestCase):

    """Test methods from Cat2Cohort."""

    def test_api_url(self):
        """Test api_url."""
        values = [
            ('fr', 'https://fr.wikipedia.org/w/api.php'),
            ('en', 'https://en.wikipedia.org/w/api.php'),
        ]
        for value, expected in values:
            self.assertEqual(api_url(value), expected)

    def test_make_CSV_line(self):
        """Test _make_CSV_line."""
        values = [
            (('Toto', 'fr'), 'Toto, frwiki'),
            (('Titi', 'en'), 'Titi, enwiki'),
        ]
        for value, expected in values:
            self.assertEqual(_make_CSV_line(*value), expected)
