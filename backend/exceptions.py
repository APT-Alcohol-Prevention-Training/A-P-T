from flask import jsonify


class AppException(Exception):
    """
    Base class for application-specific exceptions.
    """

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["error"] = self.message
        return rv


class InvalidChatbotTypeError(AppException):
    """
    Exception raised for an invalid chatbot type input.
    """

    status_code = 400


class MissingParameterError(AppException):
    """
    Exception raised for missing required parameters in the request.
    """

    status_code = 400


class ConfigurationError(AppException):
    """
    Exception raised when configuration (such as API key or model ID) is missing.
    """

    status_code = 500


def register_error_handlers(app):
    """
    Register custom error handlers for the Flask app.
    """

    @app.errorhandler(AppException)
    def handle_app_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        # Log the error here if desired
        return jsonify({"error": "An unexpected error occurred."}), 500
