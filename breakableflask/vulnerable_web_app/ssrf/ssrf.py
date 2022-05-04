from flask import Blueprint, flash, render_template
from flask import current_app as app

import urllib.request
import urllib.parse

from .url_form import URLForm

# Blueprint Configuration
ssrf_bp = Blueprint(
    "ssrf_bp", __name__, template_folder="templates", static_folder="static"
)

@ssrf_bp.route("/ssrf", methods=["GET", "POST"])
def ssrf():

    form = URLForm()

    if form.validate_on_submit():      
        url = form.url.data

        try:
            response = urllib.request.urlopen(url)
            flash(f"Reponse text: {response.read()}", "info")
        except:
            flash("Invalid URL!", "error")

    return render_template("ssrf.html", form=form)