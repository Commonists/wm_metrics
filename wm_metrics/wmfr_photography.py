# -*- coding: utf-8 -*-
import fdc
import commons_cat_metrics


template_photo = """
{{Suivi FDC/En-tête}}
{{Suivi FDC/Groupe|groupe=Soutien aux photographes}}
{{Suivi FDC/Indicateur|indicateur=Nombre de fichiers mis en ligne|q1= ${nb_q1} |q2= ${nb_q2} |q3= {$nb_q3} |q4= {$nb_q4} |cumul= {$nb.value}|Objectif=9000}}
{{Suivi FDC/Fin}}
"""

fdc_round = fdc.Round(2012, 2013, 2)
category = "Media supported by Wikimedia France"

quarters = [CommonsCatMetrics(category, fdc_round, i+1) for i in range(4)]

files = [quarters[i].get_nb_files() for i in range(4)]

nb_file   = fdc.Indicator("nb", q1=files[0], q2=files[1], q3=files[2], q4=files[3], value=files[0]+files[1]+files[2]+files[3])

report    = fdc.Report([nb_file, uploaders], template_string=template_photo)
report.generate()