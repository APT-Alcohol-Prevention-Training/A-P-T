import os
from functools import wraps

from flask import Response, request


class AuthManager:
    @classmethod
    def check_auth(cls, username, password):
        """Verify that provided credentials match the stored admin credentials."""
        # Get credentials dynamically
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        # Debug print
        print(f"Checking auth - Expected: {admin_username}/{admin_password}")
        print(f"Checking auth - Received: {username}/{password}")
        
        # Ensure credentials are set
        if not admin_username or not admin_password:
            print("Admin credentials not set in environment")
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
