# -*- coding: utf-8 -*-
#!/usr/bin/python

"""Unit tests for traffic statistics stuff."""

import unittest
from wm_metrics.traffic_statistics import Traffic


class TestTraffic(unittest.TestCase):

    """Test Traffic class."""

    def test_make_url(self):
        """Test _make_url()."""
        traffic = Traffic('France', 'fr')
        result = traffic._make_url(2013, 01)
        expected = 'http://stats.grok.se/json/fr/201301/France'
        self.assertEqual(result, expected)

    def test_make_latest_url(self):
        """test _make_latest_url()."""
        traffic = Traffic('France', 'fr')
        result = traffic._make_latest_url(90)
        expected = 'http://stats.grok.se/json/fr/latest90/France'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
