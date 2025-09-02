
from flask import Flask
from flask_cors import CORS
from .routes import routes
import os

def create_app():
    app = Flask(__name__)

    # Set base directory for data access
    app.config["BASE_DIR"] = os.path.join(os.path.dirname(__file__), "data")

    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register routes
    app.register_blueprint(routes, url_prefix="/api")

    return app


