#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from wmmetrics import app

from flask import request

import time
import logging
from logging import FileHandler

formatter = logging.Formatter("%(asctime)s: %(message)s", "%Y-%m-%d %H:%M:%S")

error_handler = FileHandler('error.log')
error_handler.setFormatter(formatter)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(error_handler)

usage_handler = RotatingFileHandler('usage.log', maxBytes=10000, backupCount=1)
usage_handler.setFormatter(formatter)
usage_handler.setLevel(logging.INFO)
app.logger.addHandler(usage_handler)

app.logger.debug(u"Flask server started")

@app.after_request
def write_access_log(response):
    app.logger.debug(u"%s %s -> %s" % (time.asctime(), request.path, response.status_code))
    return response

if __name__ == '__main__':
    WSGIServer(app).run()
