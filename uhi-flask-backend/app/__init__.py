from flask import Flask
from flask_cors import CORS
from .routes import routes  # ✅ match variable name in routes.py
import os

def create_app():
    app = Flask(__name__)
    
    # Set base directory for file access in routes.py
    app.config["BASE_DIR"] = os.path.abspath(os.path.dirname(__file__))

    # Allow CORS for frontend (dev & prod)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

    # Register routes under /api prefix
    app.register_blueprint(routes, url_prefix="/api")

    return app
