# app.py
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, abort, Response, jsonify
import os
from dotenv import load_dotenv
from datetime import datetime
import re

# 1. Import from your local files
from authmanager import AuthManager, requires_auth
from chatbot import Chatbot
from logger import Logger

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')

@app.route("/", methods=["GET", "POST"])
def home():
    if "openai_api_key" not in session:
        session["openai_api_key"] = os.getenv('OPENAI_API_KEY')
    if "fine_tuned_model" not in session:
        session["fine_tuned_model"] = Chatbot.default_model

    if request.method == "POST":
        data = request.get_json()
        user_message = data.get("message")
        chatbot_type = data.get("chatbot_type")

        if chatbot_type not in ["A", "B"]:
            return jsonify({"error": "Invalid chatbot type."}), 400

        api_key = session.get("openai_api_key")
        bot_response = Chatbot.get_response(chatbot_type, user_message, api_key)
        
        user_ip = request.remote_addr or "Unknown"
        Logger.log_conversation(chatbot_type, user_message, bot_response, user_ip)

        return jsonify({"bot_response": bot_response})

    return render_template("home.html")

@app.route('/download_logs')
@requires_auth
def download_logs():
    try:
        return send_from_directory(os.path.dirname(Logger.log_file_path), 'conversations.log', as_attachment=True)
    except FileNotFoundError:
        abort(404, description="Log file not found.")
