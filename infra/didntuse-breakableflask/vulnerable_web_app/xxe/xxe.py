from flask import Blueprint, flash, render_template
from flask import current_app as app

from lxml import etree

from .xml_form import XMLForm

# Blueprint Configuration
xxe_bp = Blueprint(
    "xxe_bp", __name__, template_folder="templates", static_folder="static"
)

@xxe_bp.route("/xxe", methods=["GET", "POST"])
def xxe():

    form = XMLForm()

    if form.validate_on_submit():      
        xml = form.xml.data
        parser = etree.XMLParser()
        # try:
        doc = etree.fromstring(str(xml), parser)
        parsed_xml = etree.tostring(doc)
        flash(f"Parsed XML: {parsed_xml}", "info")
        # except:
            # flash("Invalid XML!", "error")

    return render_template("xxe.html", form=form)