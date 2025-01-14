# logger.py

import os
import re
from datetime import datetime

class Logger:
    # logs 디렉토리 밑에 'conversations.log' 라는 파일을 사용하도록 설정
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    log_file_name = 'conversations.log'
    log_file_path = os.path.join(log_dir, log_file_name)

    @classmethod
    def init(cls):
        # logs 폴더가 없으면 생성
        if not os.path.exists(cls.log_dir):
            os.makedirs(cls.log_dir)

    @classmethod
    def log_conversation(cls, chatbot_type, user_message, bot_response, user_ip):
        masked_ip = cls.mask_ip(user_ip)
        log_entry = f"[{datetime.utcnow().isoformat()}] IP: {masked_ip} | Chatbot: {chatbot_type}\n"
        log_entry += f"User: {user_message}\nBot: {bot_response}\n\n"

        try:
            # 이제 log_file_path가 실제 파일 경로이므로 문제 없이 open() 가능
            with open(cls.log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(f"Error logging conversation: {e}")

    @staticmethod
    def mask_ip(ip_address):
        if not ip_address or len(ip_address) < 5:
            return 'Unknown'
        clean_ip = re.sub(r'[^0-9.]', '', ip_address)
        if len(clean_ip) <= 5:
            return clean_ip
        else:
            return f"{clean_ip[:2]}{'*' * (len(clean_ip) - 5)}{clean_ip[-3:]}"
