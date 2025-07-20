"""Flask routes for the chatbot application.

This module defines all the HTTP endpoints for the chatbot backend,
including conversation handling, session management, and log downloads.
"""

import json
import os
import tempfile
from datetime import datetime

from flask import (
    Blueprint,
    abort,
    after_this_request,
    jsonify,
    render_template,
    request,
    send_from_directory,
    session,
)

from auth.authmanager import requires_auth
from chatbot.chatbot import Chatbot
from logger.custom_logger import Logger
from logger.session_logger import session_logger
from validators import InputValidator
from config import current_config


main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def home():
    """Handle main chatbot interaction endpoint.
    
    GET: Returns a welcome message.
    POST: Processes user message and returns chatbot response.
    
    Expected POST data:
        message (str): User's message to the chatbot.
        chatbot_type (str): Type of chatbot (ai/student/doctor).
        risk_score (int, optional): User's risk assessment score.
        conversation_context (dict, optional): Additional context.
        
    Returns:
        JSON response with bot_response and session_id.
        
    Raises:
        400: Invalid JSON or missing required parameters.
    """
    if request.method == "POST":
        try:
            data = request.get_json()
        except Exception:
            abort(400, description="Invalid JSON payload.")

        user_message = data.get("message")
        if user_message is None:
            abort(400, description="Missing 'message' parameter.")
        
        # Sanitize user message
        user_message = InputValidator.sanitize_string(user_message)

        chatbot_type = data.get("chatbot_type")
        if chatbot_type is None:
            abort(400, description="Missing 'chatbot_type' parameter.")

        # Validate chatbot type
        if not InputValidator.validate_chatbot_type(chatbot_type):
            abort(400, description="Invalid chatbot type provided.")

        # Validate and convert risk_score
        risk_score = InputValidator.validate_risk_score(data.get("risk_score"))
        
        # Validate and sanitize conversation context
        conversation_context = InputValidator.validate_conversation_context(
            data.get("conversation_context", {})
        )

        # Get chatbot response (passing risk_score if available)
        try:
            bot_response = Chatbot.get_response(
                chatbot_type, user_message, risk_score, None, conversation_context
            )
        except ValueError as e:
            abort(400, description=str(e))
        except RuntimeError as e:
            abort(503, description=str(e))
        except Exception as e:
            config = current_config()
            if config.DEBUG:
                abort(500, description=f"Unexpected error: {str(e)}")
            else:
                abort(500, description="An unexpected error occurred")

        # Get or create session
        config = current_config()
        user_ip = request.remote_addr or "Unknown"
        if "session_id" not in session:
            session["session_id"] = session_logger.create_session(user_ip)
            session.permanent = config.SESSION_PERMANENT
        
        # Log to both traditional logger and session logger
        Logger.log_conversation(chatbot_type, user_message, bot_response, user_ip)
        session_logger.log_conversation(
            session["session_id"], chatbot_type, user_message, bot_response, user_ip,
            risk_score, conversation_context
        )

        return jsonify({
            "bot_response": bot_response,
            "session_id": session["session_id"]
        })

    # GET request response
    return jsonify({"message": "Hello world! from Flask backend"})


@main_bp.route("/download_logs")
@requires_auth
def download_logs():
    """Download legacy conversation logs file.
    
    Returns:
        File download of conversations.log.
        
    Raises:
        404: Log file not found.
    """
    config = current_config()
    log_file = config.LOG_DIR / "conversations.log"
    if not log_file.exists():
        abort(404, description="Log file not found")
    return send_from_directory(str(config.LOG_DIR), "conversations.log", as_attachment=True)


@main_bp.route("/download_session/<session_id>")
@requires_auth
def download_session(session_id):
    """Download CSV file for a specific session.
    
    Args:
        session_id: The UUID of the session to download.
        
    Returns:
        CSV file download for the specified session.
        
    Raises:
        404: Session not found.
    """
    csv_path = session_logger.get_session_csv_path(session_id)
    if not csv_path:
        abort(404, description="Session not found")
    
    directory = os.path.dirname(csv_path)
    filename = os.path.basename(csv_path)
    
    return send_from_directory(
        directory, filename, 
        as_attachment=True,
        download_name=f"session_{session_id}.csv"
    )


