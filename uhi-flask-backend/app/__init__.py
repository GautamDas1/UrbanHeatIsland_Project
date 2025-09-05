from flask import Flask
from flask_cors import CORS
from .routes import routes
import os

def create_app():
    app = Flask(__name__)

    # Store base directory
    app.config["BASE_DIR"] = os.path.abspath(os.path.dirname(__file__))

    # Allow frontend access
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173"]}})

    # Register routes
    app.register_blueprint(routes, url_prefix="/api")

    return app
