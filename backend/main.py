import os
from app import create_app
from config import current_config

# Create app with environment-specific config
app = create_app()

if __name__ == "__main__":
    # Get current configuration
    config = current_config()
    
    # Run the Flask development server with config settings
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
