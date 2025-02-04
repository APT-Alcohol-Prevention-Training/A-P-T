import os
from functools import wraps

from flask import Response, request


class AuthManager:
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    @classmethod
    def check_auth(cls, username, password):
        """Verify that provided credentials match the stored admin credentials."""
        return username == cls.admin_username and password == cls.admin_password

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
