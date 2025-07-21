import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path

from app.routes import main_bp
from config import get_config
from logger import setup_logging

# Load .env file from the backend directory
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'
load_dotenv(env_path)


def create_app(config_name=None):
    """Create and configure the Flask application.
    
    Args:
        config_name (str, optional): Configuration environment name.
    
    Returns:
        Flask: Configured Flask application instance.
        
    Raises:
        ValueError: If configuration validation fails.
    """
    try:
        # Get configuration
        config = get_config(config_name)
    except Exception as e:
        raise ValueError(f"Failed to load configuration: {str(e)}")
    
    # Set template folder to backend/templates
    template_dir = os.path.join(config.BASE_DIR, 'templates')
    app = Flask(__name__, template_folder=template_dir)
    
    # Initialize app with configuration
    config.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Configure CORS if enabled
    if config.CORS_ENABLED:
        CORS(app, 
             resources={r"/*": {"origins": config.CORS_ORIGINS}},
             allow_headers=config.CORS_ALLOW_HEADERS,
             methods=config.CORS_METHODS,
             supports_credentials=config.CORS_SUPPORTS_CREDENTIALS)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    # Add security headers if enabled
    if config.SECURITY_HEADERS_ENABLED:
        @app.after_request
        def add_security_headers(response):
            response.headers['Content-Security-Policy'] = config.CONTENT_SECURITY_POLICY
            response.headers['X-Content-Type-Options'] = config.X_CONTENT_TYPE_OPTIONS
            response.headers['X-Frame-Options'] = config.X_FRAME_OPTIONS
            response.headers['X-XSS-Protection'] = config.X_XSS_PROTECTION
            return response
    
    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        from flask import jsonify
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        from flask import jsonify
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        from flask import jsonify
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify
        app.logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        from flask import jsonify
        app.logger.error(f'Unhandled exception: {error}')
        if config.DEBUG:
            return jsonify({'error': type(error).__name__, 'message': str(error)}), 500
        return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}), 500
    
    return app
