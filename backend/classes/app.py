# app.py
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, abort, Response, jsonify
import os
from dotenv import load_dotenv
from datetime import datetime
import re
from flask_cors import CORS

# 1. Import from your local files
from authmanager import AuthManager, requires_auth
from chatbot import Chatbot
from custom_logger import Logger

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')

# CORS 설정 (프론트엔드 3000번 포트를 허용)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET", "POST"])
def home():
    """
    간단 테스트용 엔드포인트
    POST / => JSON(body:{message, chatbot_type}) 받으면
              Chatbot.get_response()로 처리 후 결과 반환
    """
    # 세션 초기 설정
    session["openai_api_key"] = os.getenv('OPENAI_API_KEY')
    session["fine_tuned_model"] = Chatbot.default_model
    if "fine_tuned_model" not in session:
        session["fine_tuned_model"] = Chatbot.default_model

    if request.method == "POST":
        data = request.get_json()
        user_message = data.get("message")
        chatbot_type = data.get("chatbot_type")

        if chatbot_type not in ["A", "B"]:
            # 실제로는 "A/B" 둘 다가 아닌 경우 에러를 줄 수 있음
            return jsonify({"error": "Invalid chatbot type."}), 400

        api_key = session.get("openai_api_key")
        bot_response = Chatbot.get_response(chatbot_type, user_message, api_key)
        
        user_ip = request.remote_addr or "Unknown"
        Logger.log_conversation(chatbot_type, user_message, bot_response, user_ip)

        return jsonify({"bot_response": bot_response})

    # GET 요청일 때
    return jsonify({"message": "!!!!!Hello from Flask backend!!!!!"})

@app.route('/download_logs')
@requires_auth
def download_logs():
    """
    로그 파일 다운로드 (Basic Auth 보호)
    """
    try:
        return send_from_directory(os.path.dirname(Logger.log_file_path), 'conversations.log', as_attachment=True)
    except FileNotFoundError:
        abort(404, description="Log file not found.")
