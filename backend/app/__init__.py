import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()


def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_default_secret_key")

    # Enable CORS (customize origins as needed)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints for route definitions
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # Register custom error handlers
    from exceptions import register_error_handlers

    register_error_handlers(app)

    return app
