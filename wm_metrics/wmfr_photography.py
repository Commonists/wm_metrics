# -*- coding: utf-8 -*-
import fdc
import commons_cat_metrics

# Output template
template_photo = """
{{Suivi FDC/En-tête}}
{{Suivi FDC/Groupe|groupe=Soutien aux photographes}}
{{Suivi FDC/Indicateur|indicateur=Nombre de fichiers mis en ligne|q1= ${nb_q1} |q2= ${nb_q2} |q3= ${nb_q3} |q4= ${nb_q4} |cumul= ${nb_value}|Objectif=9000}}
{{Suivi FDC/Indicateur|indicateur=% de fichiers mis en ligne et ayant reçu un label|q1=|q2=|q3=|q4=|cumul=|Objectif=5%}}
{{Suivi FDC/Fin}}
"""

# FDC round
fdc_round = fdc.Round(2012, 2013, 2)

# Category used
category = "Media supported by Wikimedia France"

# Quick and dirty metrics object
quarters = [commons_cat_metrics.CommonsCatMetrics(category, fdc_round, i+1) for i in range(4)]

# retrieving values from metrics object
files = [quarters[i].get_nb_files() for i in range(4)]
labels   = [float(quarters[i].get_nb_featured_files())/float(files[i]) for i in range(4)]

# Creating reporting
nb_file   = fdc.Indicator("nb", q1=files[0], q2=files[1], q3=files[2], q4=files[3], value=files[0]+files[1]+files[2]+files[3])
pct_labels= fdc.Indicator("nb", q1=labels[0], q2=labels[1], q3=labels[2], q4=labels[3], value=(labels[0]*files[0]+labels[1]*files[1]+labels[2]*files[2]+labels[3]*files[3])/(nb_file.values['value']))
report    = fdc.Report([nb_file], template_string=template_photo)

report.generate()
