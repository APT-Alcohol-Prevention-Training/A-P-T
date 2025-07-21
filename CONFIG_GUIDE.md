# APT Chat Bot Configuration Guide

This guide explains how to configure and manage the APT Chat Bot using the centralized configuration system.

## Table of Contents
- [Overview](#overview)
- [Configuration System](#configuration-system)
- [Environment Variables](#environment-variables)
- [Configuration Classes](#configuration-classes)
- [Usage Examples](#usage-examples)
- [Security Best Practices](#security-best-practices)

## Overview

The APT Chat Bot uses a centralized configuration system through `backend/config.py`. All settings are managed from this single location, making it easy to:

- Control application behavior
- Manage environment-specific settings
- Ensure security best practices
- Validate configuration before startup

## Configuration System

### File Structure
```
backend/
├── config.py           # Centralized configuration
├── .env               # Environment variables (not in git)
└── .env               # Environment variables file
```

### Key Features
- **Environment-based**: Different configurations for development, testing, and production
- **Validation**: Automatic validation of critical settings
- **Type Safety**: Proper type hints for all configuration values
- **Security**: Sensitive data loaded from environment variables
- **Flexibility**: Easy to extend with new settings

## Environment Variables

Edit the `.env` file in the backend directory with the following variables:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here
DEBUG=False

# Server Configuration
HOST=0.0.0.0
PORT=8080
WORKERS=1

# Authentication
AUTH_ENABLED=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-password-here

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_DEFAULT_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000

# CORS Configuration
CORS_ENABLED=True
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Logging
LOG_LEVEL=INFO
LOG_TO_FILE=True
LOG_TO_CONSOLE=True

# Features
FEATURE_ASSESSMENT=True
FEATURE_SESSION_EXPORT=True
FEATURE_CONVERSATION_HISTORY=True
FEATURE_ANALYTICS=False

# Security
SESSION_COOKIE_SECURE=True
SECURITY_HEADERS_ENABLED=True

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_DEFAULT=100 per hour
```

## Configuration Classes

### Base Configuration (`Config`)
The base configuration class contains default settings for all environments:

```python
from config import current_config

# Get current configuration
config = current_config()

# Access settings
api_key = config.OPENAI_API_KEY
max_tokens = config.OPENAI_MAX_TOKENS
```

### Development Configuration (`DevelopmentConfig`)
- Debug mode enabled
- Permissive CORS settings
- All features enabled
- Relaxed security for easier development

### Testing Configuration (`TestingConfig`)
- Testing mode enabled
- In-memory sessions
- Authentication disabled
- Rate limiting disabled

### Production Configuration (`ProductionConfig`)
- Debug mode disabled
- Strict security settings
- Environment variable validation
- Production-optimized settings

## Usage Examples

### 1. Accessing Configuration in Flask Routes
```python
from flask import current_app
from config import current_config

@app.route('/example')
def example():
    config = current_config()
    
    if config.FEATURE_ANALYTICS:
        # Track analytics
        pass
    
    return jsonify({
        'app': config.APP_NAME,
        'version': config.APP_VERSION
    })
```

### 2. Using OpenAI Configuration
```python
from config import current_config

config = current_config()
openai_config = config.get_openai_config()

client = OpenAI(
    api_key=openai_config['api_key'],
    timeout=openai_config['timeout'],
    max_retries=openai_config['max_retries']
)
```

### 3. Setting Up Logging
```python
from config import current_config

config = current_config()
logging_config = config.get_logging_config()

# Configure logging based on settings
logging.basicConfig(
    level=logging_config['level'],
    format=logging_config['format']
)
```

### 4. CORS Configuration
```python
from flask_cors import CORS
from config import current_config

config = current_config()

if config.CORS_ENABLED:
    CORS(app, 
         origins=config.CORS_ORIGINS,
         allow_headers=config.CORS_ALLOW_HEADERS,
         methods=config.CORS_METHODS)
```

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong secret keys** in production
3. **Enable security headers** in production
4. **Use HTTPS** for production deployments
5. **Validate all configuration** before starting the application
6. **Rotate credentials** regularly
7. **Limit CORS origins** to trusted domains only
8. **Enable rate limiting** to prevent abuse

## Directory Creation

The configuration system automatically creates necessary directories:
- `logs/` - Application logs
- `logs/session_logs/` - Session-specific logs
- `logs/session_logs/active/` - Active session logs
- `logs/session_logs/completed/` - Completed session logs

## Validation

The configuration system performs automatic validation:
- Checks for required environment variables
- Validates API keys are set
- Ensures production settings are secure
- Verifies directory permissions

## Extending Configuration

To add new configuration options:

1. Add the setting to the `Config` class:
```python
class Config:
    # Existing settings...
    
    # New setting
    MY_NEW_SETTING = os.getenv('MY_NEW_SETTING', 'default_value')
```

2. Add environment-specific overrides if needed:
```python
class ProductionConfig(Config):
    MY_NEW_SETTING = os.getenv('MY_NEW_SETTING')  # Required in production
```

3. Update the `.env` file with the new variable

4. Use the setting in your code:
```python
config = current_config()
value = config.MY_NEW_SETTING
```

## Troubleshooting

### Configuration not loading
- Check that `.env` file exists and is in the correct location
- Verify environment variable names match exactly
- Ensure `python-dotenv` is installed

### Validation errors
- Review error messages for specific issues
- Check that all required environment variables are set
- Verify values are in the correct format

### Permission errors
- Ensure the application has write permissions for log directories
- Check file ownership and permissions

## Frontend Configuration

The frontend Next.js application uses its own `.env.local` file:

```bash
BACKEND_API_URL=http://localhost:8080
```

This should match your backend server configuration.