# -*- coding: utf-8 -*-
import fdc
import commons_cat_metrics
import MySQLdb
import _mysql_exceptions

# Output template
template_photo_start = """
== Report  ==
{{Suivi FDC/En-tête}}
{{Suivi FDC/Groupe|groupe=Category analysis}}
"""

nb_files_tmpl = """{{Suivi FDC/Indicateur|indicateur=Number of files online|q1= ${nb_q1} |q2= ${nb_q2} |q3= ${nb_q3} |q4= ${nb_q4} |cumul= ${nb_value}|Objectif=}}
"""
pct_labels_tmpl = """{{Suivi FDC/Indicateur|indicateur=Percentage of highlighted files|q1=${featured_q1}|q2=${featured_q2}|q3=${featured_q3}|q4=${featured_q4}|cumul=${featured_value}|Objectif=}}
"""

nb_labels_tmpl = """{{Suivi FDC/Indicateur|indicateur=Number of highlighted files|q1=${nb_featured_q1}|q2=${nb_featured_q2}|q3=${nb_featured_q3}|q4=${nb_featured_q4}|cumul=${nb_featured_value}|Objectif=}}
"""

nb_uploaders_tmpl = """{{Suivi FDC/Indicateur|indicateur=Number of users|q1=${uploaders_q1}|q2=${uploaders_q2}|q3=${uploaders_q3}|q4=${uploaders_q4}|cumul=${uploaders_value}|Objectif=}}
"""

template_photo_end = """{{Suivi FDC/Fin}}
"""


class WMmetricsException(Exception):
    pass


def make_example_report(fdc_round, category,
                        nb_files_on=True,
                        nb_labels_on=True,
                        nb_uploaders_on=True,
                        pct_labels_on=True):
    """Quick report maker. Indicators can be disabled by passing argument False"""
    # Quick and dirty metrics object
    try:
        db = commons_cat_metrics.get_commons_db()
        db_cursor = db.cursor()

        # Metrics
        metrics = commons_cat_metrics.Indicators(
            category, fdc_round, cursor=db_cursor)
        # Init indicators with None so they can be enabled/disabled by option
        nb_files = None
        nb_labels = None
        nb_uploaders = None
        pct_labels = None
        template_photo = template_photo_start
        # Retrieving all indicators
        if nb_files_on:
            nb_files = metrics.nb_files_indicator("nb")
            template_photo += nb_files_tmpl
        if nb_labels_on:
            nb_labels = metrics.nb_labels_indicator("nb_featured")
            template_photo += nb_labels_tmpl
        if nb_uploaders_on:
            nb_uploaders = metrics.nb_uploaders_indicator("uploaders")
            template_photo += nb_uploaders_tmpl
        if pct_labels_on:
            pct_labels = metrics.pct_labels_indicator("featured")
            template_photo += pct_labels_tmpl
        template_photo += template_photo_end

        # List of indicators selected
        list_of_indicators = [indicator for indicator in [
            nb_files, pct_labels, nb_uploaders, nb_labels] if indicator is not None]

        report = fdc.Report(list_of_indicators, template_string=template_photo)
        fdc_report = report.generate()

        # Ending mysql
        db_cursor.close()
        db.close()
        return fdc_report
    except _mysql_exceptions.OperationalError:
        raise WMmetricsException("Problem with database connection")


def main():
    # FDC round
    fdc_round = fdc.Round(2012, 2013, 2)

    # Category used
    category = "Media supported by Wikimedia France"
    print make_example_report(fdc_round, category, nb_files_on=True, nb_labels_on=False, nb_uploaders_on=False, pct_labels_on=False)


if __name__ == "__main__":
    main()
