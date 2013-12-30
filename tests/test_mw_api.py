"""Unit tests for mw_api."""

import unittest
from wm_metrics.mw_api import MwApi, MwApiQuery


class TestMwApi(unittest.TestCase):

    """Test MwApi."""

    def test_MwApi_constructor_default(self):
        """Test MwApi constructor with default values."""
        mw_api = MwApi('test')
        expected = {'action': 'test',
                    'prop': {},
                    'format': 'json'
                    }
        self.assertEqual(vars(mw_api), expected)

    def test_MwApi_constructor(self):
        """Test MwApi constructor with custom values."""
        input_properties = {'A': 'a', 'B': 'b'}
        input_format = 'xml'
        mw_api = MwApi('test',
                       properties=input_properties,
                       format=input_format)
        expected = {'action': 'test',
                    'prop': input_properties,
                    'format': input_format
                    }
        self.assertEqual(vars(mw_api), expected)


class TestMwApiQuery(unittest.TestCase):

    """Test MwApiQuery."""

    def test_MwApi_constructor_default(self):
        """Test MwApiQuery constructor with default values."""
        mw_api_query = MwApiQuery()
        expected = {'action': 'query',
                    'prop': {},
                    'format': 'json'
                    }
        self.assertEqual(vars(mw_api_query), expected)

    def test_MwApi_constructor(self):
        """Test MwApiQuery constructor with custom values."""
        input_properties = {'A': 'a', 'B': 'b'}
        input_format = 'xml'
        mw_api_query = MwApiQuery(properties=input_properties,
                                  format=input_format)
        expected = {'action': 'query',
                    'prop': input_properties,
                    'format': input_format
                    }
        self.assertEqual(vars(mw_api_query), expected)
