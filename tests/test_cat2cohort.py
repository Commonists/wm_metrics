"""Unit tests for cat2cohort."""

import unittest
from wm_metrics.cat2cohort import api_url, _make_CSV_line, _userlist_to_CSV_cohort


class TestCat2Cohort(unittest.TestCase):

    """Test methods from Cat2Cohort."""

    def setUp(self):
        """Set up the tests."""
        self.userlist = [('Toto', 'fr'), ('Titi', 'en')]
        self.csvlines = ['Toto, frwiki', 'Titi, enwiki']

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
        for value, expected in zip(self.userlist, self.csvlines):
            self.assertEqual(_make_CSV_line(*value), expected)

    def test_userlist_to_CSV_cohort(self):
        """Test _userlist_to_CSV_cohort."""
        expected = '\n'.join(self.csvlines)
        self.assertEqual(_userlist_to_CSV_cohort(self.userlist),
                         expected)


if __name__ == '__main__':
    unittest.main()
