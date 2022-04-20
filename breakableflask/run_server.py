from vulnerable_web_app import create_app
from waitress import serve

import logging
from flask import request
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
    return e.status_code

serve(app, host="0.0.0.0", port=5000)