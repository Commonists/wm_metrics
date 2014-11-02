# -*- coding: latin-1 -*-
import os
import sys
import logging
from flask import Flask, render_template, request
from logging.handlers import RotatingFileHandler

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(current_dir, '..'))

from wm_metrics import fdc
from wm_metrics import wmfr_photography
from wm_metrics import commons_cat_metrics
from wm_metrics import category_induced
from wm_metrics import mw_util

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/fdc")
def fdc_report_page():
    return render_template('fdc-report.html')


@app.route("/category-induced")
def category_induced_page():
    return render_template('category-induced.html')


@app.route("/fdc/submit", methods=["POST"])
def compute_fdc_report():
    category = request.form['category']
    fdc_year = int(request.form['year'])
    round_num = int(request.form['round'])
    prefix = "Category:"
    if not category:
        return render_template('error.html', message='No category provided')
    if category.startswith(prefix):
        category = category[len(prefix):]

    app.logger.info('FDC report %s-%s on %s' % (fdc_year, round_num, category))

    nb_uploaders_on = 'indicator-uploaders' in request.form
    nb_files_on = 'indicator-files' in request.form
    nb_labels_on = 'indicator-highlighted' in request.form
    pct_labels_on = 'indicator-highlighted_percentage' in request.form

    fdc_round = fdc.Round(fdc_year-1, fdc_year, round_num)
    results = 'Nothing'
    try:
        results = wmfr_photography.make_example_report(fdc_round, category,
                        nb_files_on=nb_files_on,
                        nb_labels_on=nb_labels_on,
                        nb_uploaders_on=nb_uploaders_on,
                        pct_labels_on=pct_labels_on)

    except wmfr_photography.WMmetricsException, e:
        message = 'Something went wrong in Wm_metrics: ' + e.message
        return render_template('error.html', message=message)
    try:
        return render_template('fdc-report-results.html',
                               category=category,
                               fdc_round=fdc_round,
                               contents=results.decode('utf-8'))
    except UnicodeDecodeError, e:
        return render_template('error.html', message='Unicode error')
    except Exception, e:
        return render_template('error.html', message=e)


@app.route("/category-induced/submit", methods=["POST"])
def compute_category_induced():
    category = mw_util.str2cat(request.form['category'])
    app.logger.info('CategoryInduced on %s' % (category))
    try:
        ci = category_induced.CategoryInduced(category)
        ci.categories = ci.list_category()
        first_images = [ci.first_image(x) for x in ci.categories]
        first_images.sort()
        categories_count = len(first_images)
        images = [x.decode('utf-8')[5:].replace(" ", "_") for x in ci.list_images()]
        images_count = len(images)
        result = [first_images[x][0] for x in range(len(first_images))
                  if (len(first_images[x][1]) > 0
                      and first_images[x][1][0] in images)]
        result.sort()
        results_count = len(result)
        categories_traversed_count = len(first_images)
        contents = '\n'.join(result)
        return render_template('category-induced-result.html',
                               category=category,
                               images_count=images_count,
                               categories_count=categories_count,
                               results_count=results_count,
                               contents=contents)
    except Exception, e:
        return render_template('error.html', message=e)


@app.errorhandler(404)
def page_not_found(error):
    message = "Page does not exist."
    return render_template('error.html', message=message), 404


if __name__ == "__main__":
    handler = RotatingFileHandler('usage.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
