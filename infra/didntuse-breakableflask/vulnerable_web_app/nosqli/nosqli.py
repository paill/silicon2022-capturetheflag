from flask import Blueprint, flash, render_template
from flask import current_app as app
from flask_pymongo import PyMongo
import json

from .login_form import LoginForm
from .config import *

app.config["MONGO_URI"] = f"mongodb://{NOSQL_USER}:{NOSQL_PASSWORD}@{NOSQL_HOST}:{NOSQL_PORT}/{NOSQL_DATABASE}"
mongo = PyMongo(app)


# Blueprint Configuration
nosqli_bp = Blueprint(
    "nosqli_bp", __name__, template_folder="templates", static_folder="static"
)

@nosqli_bp.route("/nosqli", methods=["GET", "POST"])
def nosqli():

    form = LoginForm()

    if form.validate_on_submit():      
        username = form.username.data
        password = form.password.data

        # The form inputs will come in as strings which protects against NoSQL injection. 
        # In order to make this form vulnerable, we need to attempt to load the inputs as JSON
        # But if an input is not JSON, the form still needs to work
        try:
            username = json.loads(username)
        except ValueError as e:
            pass
        try:
            password = json.loads(password)
        except ValueError as e:
            pass

        user_count = mongo.db.users.count_documents({
            "username": username,
            "password": password
        })

        if user_count > 0:
            flash(f"{FLAG}",)
            return render_template("nosqli.html", form=form)
        else:
            flash("Login failed", "error")

    return render_template("nosqli.html", form=form)
