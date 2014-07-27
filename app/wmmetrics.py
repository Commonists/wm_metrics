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
    round_num = int(request.form['round'])
    fdc_round = fdc.Round(fdc_year-1, fdc_year, round_num)
    try:
        results = wmfr_photography.make_example_report(fdc_round, category)
        return render_template('fdc-report-results.html',
                               category=category,
                               fdc_round=fdc_round,
                               contents=results)
    except wmfr_photography.WMmetricsException, e:
        message = 'Something went wrong in Wm_metrics: ' + e.message
        return render_template('error.html', message=message)
    except Exception, e:
        message = 'Something went wrong somewhere: ' + e.message
        return render_template('error.html', message=e)

if __name__ == "__main__":
    app.run(debug=True)
