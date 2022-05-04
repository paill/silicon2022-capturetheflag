from vulnerable_web_app import create_app
from waitress import serve
from werkzeug.exceptions import HTTPException

import logging
from flask import render_template, request
import time
import traceback

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app = create_app()

@app.after_request
def after_request(response):
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
    if isinstance(e, HTTPException):
        return e
    return "Bad request", 500

serve(app, host="0.0.0.0", port=5000)