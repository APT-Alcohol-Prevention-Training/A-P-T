import os
from flask import Blueprint, abort, jsonify, request, send_from_directory, session

# Local imports for authentication, chatbot, and logging
from auth.authmanager import requires_auth
from chatbot.chatbot import Chatbot
from exceptions import InvalidChatbotTypeError, MissingParameterError
from logger.custom_logger import Logger

# Define a blueprint for main routes
main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def home():
    """
    Home endpoint:
      - GET returns a welcome message.
      - POST expects JSON with 'message', 'chatbot_type', and (optionally) 'risk_score'.
        It processes the message, logs the conversation, and returns the chatbot response.
    """
    # Set session variables for API key and default model
    session["openai_api_key"] = os.getenv("OPENAI_API_KEY")
    session["fine_tuned_model"] = os.getenv("OPENAI_DEFAULT_MODEL")

    if request.method == "POST":
        data = request.get_json()
        if not data:
            raise MissingParameterError(
                "Invalid or missing JSON payload.", status_code=400
            )

        user_message = data.get("message")
        if user_message is None:
            raise MissingParameterError("Missing 'message' parameter.", status_code=400)

        chatbot_type = data.get("chatbot_type")
        if chatbot_type is None:
            raise MissingParameterError(
                "Missing 'chatbot_type' parameter.", status_code=400
            )

        # Allowed types: "ai", "student", "doctor"
        ALLOWED_CHATBOT_TYPES = ["ai", "student", "doctor"]
        if chatbot_type not in ALLOWED_CHATBOT_TYPES:
            raise InvalidChatbotTypeError(
                "Invalid chatbot type provided.", status_code=400
            )

        # Optionally retrieve risk_score (used in the pre-chat assessment)
        risk_score = data.get("risk_score")

        # Retrieve API key from session and get chatbot response (passing risk_score if available)
        api_key = session.get("openai_api_key")
        bot_response = Chatbot.get_response(
            chatbot_type, user_message, risk_score, api_key
        )

        # Log the conversation using the custom logger
        user_ip = request.remote_addr or "Unknown"
        Logger.log_conversation(chatbot_type, user_message, bot_response, user_ip)

        return jsonify({"bot_response": bot_response})

    # GET request response
    return jsonify({"message": "Hello world! from Flask backend"})


@main_bp.route("/download_logs")
@requires_auth
def download_logs():
    """
    Endpoint to download conversation logs.
    Protected using basic authentication.
    """
    try:
        log_dir = os.path.dirname(Logger.log_file_path)
        return send_from_directory(log_dir, "conversations.log", as_attachment=True)
    except FileNotFoundError:
        abort(404, description="Log file not found.")
    except Exception as e:
        abort(500, description=str(e))
