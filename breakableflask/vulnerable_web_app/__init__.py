"""Initialize Flask app."""
from flask import Flask
from flask_bootstrap import Bootstrap
import os
SECRET_KEY = os.urandom(32)



def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    Bootstrap(app)
    app.config['SECRET_KEY'] = SECRET_KEY
    with app.app_context():
        # Import parts of our application
        from .cookie import cookie
        from .nosqli import nosqli


        # Register Blueprints
        app.register_blueprint(cookie.cookie_bp)
        app.register_blueprint(nosqli.nosqli_bp)

        return app