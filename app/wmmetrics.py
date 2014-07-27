import os
import sys
from flask import Flask, render_template, request

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(current_dir, '..'))

from wm_metrics import fdc
from wm_metrics import wmfr_photography
from wm_metrics import commons_cat_metrics

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fdc")
def fdc_report_page():
    return render_template('fdc-report.html')

@app.route("/fdc/submit", methods=["POST"])
def compute_fdc_report():
    category = request.form['category']
    fdc_year = int(request.form['year'])
    fdc_round = fdc.Round(fdc_year-1, fdc_year, int(request.form['round']))
    results = wmfr_photography.make_example_report(fdc_round, category)
    return results

if __name__ == "__main__":
    app.run(debug=True)
