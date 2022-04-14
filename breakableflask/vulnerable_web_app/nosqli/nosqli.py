from flask import Blueprint, flash, render_template, redirect
from flask import current_app as app
from flask_pymongo import PyMongo

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

        # TODO: Make vulnerable
        user_count = mongo.db.users.count_documents({
            "username": username,
            "password": password
        })

        if user_count > 0:
            return render_template('flag.html')
        else:
            flash('Login failed')

    return render_template('nosqli.html', form=form)
