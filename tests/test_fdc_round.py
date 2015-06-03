"""Unit tests for fdc.indicator."""

import unittest
from wm_metrics.fdc.round import Round
from wm_metrics.helpers import period


class TestFdcRound(unittest.TestCase):

    """Test methods from wm_metrics.fdc.indicator."""

    def test_init(self):
        fdc_round = Round(2014, 2015, 1)
        self.assertIsInstance(fdc_round, Round)
        self.assertEquals(fdc_round.year1, 2014)
        self.assertEquals(fdc_round.year2, 2015)

    def test_init_with_wrong_round_number(self):
        """Test that a ValueError is raised with an incorrect round number."""
        with self.assertRaises(ValueError):
            Round(2014, 2015, 3)

    def test_quarter_with_wrong_argument(self):
        """Test that a ValueError is raised with an incorrect quarter number."""
        fdc_round = Round(2014, 2015, 1)
        with self.assertRaises(ValueError):
            fdc_round.quarter(0)
        with self.assertRaises(ValueError):
            fdc_round.quarter(5)

    def test_to_period_for_quarter_returns_period_object(self):
        fdc_round = Round(2014, 2015, 1)
        result = fdc_round.to_period_for_quarter(1)
        self.assertIsInstance(result, period.Period)


class TestFdcFirstRound(unittest.TestCase):

    def setUp(self):
        self.fdc_round = Round(2014, 2015, 1)

    def test_full_period_in_first_round(self):
        result = self.fdc_round.full_period()
        expected = {'start': '20150101000000', 'end': '20151231235959'}
        self.assertEquals(result, expected)

    def test_quarter_one_in_first_round(self):
        result = self.fdc_round.quarter(1)
        expected = {'start': '20150101000000', 'end': '20150331235959'}
        self.assertEquals(result, expected)

    def test_quarter_two_in_first_round(self):
        result = self.fdc_round.quarter(2)
        expected = {'start': '20150401000000', 'end': '20150630235959'}
        self.assertEquals(result, expected)

    def test_quarter_three_in_first_round(self):
        result = self.fdc_round.quarter(3)
        expected = {'start': '20150701000000', 'end': '20150930235959'}
        self.assertEquals(result, expected)

    def test_quarter_four_in_first_round(self):
        result = self.fdc_round.quarter(4)
        expected = {'start': '20151001000000', 'end': '20151231235959'}
        self.assertEquals(result, expected)

    def test_repr_in_first_round(self):
        result = self.fdc_round.__repr__()
        expected = '2014-2015 round1'
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_one_in_first_round(self):
        result = self.fdc_round.to_period_for_quarter(1)
        expected = period.Period('20150101000000', '20150331235959')
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_two_in_first_round(self):
        result = self.fdc_round.to_period_for_quarter(2)
        expected = period.Period('20150401000000', '20150630235959')
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_three_in_first_round(self):
        result = self.fdc_round.to_period_for_quarter(3)
        expected = period.Period('20150701000000', '20150930235959')
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_four_in_first_round(self):
        result = self.fdc_round.to_period_for_quarter(4)
        expected = period.Period('20151001000000', '20151231235959')
        self.assertEquals(result, expected)


class TestFdcSecondRound(unittest.TestCase):

    def setUp(self):
        self.fdc_round = Round(2014, 2015, 2)

    def test_full_period_in_second_round(self):
        result = self.fdc_round.full_period()
        expected = {'start': '20150701000000', 'end': '20160630235959'}
        self.assertEquals(result, expected)

    def test_quarter_one_in_second_round(self):
        result = self.fdc_round.quarter(1)
        expected = {'start': '20150701000000', 'end': '20150930235959'}
        self.assertEquals(result, expected)

    def test_quarter_two_in_second_round(self):
        result = self.fdc_round.quarter(2)
        expected = {'start': '20151001000000', 'end': '20151231235959'}
        self.assertEquals(result, expected)

    def test_quarter_three_in_second_round(self):
        result = self.fdc_round.quarter(3)
        expected = {'start': '20160101000000', 'end': '20160331235959'}
        self.assertEquals(result, expected)

    def test_quarter_four_in_second_round(self):
        result = self.fdc_round.quarter(4)
        expected = {'start': '20160401000000', 'end': '20160630235959'}
        self.assertEquals(result, expected)

    def test_repr_in_second_round(self):
        result = self.fdc_round.__repr__()
        expected = '2014-2015 round2'
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_one_in_second_round(self):
        result = self.fdc_round.to_period_for_quarter(1)
        expected = period.Period('20150701000000', '20150930235959')
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_two_in_second_round(self):
        result = self.fdc_round.to_period_for_quarter(2)
        expected = period.Period('20151001000000', '20151231235959')
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_three_in_second_round(self):
        result = self.fdc_round.to_period_for_quarter(3)
        expected = period.Period('20160101000000', '20160331235959')
        self.assertEquals(result, expected)

    def test_to_period_for_quarter_four_in_second_round(self):
        result = self.fdc_round.to_period_for_quarter(4)
        expected = period.Period('20160401000000', '20160630235959')
        self.assertEquals(result, expected)


if __name__ == '__main__':
    unittest.main()
