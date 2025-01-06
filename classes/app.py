from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, abort, Response, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import re
from functools import wraps
# Import classes
from auth_manager import AuthManager, requires_auth  # Import AuthManager class and decorator
from chatbot import Chatbot  # Import Chatbot class
from logger import Logger  # Import Logger class

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')  # Load from .env or use default

# Home route handling both home page and chat functionalities
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
        
        # IP 주소 기록을 위해 가져오기
        user_ip = request.remote_addr or "Unknown"
        Logger.log_conversation(chatbot_type, user_message, bot_response, user_ip)

        return jsonify({"bot_response": bot_response})

    return render_template("home.html")

# Log file download route (protected)
@app.route('/download_logs')
@requires_auth
def download_logs():
    """
    로그 파일을 다운로드할 수 있는 라우트입니다.
    관리자만 접근할 수 있습니다.
    """
    try:
        # send_from_directory는 positional arguments로 directory와 path를 받습니다.
        return send_from_directory(os.path.dirname(Logger.log_file_path), 'conversations.log', as_attachment=True)
    except FileNotFoundError:
        abort(404, description="Log file not found.")


# Random 배정 - 시스템 구현 가능 - formal, informal은 비공개로 (before reveal)
# 사진 * 2 Random = 총 4개
# AOD
# 성별
# 이름 하나만 Tylor(v), Alex
# 5A
# 지금은 설정창 필요 없음
# 데이터 나오는거 seperate 으로

# 무조건 1분인지. 아직안끝났다면 어떻게 해야할지 ?
# 만약 무조건 1분이라면 질문의 개수가 몇개일지 ?
# 애널리스트를 그렇게 한다. - 이거는 상관없다. 

# 일분간 진행됩니다. 그럴수도있고 아닐수도있고 - 다음 답변을 받고 " 끝~ 이런거 던져주자 "

# 끝나고나서
# 그다음 설문조사 - 틀이 있는지?
# 설문조사 형태가 존재한다. - 이건 데이터를