@main_bp.route("/sessions")
@requires_auth
def list_sessions():
    """List all available sessions organized by status.
    
    Returns:
        JSON with active and completed session lists.
    """
    sessions = session_logger.get_all_sessions()
    return jsonify(sessions)


@main_bp.route("/download_all_sessions")
@requires_auth
def download_all_sessions():
    """Download all sessions data in a single consolidated CSV file.
    
    Combines all active and completed sessions into one CSV file,
    sorted by timestamp.
    
    Returns:
        CSV file download with all session data.
        
    Raises:
        404: No session data found.
    """
    # Create temporary file for the consolidated CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp_path = tmp.name
    
    # Export all sessions to the temporary file
    count = session_logger.export_all_sessions_to_csv(tmp_path)
    
    if count == 0:
        os.unlink(tmp_path)
        abort(404, description="No session data found")
    
    # Send the file
    directory = os.path.dirname(tmp_path)
    filename = os.path.basename(tmp_path)
    
    @after_this_request
    def remove_file(response):  # pyright: ignore[reportUnusedFunction]
        """Clean up temporary file after sending response."""
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        return response
    
    return send_from_directory(
        directory, filename, 
        as_attachment=True,
        download_name=f"all_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )


@main_bp.route("/session_management")
@requires_auth
def session_management():
    """Display session management web interface.
    
    Returns:
        Rendered HTML template for session management.
    """
    return render_template("sessions.html")


@main_bp.route("/download")
def download_data():
    """Public endpoint to download all session data as CSV.
    
    This is a simplified endpoint that doesn't require authentication,
    allowing users to download all session data by visiting the URL directly.
    
    Returns:
        CSV file download with all session data.
        
    Raises:
        404: No session data found.
    """
    # Create temporary file for the consolidated CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp_path = tmp.name
    
    # Export all sessions to the temporary file
    count = session_logger.export_all_sessions_to_csv(tmp_path)
    
    if count == 0:
        os.unlink(tmp_path)
        abort(404, description="No session data found")
    
    # Send the file
    directory = os.path.dirname(tmp_path)
    filename = os.path.basename(tmp_path)
    
    @after_this_request
    def remove_file(response):  # pyright: ignore[reportUnusedFunction]
        """Clean up temporary file after sending response."""
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        return response
    
    return send_from_directory(
        directory, filename, 
        as_attachment=True,
        download_name=f"apt_session_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

@main_bp.route("/api/get_assessment_step", methods=["POST"])
def get_assessment_step():
    """Get assessment step data by step key.
    
    Expected POST data:
        stepKey (str): The key identifying the assessment step.
        
    Returns:
        JSON response with step data or error message.
        
    Raises:
        400: Missing or invalid stepKey parameter.
        404: Step not found.
        500: Server error loading assessment data.
    """
    try:
        # Load the JSON file from the configured path
        config = current_config()
        
        # Check if assessment feature is enabled
        if not config.FEATURE_ASSESSMENT:
            return jsonify({"error": "Assessment feature is disabled"}), 403
            
        with open(config.ASSESSMENT_DATA_FILE, 'r', encoding="utf-8") as f:
            assessment_steps_data = json.load(f)

        data = request.get_json()
        step_key = data.get("stepKey")
        
        if not step_key:
            return jsonify({"error": "Missing stepKey parameter"}), 400
        
        # Validate step key to prevent path traversal
        if not InputValidator.validate_step_key(step_key):
            return jsonify({"error": "Invalid stepKey format"}), 400

        # Retrieve the assessment step data associated with the stepKey
        step_data = assessment_steps_data.get(step_key)

        if step_data:
            return jsonify(step_data)
        else:
            return jsonify({"error": "Step not found"}), 404
            
    except FileNotFoundError:
        return jsonify({"error": "Assessment steps file not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode the assessment steps JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to load assessment steps: {str(e)}"}), 500
