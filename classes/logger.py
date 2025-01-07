# logger.py
import os
import re
from datetime import datetime

class Logger:
    # log_file_path will point to classes/logs (a file named 'logs' in this example)
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

    @classmethod
    def init(cls):
        log_dir = os.path.dirname(cls.log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    @classmethod
    def log_conversation(cls, chatbot_type, user_message, bot_response, user_ip):
        masked_ip = cls.mask_ip(user_ip)
        log_entry = f"[{datetime.utcnow().isoformat()}] IP: {masked_ip} | Chatbot: {chatbot_type}\n"
        log_entry += f"User: {user_message}\nBot: {bot_response}\n\n"

        try:
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
