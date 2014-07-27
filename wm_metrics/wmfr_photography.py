# -*- coding: utf-8 -*-
import fdc
import commons_cat_metrics
import MySQLdb

# Output template
template_photo = """
== Indicateur avec pourcentages ==
{{Suivi FDC/En-tête}}
{{Suivi FDC/Groupe|groupe=Soutien aux photographes}}
{{Suivi FDC/Indicateur|indicateur=Nombre de fichiers mis en ligne|q1= ${nb_q1} |q2= ${nb_q2} |q3= ${nb_q3} |q4= ${nb_q4} |cumul= ${nb_value}|Objectif=9000}}
{{Suivi FDC/Indicateur|indicateur=% de fichiers mis en ligne et ayant reçu un label|q1=${featured_q1}|q2=${featured_q2}|q3=${featured_q3}|q4=${featured_q4}|cumul=${featured_value}|Objectif=5%}}
{{Suivi FDC/Indicateur|indicateur=Nombre d'utilisateurs|q1=${uploaders_q1}|q2=${uploaders_q2}|q3=${uploaders_q3}|q4=${uploaders_q4}|cumul=${uploaders_value}|Objectif=80}}
{{Suivi FDC/Fin}}

== Indicateurs sans pourcentages ==

{{Suivi FDC/En-tête}}
{{Suivi FDC/Groupe|groupe=Soutien aux photographes}}
{{Suivi FDC/Indicateur|indicateur=Nombre de fichiers mis en ligne|q1= ${nb_q1} |q2= ${nb_q2} |q3= ${nb_q3} |q4= ${nb_q4} |cumul= ${nb_value}|Objectif=9000}}
{{Suivi FDC/Indicateur|indicateur=Nombre de fichiers mis en ligne et ayant reçu un label|q1=${nb_featured_q1}|q2=${nb_featured_q2}|q3=${nb_featured_q3}|q4=${nb_featured_q4}|cumul=${nb_featured_value}|Objectif=450}}
{{Suivi FDC/Indicateur|indicateur=Nombre d'utilisateurs|q1=${uploaders_q1}|q2=${uploaders_q2}|q3=${uploaders_q3}|q4=${uploaders_q4}|cumul=${uploaders_value}|Objectif=80}}
{{Suivi FDC/Fin}}
"""


def make_example_report(fdc_round, category):
    """Quick report maker"""
    # Quick and dirty metrics object
    db = commons_cat_metrics.get_commons_db()
    db_cursor = db.cursor()

    # Metrics
    commons_cat_metrics.Indicators(category, fdc_round, cursor=db_cursor)
    # Retrieving all indicators
    nb_files = commons_cat_metrics.nb_files_indicator("nb")
    nb_labels = commons_cat_metrics.nb_labels_indicator("nb_featured")
    nb_uploaders = commons_cat_metrics.nb_uploaders_indicator("uploaders")
    pct_labels = commons_cat_metrics.pct_uploaders_indicator("featured")

    report = fdc.Report([nb_files, pct_labels, nb_uploaders, nb_labels], template_string=template_photo)
    report.generate()

    # Ending mysql
    db_cursor.close()
    db.close()


def main():
    # FDC round
    fdc_round = fdc.Round(2012, 2013, 2)

    # Category used
    category = "Media supported by Wikimedia France"
    make_example_report(fdc_round, category)


if __name__ == "__main__":
    main()
