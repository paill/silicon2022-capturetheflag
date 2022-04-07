"""Initialize Flask app."""
from flask import Flask


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        # Import parts of our application
        from .cookie import cookie

        # Register Blueprints
        app.register_blueprint(cookie.cookie_bp)

        return app