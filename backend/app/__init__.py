import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.routes import main_bp

load_dotenv()


def create_app():
    """Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    # Set template folder to backend/templates
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://34.31.208.12:3000",
        "http://34.31.208.12:8080",
        "https://34.31.208.12:3000",
        "https://34.31.208.12:8080"
    ]
    
    CORS(app, resources={r"/*": {"origins": allowed_origins}})
    app.register_blueprint(main_bp)

    return app
