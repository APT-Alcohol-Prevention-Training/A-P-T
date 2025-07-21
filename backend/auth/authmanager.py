from functools import wraps
from flask import Response, request
from config import current_config


class AuthManager:
    @classmethod
    def check_auth(cls, username, password):
        """Verify that provided credentials match the stored admin credentials."""
        config = current_config()
        
        # Check if authentication is enabled
        if not config.AUTH_ENABLED:
            return True
        
        # Get credentials from config
        admin_username = config.ADMIN_USERNAME
        admin_password = config.ADMIN_PASSWORD
        
        # Ensure credentials are set
        if not admin_username or not admin_password:
            return False
            
        # Compare username and password
        return username == admin_username and password == admin_password

    @staticmethod
    def authenticate():
        """Return a 401 response prompting for proper credentials."""
        return Response(
            "Could not verify your access level for that URL.\n"
            "You have to login with proper credentials.",
            401,
            {"WWW-Authenticate": 'Basic realm="Login Required"'},
        )


def requires_auth(f):
    """Decorator to enforce basic authentication on routes."""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not AuthManager.check_auth(auth.username, auth.password):
            return AuthManager.authenticate()
        return f(*args, **kwargs)

    return decorated
