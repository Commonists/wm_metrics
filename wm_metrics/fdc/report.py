# -*- coding: utf-8 -*-

"""FDC Report."""

from string import Template


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
        if template_file is not None:
            self.template = self._read_template_file(template_file)
        self._fill_indicator_contents(indicator_list)

    def _read_template_file(self, template_file):
        with open(template_file, 'r') as f:
            return Template(f.read())

    def _fill_indicator_contents(self, indicator_list):
        for indicator in indicator_list:
            for key in indicator.values.keys():
                var_name = "%s_%s" % (indicator.name, key)
                if indicator.values[key] is None:
                    self.indicator_values[var_name] = ""
                else:
                    self.indicator_values[var_name] = indicator.values[key]

    def generate(self):
        """ Generate report from template and indicators.
        """
        return self.template.safe_substitute(self.indicator_values)
