# -*- coding: utf-8 -*-

"""FDC module dealing with quarter."""

import time
from string import Template


class Round:

    """
    FDC Round allows to compute accurate timestamps for start and end of each quarter of the round.

    start and end timestamp are returned as a dictionnary of string { 'start': "...", 'end': "..." }
    """

    QUARTER = [
        {'start': "0101000000", 'end': "0331235959"},
        {'start': "0401000000", 'end': "0630235959"},
        {'start': "0701000000", 'end': "0930235959"},
        {'start': "1001000000", 'end': "1231235959"}
    ]

    def __init__(self, year1, year2, round_number):
        """Constructor.

        Args:
                year1 (int): Year of request of round 1
                year2 (int): Year of request of round 2
                round_number (int): FDC round number,
                        either 1 for round 1 and 2 for round 2

        Raises:
                ValueError: if round is not 1 or 2
        """
        self.year1 = year1
        self.year2 = year2
        if round_number in [1, 2]:
            self.round = round_number
        else:
            raise ValueError(
                "Round number should be either 1 or 2 but is %d" % round_number)

    def quarter(self, quarter):
        """Returns the timestamp of start and end of the quarter.

        Args:
                quarter (int): Number of the quarter (values are between 1 and 4)

        Returns:
                both timestamp of start and end of the quarter as {'start': "XXX", 'end': "YYY"}

        Raises:
                ValueError: if quarter is not in 1..4
        """
        year = self.year2
        index = quarter - 1
        if not quarter in range(1, 5):
            raise ValueError(
                "quarter should be between 1 and 4 but is %d" % quarter)
        if self.round == 2:
            index = (quarter + 1) % 4
            if quarter >= 3:
                year = self.year2 + 1
        return {
            'start': str(year) + Round.QUARTER[index]['start'],
            'end': str(year) + Round.QUARTER[index]['end']}

    def full_period(self):
        """Returns the timestamp of start of the period and the timestamp of end of the period

        Returns:
                both timestamp of start and end of the period as {'start': "XXX", 'end': "YYY"}
        """
        return {
            'start': self.quarter(1)['start'],
            'end': self.quarter(4)['end']
        }

    def _today(self):
        """Returns timestamp of today 0000Z"""
        return time.strftime("%Y%m%d000000", time.gmtime())

    def __repr__(self):
        return "%s-%s round%s" % (self.year1, self.year2, self.round)

    def to_period_for_quarter(self, quarter):
        import period
        fdc_period = self.quarter(quarter)
        time_period = period.Period(fdc_period['start'], fdc_period['end'])
        return time_period


class Indicator:

    """Indicator for FDC reports have values for Q1, Q2, Q3, Q4 or/and a value.
    it allows to follow the evolution of an indicator during the quarters and have its final value
    or to follow an indicator with only a single value.
    """

    def __init__(self, name, q1=None, q2=None, q3=None, q4=None, value=None):
        """Constructor returns an indicator.
        it can be initilized with values for q1, q2, q3, q4 and another value (cumulative)

        Args:
                name (str): Unique name (can be used to refer to the indicator)
                q1 (float): Value at first quarter (optional)
                q2 (float): Value at second quarter (optional)
                q3 (float): Value at third quarter (optional)
                q4 (float): Value at fourth quarter (optional)
                value (float): A value of the indicator that has no relation to a quarter: cumulative value, fixed value, whatever (optional)
        """
        self.name = name
        self.values = dict()
        self.values["q1"] = q1
        self.values["q2"] = q2
        self.values["q3"] = q3
        self.values["q4"] = q4
        self.values["value"] = value


class Report:

    """Report is build from indicator list and template
    and generate a report.
    """

    def __init__(self, indicator_list, template_string=None, template_file=None):
        """ Initialize a report.

        In template variables are named:
                $name_q1, $name_q2 $name_q3, $name_q4, $name_value

        Args:
                indicator_list (list): list of fdc.Indicator
                template_string (str): Template string of the report to use (iff there is no template_file)
                template_file (file): File containing the template string to use to generate the report
        """
        self.template = Template(template_string)
        self.indicator_values = dict()
        if template_string is None and template_file is None:
            raise ValueError(
                "template_string or template_file argument needs to be used.")
        if template_file != None:
            # reads template file
            with open(template_file, 'r') as f:
                self.template = Template(f.read())
        # fill the dictionnary of values
        for indicator in indicator_list:
            for key in indicator.values.keys():
                var_name = "%s_%s" % (indicator.name, key)
                if indicator.values[key] == None:
                    self.indicator_values[var_name] = ""
                else:
                    self.indicator_values[var_name] = indicator.values[key]

    def generate(self):
        """ Generate report from template and indicators.
        """
        return self.template.safe_substitute(self.indicator_values)
