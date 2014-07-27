from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fdc")
def fdc_report_page():
    return render_template('fdc-report.html')

if __name__ == "__main__":
    app.run(debug=True)
