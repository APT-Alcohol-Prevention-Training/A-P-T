from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, abort, Response, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import re
from functools import wraps

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')  # Load from .env or use default

# Logger Class
class Logger:
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

    @classmethod
    def init(cls):
        log_dir = os.path.dirname(cls.log_file_path)
        # 로그 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    @classmethod
    def log_conversation(cls, chatbot_type, user_message, bot_response, user_ip):
        # """
        # 대화 내용을 로그 파일에 기록합니다.
        
        # :param chatbot_type: 챗봇 유형 (A 또는 B)
        # :param user_message: 사용자가 보낸 메시지
        # :param bot_response: 챗봇의 응답
        # :param user_ip: 사용자의 IP 주소
        # """
        masked_ip = mask_ip(user_ip)  # IP 주소 마스킹
        
        log_entry = f"[{datetime.utcnow().isoformat()}] IP: {masked_ip} | Chatbot: {chatbot_type}\n"
        log_entry += f"User: {user_message}\nBot: {bot_response}\n\n"
        
        try:
            with open(cls.log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(f"Error logging conversation: {e}")
    @staticmethod
    def mask_ip(ip_address):
        # """
        # IP 주소를 마스킹하여 앞 2자리와 뒤 3자리만 표시합니다.
        # 예: '192.168.1.10' -> '19*****010'
        
        # :param ip_address: 원본 IP 주소 문자열
        # :return: 마스킹된 IP 주소 문자열
        # """
        if not ip_address or len(ip_address) < 5:
            return 'Unknown'
        
        # IP 주소에서 숫자와 점(.)만 추출
        clean_ip = re.sub(r'[^0-9.]', '', ip_address)
        
        # 길이에 따라 마스킹 처리
        if len(clean_ip) <= 5:
            return clean_ip  # 너무 짧으면 그대로 반환
        else:
            return f"{clean_ip[:2]}{'*' * (len(clean_ip) - 5)}{clean_ip[-3:]}"
        
# Authentication Manager Class
class AuthManager:
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')

    @classmethod
    def check_auth(cls, username, password):
        # """
        # 관리자 인증을 확인합니다.
        
        # :param username: 입력된 사용자 이름
        # :param password: 입력된 비밀번호
        # :return: 인증 성공 여부
        # """
        return username == cls.admin_username and password == cls.admin_password
    @staticmethod
    def authenticate():
        """
        인증 실패 시 401 응답을 반환합니다.
        """
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials.', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Decorator for Authentication
def requires_auth(f):
    """
    기본 인증을 요구하는 데코레이터입니다.
    
    :param f: 보호할 함수
    :return: 보호된 함수
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not AuthManager.check_auth(auth.username, auth.password):
            return AuthManager.authenticate()
        return f(*args, **kwargs)
    return decorated

# Chatbot Class
class Chatbot:
    default_model = os.getenv('OPENAI_DEFAULT_MODEL')

    # Function to get chatbot response
    @classmethod
    def get_response(cls, chatbot_type, user_message, api_key):
        # Use session-specific model or default
        fine_tuned_model = session.get('fine_tuned_model', cls.default_model)

        if not api_key or not fine_tuned_model:
            return "Please configure API key and model ID first."

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        if chatbot_type == 'A':
            style_instruction = "Respond in an informal, friendly, and casual manner."
        else:
            style_instruction = "Respond in a formal and official manner."

        messages = [
            {"role": "system", "content": f"{style_instruction}"},
            {"role": "user", "content": user_message}
        ]

        try:
            response = client.chat.completions.create(
                model=fine_tuned_model,  # Use the fine-tuned model from session or class default
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return "I'm sorry, I encountered an error. Please try again later."
        
# Home route
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

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

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