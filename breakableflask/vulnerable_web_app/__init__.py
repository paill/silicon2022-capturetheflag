"""Initialize Flask app."""
from flask import Flask
from flask_bootstrap import Bootstrap
import os
import importlib

SECRET_KEY = os.urandom(32)



def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    Bootstrap(app)
    app.config['SECRET_KEY'] = SECRET_KEY
    with app.app_context():
        blueprints = os.environ["BLUEPRINTS"].split(',')

        for blueprint_string in blueprints:
            blueprint_module = importlib.import_module(f".{blueprint_string}.{blueprint_string}", package=__name__)
            blueprint_object = getattr(blueprint_module, f"{blueprint_string}_bp")
            app.register_blueprint(blueprint_object)

        return app