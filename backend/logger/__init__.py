"""
Logging module for APT Chat Bot
"""
import logging
import logging.handlers
from pathlib import Path
from config import current_config


def setup_logging(app=None):
    """Setup application logging based on configuration.
    
    Args:
        app: Flask application instance (optional)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    config = current_config()
    
    # Create logger
    logger = logging.getLogger('apt_chatbot')
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create formatters
    formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    # Console handler
    if config.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler with rotation
    if config.LOG_TO_FILE:
        try:
            log_file = config.LOG_DIR / 'app.log'
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=config.LOG_FILE_MAX_BYTES,
                backupCount=config.LOG_FILE_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            if app:
                app.logger.error(f"Failed to setup file logging: {e}")
            else:
                print(f"Failed to setup file logging: {e}")
    
    # If Flask app provided, configure its logger too
    if app:
        app.logger.handlers = logger.handlers
        app.logger.setLevel(logger.level)
    
    return logger


# Create a default logger instance
logger = setup_logging()