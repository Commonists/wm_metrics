"""Unit tests for cat2cohort."""

import unittest
from wm_metrics.cat2cohort import api_url


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
