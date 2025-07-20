"""
APT Chat Bot - Centralized Configuration System
==============================================
This module provides a comprehensive configuration management system for the APT Chat Bot.
All settings are centralized here for easy management and environment-specific deployment.
"""

import os
import secrets
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import timedelta


class Config:
    """Base configuration class with common settings."""
    
    # ===== APPLICATION SETTINGS =====
    APP_NAME = "APT Chat Bot"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    
    # ===== PATHS AND DIRECTORIES =====
    BASE_DIR = Path(__file__).parent.absolute()
    LOG_DIR = BASE_DIR / "logs"
    SESSION_LOG_DIR = LOG_DIR / "session_logs"
    ACTIVE_SESSION_DIR = SESSION_LOG_DIR / "active"
    COMPLETED_SESSION_DIR = SESSION_LOG_DIR / "completed"
    ASSESSMENT_DATA_FILE = BASE_DIR / "assessment_data.json"
    
    # ===== SERVER CONFIGURATION =====
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    WORKERS = int(os.getenv('WORKERS', 1))
    
    # ===== FLASK CONFIGURATION =====
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_NAME = 'apt_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # ===== CORS CONFIGURATION =====
    CORS_ENABLED = os.getenv('CORS_ENABLED', 'True').lower() == 'true'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',') if os.getenv('CORS_ORIGINS') else [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://34.31.208.12:3000",
        "http://34.31.208.12:8000",
        "https://34.31.208.12:3000",
        "https://34.31.208.12:8000"
    ]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_SUPPORTS_CREDENTIALS = True
    
    # ===== AUTHENTICATION =====
    AUTH_ENABLED = os.getenv('AUTH_ENABLED', 'True').lower() == 'true'
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    AUTH_TOKEN_EXPIRY = timedelta(hours=24)
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 5))
    LOGIN_ATTEMPT_WINDOW = timedelta(minutes=15)
    
    # ===== OPENAI CONFIGURATION =====
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_DEFAULT_MODEL = os.getenv('OPENAI_DEFAULT_MODEL', 'gpt-3.5-turbo')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', 2000))
    OPENAI_TOP_P = float(os.getenv('OPENAI_TOP_P', 1.0))
    OPENAI_FREQUENCY_PENALTY = float(os.getenv('OPENAI_FREQUENCY_PENALTY', 0.0))
    OPENAI_PRESENCE_PENALTY = float(os.getenv('OPENAI_PRESENCE_PENALTY', 0.0))
    OPENAI_TIMEOUT = int(os.getenv('OPENAI_TIMEOUT', 30))
    OPENAI_MAX_RETRIES = int(os.getenv('OPENAI_MAX_RETRIES', 3))
    
    # ===== LOGGING CONFIGURATION =====
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_FILE_MAX_BYTES = int(os.getenv('LOG_FILE_MAX_BYTES', 10485760))  # 10MB
    LOG_FILE_BACKUP_COUNT = int(os.getenv('LOG_FILE_BACKUP_COUNT', 5))
    LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'True').lower() == 'true'
    LOG_TO_CONSOLE = os.getenv('LOG_TO_CONSOLE', 'True').lower() == 'true'
    
    # ===== RATE LIMITING =====
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '100 per hour')
    RATE_LIMIT_STORAGE_URL = os.getenv('RATE_LIMIT_STORAGE_URL', 'memory://')
    
    # ===== VALIDATION SETTINGS =====
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', 4000))
    MIN_MESSAGE_LENGTH = int(os.getenv('MIN_MESSAGE_LENGTH', 1))
    ALLOWED_MESSAGE_TYPES = ['text', 'system']
    MAX_CONVERSATION_LENGTH = int(os.getenv('MAX_CONVERSATION_LENGTH', 100))
    
    # ===== PERFORMANCE SETTINGS =====
    RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', 60))
    CONNECTION_POOL_SIZE = int(os.getenv('CONNECTION_POOL_SIZE', 10))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    
    # ===== SECURITY SETTINGS =====
    SECURITY_HEADERS_ENABLED = os.getenv('SECURITY_HEADERS_ENABLED', 'True').lower() == 'true'
    CONTENT_SECURITY_POLICY = os.getenv('CONTENT_SECURITY_POLICY', "default-src 'self'")
    X_CONTENT_TYPE_OPTIONS = 'nosniff'
    X_FRAME_OPTIONS = 'DENY'
    X_XSS_PROTECTION = '1; mode=block'
    
    # ===== FEATURE FLAGS =====
    FEATURE_ASSESSMENT = os.getenv('FEATURE_ASSESSMENT', 'True').lower() == 'true'
    FEATURE_SESSION_EXPORT = os.getenv('FEATURE_SESSION_EXPORT', 'True').lower() == 'true'
    FEATURE_CONVERSATION_HISTORY = os.getenv('FEATURE_CONVERSATION_HISTORY', 'True').lower() == 'true'
    FEATURE_ANALYTICS = os.getenv('FEATURE_ANALYTICS', 'False').lower() == 'true'
    
    @classmethod
    def init_app(cls, app):
        """Initialize Flask app with configuration."""
        # Apply Flask-specific configurations
        for key in dir(cls):
            if key.isupper() and not key.startswith('_'):
                app.config[key] = getattr(cls, key)
        
        # Create necessary directories
        cls.create_directories()
        
        # Validate configuration
        cls.validate_config()
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        directories = [
            cls.LOG_DIR,
            cls.SESSION_LOG_DIR,
            cls.ACTIVE_SESSION_DIR,
            cls.COMPLETED_SESSION_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_config(cls):
        """Validate critical configuration settings."""
        # Skip validation in testing environment
        if cls.TESTING:
            return
            
        errors = []
        
        # Check OpenAI API key
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not set")
        
        # Check secret key in production
        if not cls.DEBUG and cls.SECRET_KEY == secrets.token_hex(32):
            errors.append("Flask SECRET_KEY must be set in production")
        
        # Check authentication in production
        if not cls.DEBUG and (cls.ADMIN_USERNAME == 'admin' or cls.ADMIN_PASSWORD == 'admin123'):
            errors.append("Default admin credentials should not be used in production")
        
        # Check CORS in production
        if not cls.DEBUG and 'localhost' in str(cls.CORS_ORIGINS):
            errors.append("Localhost should not be in CORS_ORIGINS in production")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Get OpenAI configuration as a dictionary."""
        return {
            'api_key': cls.OPENAI_API_KEY,
            'model': cls.OPENAI_DEFAULT_MODEL,
            'temperature': cls.OPENAI_TEMPERATURE,
            'max_tokens': cls.OPENAI_MAX_TOKENS,
            'top_p': cls.OPENAI_TOP_P,
            'frequency_penalty': cls.OPENAI_FREQUENCY_PENALTY,
            'presence_penalty': cls.OPENAI_PRESENCE_PENALTY,
            'timeout': cls.OPENAI_TIMEOUT,
            'max_retries': cls.OPENAI_MAX_RETRIES
        }
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """Get logging configuration as a dictionary."""
        return {
            'level': cls.LOG_LEVEL,
            'format': cls.LOG_FORMAT,
            'date_format': cls.LOG_DATE_FORMAT,
            'file_max_bytes': cls.LOG_FILE_MAX_BYTES,
            'file_backup_count': cls.LOG_FILE_BACKUP_COUNT,
            'log_to_file': cls.LOG_TO_FILE,
            'log_to_console': cls.LOG_TO_CONSOLE,
            'log_dir': str(cls.LOG_DIR)
        }
    
    @classmethod
    def get_cors_config(cls) -> Dict[str, Any]:
        """Get CORS configuration as a dictionary."""
        return {
            'origins': cls.CORS_ORIGINS,
            'allow_headers': cls.CORS_ALLOW_HEADERS,
            'methods': cls.CORS_METHODS,
            'supports_credentials': cls.CORS_SUPPORTS_CREDENTIALS
        }
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Export all configuration as a dictionary."""
        config = {}
        for key in dir(cls):
            if key.isupper() and not key.startswith('_'):
                value = getattr(cls, key)
                # Convert Path objects to strings
                if isinstance(value, Path):
                    value = str(value)
                config[key] = value
        return config


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False
    
    # More permissive CORS for development
    CORS_ORIGINS = ["*"]
    
    # Disable some security features for easier development
    SESSION_COOKIE_SECURE = False
    SECURITY_HEADERS_ENABLED = False
    
    # Enable all features for development
    FEATURE_ANALYTICS = True


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    
    # Use in-memory session storage for tests
    SESSION_TYPE = 'null'
    
    # Disable rate limiting for tests
    RATE_LIMIT_ENABLED = False
    
    # Use a fixed secret key for tests
    SECRET_KEY = 'test-secret-key'
    
    # Disable authentication for most tests
    AUTH_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    
    # Enforce security in production
    SESSION_COOKIE_SECURE = True
    SECURITY_HEADERS_ENABLED = True
    
    # Production-specific settings
    LOG_LEVEL = 'WARNING'
    RATE_LIMIT_DEFAULT = '50 per hour'
    
    # Ensure critical settings are from environment
    @classmethod
    def validate_config(cls):
        """Extended validation for production."""
        super().validate_config()
        
        # Additional production checks
        if not os.getenv('FLASK_SECRET_KEY'):
            raise ValueError("FLASK_SECRET_KEY must be explicitly set in production")
        
        if not os.getenv('ADMIN_USERNAME') or not os.getenv('ADMIN_PASSWORD'):
            raise ValueError("Admin credentials must be explicitly set in production")


# Configuration factory
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env_name: Optional[str] = None) -> Config:
    """Get configuration based on environment name."""
    if env_name is None:
        env_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(env_name, config['default'])


# Convenience function for getting current config
def current_config() -> Config:
    """Get the current configuration based on FLASK_ENV."""
    return get_config()