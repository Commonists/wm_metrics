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

    # All quarters
    quarters = [commons_cat_metrics.CommonsCatMetrics(category, fdc_round, i+1, cursor=db_cursor) for i in range(4)]

    # retrieving values from metrics object
    files = [quarters[i].get_nb_files() for i in range(4)]
    labels = [100*float(quarters[i].get_nb_featured_files())/float(files[i]) for i in range(4)]
    uploaders = [quarters[i].get_nb_uploaders() for i in range(4)]
    uploaders.append(total_uploaders_period(fdc_round, category, db_cursor))
	# total uploaders on the period



    # Creating reporting
    nb_file = fdc.Indicator("nb", q1=files[0], q2=files[1], q3=files[2], q4=files[3], value=files[0]+files[1]+files[2]+files[3])
    pct_labels = fdc.Indicator("featured",
                               q1=round(labels[0], 2), q2=round(labels[1], 2),
                               q3=round(labels[2], 2), q4=round(labels[3], 2),
                               value=round((labels[0]*files[0]+labels[1]*files[1]+labels[2]*files[2]+labels[3]*files[3])/(nb_file.values['value']), 2))
    nb_labels = fdc.Indicator("nb_featured",
                               q1=int(round(labels[0]*files[0])/100), q2=int(round(labels[1]*files[1])/100),
                               q3=int(round(labels[2]*files[2])/100), q4=int(round(labels[3]*files[3])/100),
                               value=int(round(labels[0]*files[0]+labels[1]*files[1]+labels[2]*files[2]+labels[3]*files[3])/100)
    	)
    nb_uploader = fdc.Indicator("uploaders",
    							q1=uploaders[0],
    							q2=uploaders[1],
    							q3=uploaders[2],
    							q4=uploaders[3],
    							value=uploaders[4]
    	)
    report = fdc.Report([nb_file, pct_labels, nb_uploader, nb_labels], template_string=template_photo)
    report.generate()

    # Ending mysql
    db_cursor.close()
    db.close()

def total_uploaders_period(fdc_round, category, db_cursor):
	"""Quick uploaders on entire period indicator"""
	import wmflabs_queries

	cat = category.replace(" ", "_")
	query = wmflabs_queries.count_uploaders_in_category(cat, fdc_round.full_period()['start'] , fdc_round.full_period()['end'])
	db_cursor.execute(query)
	return long(db_cursor.fetchone()[0])


def main():
    # FDC round
    fdc_round = fdc.Round(2012, 2013, 2)

    # Category used
    category = "Media supported by Wikimedia France"
    make_example_report(fdc_round, category)


if __name__ == "__main__":
    main()
