import os
import re
from datetime import datetime


class Logger:
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    log_file_name = "conversations.log"
    log_file_path = os.path.join(log_dir, log_file_name)

    @classmethod
    def init(cls):
        """Ensure that the log directory exists."""
        if not os.path.exists(cls.log_dir):
            os.makedirs(cls.log_dir)

    @classmethod
    def log_conversation(cls, chatbot_type, user_message, bot_response, user_ip):
        """Log the conversation with a timestamp and a masked IP address."""
        cls.init()
        masked_ip = cls.mask_ip(user_ip)
        log_entry = (
            f"[{datetime.utcnow().isoformat()}] IP: {masked_ip} | Chatbot: {chatbot_type}\n"
            f"User: {user_message}\n"
            f"Bot: {bot_response}\n\n"
        )
        try:
            with open(cls.log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            # If logging fails, output the error to the console (or consider raising an exception)
            print(f"Error logging conversation: {e}")

    @staticmethod
    def mask_ip(ip_address):
        """Mask the middle portion of an IP address for privacy."""
        if not ip_address or len(ip_address) < 5:
            return "Unknown"
        clean_ip = re.sub(r"[^0-9.]", "", ip_address)
        if len(clean_ip) <= 5:
            return clean_ip
        return f"{clean_ip[:2]}{'*' * (len(clean_ip) - 5)}{clean_ip[-3:]}"
