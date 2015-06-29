#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""wm_metrics flask webapp module."""

import os
import sys

from flask import Flask, render_template, request

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(current_dir, '..'))

from wm_metrics.fdc.round import Round
from wm_metrics import wmfr_photography
from wm_metrics import category_induced
from wm_metrics import mw_util

app = Flask(__name__)


@app.route("/")
def index():
    """Home page of the wm_metrics tool."""
    return render_template('index.html')


@app.route("/fdc")
def fdc_report_page():
    """Form to create your FDC report."""
    return render_template('fdc-report.html')


@app.route("/category-induced")
def category_induced_page():
    """Form to compute the Category induced."""
    return render_template('category-induced.html')


@app.route("/fdc/submit", methods=["POST"])
def compute_fdc_report():
    """FDC report generation."""
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
    pixel_count_on = 'indicator-pixel-count' in request.form

    fdc_round = Round(fdc_year - 1, fdc_year, round_num)
    results = 'Nothing'
    try:
        results = wmfr_photography.make_example_report(fdc_round, category,
                                                       nb_files_on=nb_files_on,
                                                       nb_labels_on=nb_labels_on,
                                                       nb_uploaders_on=nb_uploaders_on,
                                                       pct_labels_on=pct_labels_on,
                                                       pixel_count_on=pixel_count_on)

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
    """Compute the induced categories."""
    category = mw_util.str2cat(request.form['category'])
    app.logger.info('CategoryInduced on %s' % (category))
    try:
        ci = category_induced.CategoryInduced(category)
        ci.induce_categories()
        contents = '\n'.join(ci.result)
        return render_template('category-induced-result.html',
                               category=category,
                               images_count=ci.images_count,
                               categories_count=ci.categories_traversed_count,
                               results_count=ci.results_count,
                               contents=contents)
    except Exception, e:
        return render_template('error.html', message=e)


@app.errorhandler(404)
def page_not_found(error):
    message = "Page does not exist."
    return render_template('error.html', message=message), 404


@app.errorhandler(500)
def error_500(error):
    message = "Internal wm-metrics error (aka 500)"
    return render_template('error.html', message=message), 500


if __name__ == "__main__":
    app.run(debug=True)
