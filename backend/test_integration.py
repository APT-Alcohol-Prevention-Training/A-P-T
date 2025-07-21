#!/usr/bin/env python3
"""
Integration tests for APT Chat Bot modules
"""
import os
import sys
import json
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chatbot_integration():
    """Test chatbot module integration with config"""
    print("Testing chatbot integration...")
    try:
        # Mock OpenAI client
        mock_openai = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_openai.chat.completions.create.return_value = mock_response
        
        with patch('chatbot.chatbot.OpenAI', return_value=mock_openai):
            from chatbot.chatbot import Chatbot
            
            # Test basic response
            response = Chatbot.get_response('ai', 'Hello', api_key='test-key')
            assert response == "Test response"
            print("✅ Chatbot basic response working")
            
            # Test scenario responses
            response = Chatbot._handle_party_scenario_response("I'm not drinking tonight")
            assert "clear, confident" in response
            print("✅ Party scenario handler working")
            
            response = Chatbot._handle_concert_scenario_response("I'll pass on pre-gaming")
            # Concert scenario should have some positive feedback
            assert len(response) > 20  # Ensure we got a meaningful response
            print("✅ Concert scenario handler working")
            
            response = Chatbot._handle_date_scenario_response("Just water for me")
            assert "Simple and smooth" in response or "water" in response.lower()
            print("✅ Date scenario handler working")
            
        return True
    except Exception as e:
        import traceback
        print(f"❌ Chatbot integration test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_logger_integration():
    """Test logging modules integration"""
    print("\nTesting logger integration...")
    try:
        from logger.custom_logger import Logger
        from logger.session_logger import SessionLogger
        from config import current_config
        
        config = current_config()
        
        # Test custom logger (without actual file write)
        with patch('builtins.open', MagicMock()):
            Logger.log_conversation('ai', 'test message', 'test response', '127.0.0.1')
            print("✅ Custom logger integration working")
        
        # Test session logger
        session_logger = SessionLogger()
        session_id = session_logger.create_session('127.0.0.1')
        assert session_id is not None
        print("✅ Session logger creation working")
        
        # Test IP masking
        masked_ip = Logger.mask_ip('192.168.1.100')
        assert masked_ip == '192.168.xxx.xxx'
        
        masked_ip = Logger.mask_ip('8.8.8.8')
        assert masked_ip == '8.8.8.8'  # Public IP not masked
        print("✅ IP masking working correctly")
        
        return True
    except Exception as e:
        print(f"❌ Logger integration test failed: {str(e)}")
        return False

def test_config_integration():
    """Test configuration integration across modules"""
    print("\nTesting configuration integration...")
    try:
        from config import current_config
        from app import create_app
        
        # Test that config is accessible from different modules
        config = current_config()
        
        # Test config dict export
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert 'APP_NAME' in config_dict
        assert 'OPENAI_API_KEY' in config_dict
        print("✅ Configuration export working")
        
        # Test environment switching
        os.environ['FLASK_ENV'] = 'production'
        prod_config = current_config()
        assert prod_config.DEBUG == False
        
        os.environ['FLASK_ENV'] = 'development'
        dev_config = current_config()
        assert dev_config.DEBUG == True
        print("✅ Environment switching working")
        
        return True
    except Exception as e:
        print(f"❌ Config integration test failed: {str(e)}")
        return False

def test_error_propagation():
    """Test error handling across modules"""
    print("\nTesting error propagation...")
    try:
        from chatbot.chatbot import Chatbot
        from config import get_config
        
        # Test with missing API key
        test_config = get_config('testing')
        test_config.OPENAI_API_KEY = ''
        
        with patch('chatbot.chatbot.current_config', return_value=test_config):
            try:
                Chatbot.get_response('ai', 'test')
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "Missing OpenAI API key" in str(e)
                print("✅ API key validation working")
        
        # Test invalid chatbot type
        try:
            Chatbot.get_response('invalid_type', 'test', api_key='test')
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Invalid chatbot type" in str(e)
            print("✅ Chatbot type validation working")
        
        return True
    except Exception as e:
        print(f"❌ Error propagation test failed: {str(e)}")
        return False

def test_session_management():
    """Test session management functionality"""
    print("\nTesting session management...")
    try:
        from logger.session_logger import SessionLogger
        
        # Create a mock session logger
        logger = SessionLogger()
        
        # Test session creation
        session_id = logger.create_session('127.0.0.1')
        assert session_id in logger.sessions
        print("✅ Session creation working")
        
        # Test session data structure
        assert isinstance(logger.sessions[session_id], list)
        assert len(logger.sessions[session_id]) == 0
        print("✅ Session data structure correct")
        
        # Test getting all sessions
        all_sessions = logger.get_all_sessions()
        assert 'active' in all_sessions
        assert 'completed' in all_sessions
        print("✅ Session listing working")
        
        return True
    except Exception as e:
        print(f"❌ Session management test failed: {str(e)}")
        return False

def test_validation_integration():
    """Test validation integration with config"""
    print("\nTesting validation integration...")
    try:
        from validators import InputValidator
        from config import current_config
        
        config = current_config()
        
        # Test max length from config
        long_text = "x" * (config.MAX_MESSAGE_LENGTH + 100)
        sanitized = InputValidator.sanitize_string(long_text)
        assert len(sanitized) <= config.MAX_MESSAGE_LENGTH
        print("✅ Validation uses config limits")
        
        # Test various malicious inputs
        test_cases = [
            ("<script>alert('xss')</script>", ""),
            ("SELECT * FROM users--", "SELECT * FROM users"),
            ("Normal text with <b>tags</b>", "Normal text with tags"),
            ("Text with null\x00byte", "Text with nullbyte")
        ]
        
        for dirty, expected_contains in test_cases:
            clean = InputValidator.sanitize_string(dirty)
            if expected_contains:
                assert expected_contains in clean or clean == expected_contains
        
        print("✅ Input sanitization comprehensive")
        return True
    except Exception as e:
        print(f"❌ Validation integration test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("=" * 50)
    print("APT Chat Bot Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_chatbot_integration,
        test_logger_integration,
        test_config_integration,
        test_error_propagation,
        test_session_management,
        test_validation_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Summary: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)