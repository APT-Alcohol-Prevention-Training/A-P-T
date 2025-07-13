"""
Input validation utilities for the backend
"""
import html
import re
from typing import Dict, Any, Optional


class InputValidator:
    """Validates and sanitizes user input"""
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """
        Sanitize a string by removing potentially harmful characters
        and limiting length.
        
        Args:
            text: Input string to sanitize
            max_length: Maximum allowed length (default: 1000)
            
        Returns:
            Sanitized string safe for storage and display
        """
        if not isinstance(text, str):
            return ""
        
        # First, decode any HTML entities to prevent double encoding
        text = html.unescape(text)
        
        # Remove any HTML/XML tags more thoroughly
        # This pattern handles nested tags and attributes
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove any remaining script-related content
        text = re.sub(r'(?i)(javascript:|on\w+\s*=|<script|</script)', '', text)
        
        # Remove SQL injection attempts
        sql_patterns = [
            r"(?i)(union\s+select|drop\s+table|insert\s+into|delete\s+from|update\s+set)",
            r"(?i)(exec\s*\(|execute\s+immediate|xp_cmdshell)",
            r"['\";]--",  # SQL comments
            r"(?i)(or\s+1\s*=\s*1|and\s+1\s*=\s*1)"  # Common SQL injection patterns
        ]
        for pattern in sql_patterns:
            text = re.sub(pattern, '', text)
        
        # Remove null bytes and other dangerous characters
        text = text.replace('\0', '')
        text = text.replace('\x00', '')
        
        # Remove all control characters except newline, tab, and carriage return
        # Keep \t (0x09), \n (0x0A), \r (0x0D)
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
        
        # Normalize whitespace (multiple spaces to single space)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove any Unicode direction override characters (potential security risk)
        text = re.sub(r'[\u202A-\u202E\u2066-\u2069]', '', text)
        
        # Limit length after all cleaning
        text = text[:max_length]
        
        # Final trim
        text = text.strip()
        
        # Ensure we don't return None
        return text if text else ""
    
    @staticmethod
    def validate_chatbot_type(chatbot_type: str) -> bool:
        """Validate chatbot type is one of allowed values"""
        return chatbot_type in ["ai", "student", "doctor"]
    
    @staticmethod
    def validate_risk_score(risk_score: Any) -> Optional[int]:
        """Validate and convert risk score to integer"""
        try:
            score = int(risk_score)
            if 0 <= score <= 20:
                return score
            return None
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def validate_step_key(step_key: str) -> bool:
        """Validate assessment step key format"""
        if not isinstance(step_key, str):
            return False
        
        # Only allow alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', step_key):
            return False
        
        # Limit length to prevent abuse
        if len(step_key) > 50:
            return False
        
        return True
    
    @staticmethod
    def validate_conversation_context(context: Any) -> Dict[str, Any]:
        """Validate and sanitize conversation context"""
        if not isinstance(context, dict):
            return {}
        
        # Only allow specific keys
        allowed_keys = ['party_scenario']
        sanitized = {}
        
        for key in allowed_keys:
            if key in context:
                value = context[key]
                # Validate party_scenario value
                if key == 'party_scenario' and isinstance(value, int) and 1 <= value <= 3:
                    sanitized[key] = value
        
        return sanitized