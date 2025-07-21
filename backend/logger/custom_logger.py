import re
from datetime import datetime
import json
from config import current_config

class Logger:
    @classmethod
    def _get_config(cls):
        """Get current configuration."""
        return current_config()
    
    @classmethod
    def init(cls):
        """Ensure that the log directory exists."""
        config = cls._get_config()
        # Log directory is created by config.create_directories()
        # This method is kept for backward compatibility
        pass

    @classmethod
    def log_conversation(cls, chatbot_type, user_message, bot_response, user_ip):
        """Log the conversation with a timestamp and a masked IP address."""
        config = cls._get_config()
        
        # Only log if logging to file is enabled
        if not config.LOG_TO_FILE:
            return
            
        masked_ip = cls.mask_ip(user_ip)
        
        # Create JSON format log entry
        log_data = {
            "timestamp": datetime.now().strftime(config.LOG_DATE_FORMAT),
            "ip_address": masked_ip,
            "chatbot_type": chatbot_type,
            "user_message": user_message,
            "bot_response": bot_response
        }
        
        log_file_path = config.LOG_DIR / "conversations.log"
        
        try:
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(json.dumps(log_data) + "\n")
        except Exception as e:
            if config.DEBUG:
                print(f"Error logging conversation: {e}")

    @staticmethod
    def mask_ip(ip_address):
        """Mask the last two octets of an IP address for privacy."""
        if not ip_address or ip_address == "Unknown":
            return "Unknown"
        
        # Check if it's a valid IP address format and extract octets
        ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
        match = re.match(ip_pattern, ip_address)
        
        if not match:
            return "Unknown"
        
        # Extract octets from regex groups
        first_octet = int(match.group(1))
        second_octet = int(match.group(2))
        
        # Check if it's a private IP address
        # Private IP ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
        if (first_octet == 10 or 
            (first_octet == 172 and 16 <= second_octet <= 31) or 
            (first_octet == 192 and second_octet == 168)):
            # Mask last two octets for private IPs
            return f"{match.group(1)}.{match.group(2)}.xxx.xxx"
        
        # For public IPs, don't mask
        return ip_address
