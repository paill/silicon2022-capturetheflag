from flask import Blueprint
from flask import current_app as app
from flask import render_template
from flask import request, make_response

import pickle
from base64 import b64decode,b64encode

# Blueprint Configuration
cookie_bp = Blueprint(
    "cookie_bp", __name__, template_folder="templates", static_folder="static"
)

@cookie_bp.route("/cookie", methods=["GET", "POST"])
def cookie():
    cookieValue = None
    value = None
    
    if request.method == 'POST':
        cookieValue = request.form['value']
        value = cookieValue
    elif 'value' in request.cookies:
        cookieValue = pickle.loads(b64decode(request.cookies['value'])) 
    
        
    form = """
    <html>
       <body>Cookie value: """ + str(cookieValue) +"""
          <form action = "/cookie" method = "POST">
             <p><h3>Enter value to be stored in cookie</h3></p>
             <p><input type = 'text' name = 'value'/></p>
             <p><input type = 'submit' value = 'Set Cookie'/></p>
          </form>
       </body>
    </html>
    """
    resp = make_response(form)
    
    if value:
        resp.set_cookie('value', b64encode(pickle.dumps(value)))

    return resp