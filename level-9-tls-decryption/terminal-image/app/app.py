"""Initialize Flask app."""
from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def root():
    return f"Welcome to Bowser Corp. Please Authenticate to continue"

@app.route('/kingkoopa')
def restricted():
    if request.environ.get('CLIENT_VERIFY') == 'SUCCESS':
        return f"Restricted Area. Surveillance file keys accessible for reading at /kingkoopa/sslkeylogfile"
    else:
        return f"Access Denied!"

@app.route('/kingkoopa/sslkeylogfile')
def sslkeylogfile():
    if request.environ.get('CLIENT_VERIFY') == 'SUCCESS':
        return send_from_directory(directory='/app', path='sslkeylogfile')
    else:
        return f"Access Denied!"

if __name__ == '__main__':
    app.run()
