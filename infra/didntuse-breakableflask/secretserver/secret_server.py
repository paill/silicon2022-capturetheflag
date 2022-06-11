"""Initialize Flask app."""
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def you_found_me():
    return f"Hey! You shouldn't be here! - {os.environ['SECRETSERVER_FLAG']}"

app.run(host="0.0.0.0", port=1234)
