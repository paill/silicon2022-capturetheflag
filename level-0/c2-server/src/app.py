#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

from waitress import serve
from werkzeug.exceptions import HTTPException

import json
import base64
import subprocess

import time
import traceback

app = Flask(__name__)

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/c2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String)
    result = db.Column(db.String)

class Beacon(db.Model):
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id"  : self.id,
            "name": self.name,
            "status"  : self.status
        }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    status = db.Column(db.String)

def initalize_session_cookie():
    session_cookie_dict = {"username": "guest", "is_admin": False}
    session_cookie_string = json.dumps(session_cookie_dict)
    return base64.b64encode(session_cookie_string.encode("utf-8")).decode("utf-8")

def admin_only(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        session_cookie = request.cookies.get("session")
        if session_cookie:
            try:
                session_cookie_string = base64.b64decode(session_cookie.encode("utf-8")).decode("utf-8")
                session_cookie_dict = json.loads(session_cookie_string)
                is_admin = session_cookie_dict.get("is_admin")
                if is_admin:
                    return f(*args, **kwargs)
            except Exception as e:
                logging.error(f"{e}")
                return render_template("redir.html", message="Access denied. Admins only.")
        return render_template("redir.html", message="Access denied. Admins only.") 
    return decorator

@app.route("/", methods=["GET"])
def home():
    commands = Command.query.all()
    response = make_response(render_template("index.html", commands=commands))
    response.set_cookie("session", initalize_session_cookie())
    return response

@app.route("/console", methods=["GET"])
@admin_only
def console():
    return render_template("console.html")

@app.route("/beacons", methods=["GET"])
@admin_only
def beacons():
    beacons = Beacon.query.all()
    return jsonify([beacon.serialize for beacon in beacons])

@app.route("/command", methods=["POST"])
@admin_only
def command():
    ALLOWED_COMMAND_LIST = ("whoami", "ls")
    DISABLED_COMMAND_LIST = ("upload", "download", "echo")

    try:
        data = request.json
        beacon_id = data.get("beacon_id")
        command = data.get("command")
        arg = " ".join(list(data.get("arg")))

        if beacon_id and command:
            if beacon_id == 1:
                if command in ALLOWED_COMMAND_LIST:
                    if command == "ls":
                        if arg is None:
                            arg = "."
                        command = f"{command} {arg}"
                        logger.info(command)
                        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
                    else:
                        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
                    return jsonify({"status":"success", "message": output})
                elif command in DISABLED_COMMAND_LIST:
                    return jsonify({"status":"error", "message":f"{command} command is disabled on test beacons"})
                else:
                    return jsonify({"status":"error", "message":"command not allowed"})
            else:
                return jsonify({"status":"error", "message":"invalid beacon id - is the beacon running?"})
        else:
            return jsonify({"status":"error", "message":"invalid request"})
    except:
        return jsonify({"status":"error", "message":"invalid request"})

@app.route("/b0w53r5_5up3r_s3cR3t_P4th", methods=["GET"])
def flag():
    return render_template("secretpath.html")

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


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)