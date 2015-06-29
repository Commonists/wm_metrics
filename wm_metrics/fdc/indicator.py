"""Indicator model."""


class Indicator(object):

    """Indicator for FDC report.

    Indicator for FDC reports have values for Q1, Q2, Q3, Q4 or/and a value.
    it allows to follow the evolution of an indicator during the quarters and have its final value
    or to follow an indicator with only a single value.
    """

    def __init__(self, name, q1=None, q2=None, q3=None, q4=None, value=None):
        """Constructor returns an indicator.

        it can be initilized with values for q1, q2, q3, q4 and another value
        (cumulative)

        Args:
                name (str): Unique name (can be used to refer to the indicator)
                q1 (float): Value at first quarter (optional)
                q2 (float): Value at second quarter (optional)
                q3 (float): Value at third quarter (optional)
                q4 (float): Value at fourth quarter (optional)
                value (float): A value of the indicator that has no relation to
                    a quarter: cumulative value, fixed value, etc. (optional)
        """
        self.name = name
        self.values = dict()
        self.values["q1"] = q1
        self.values["q2"] = q2
        self.values["q3"] = q3
        self.values["q4"] = q4
        self.values["value"] = value
