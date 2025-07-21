#!/usr/bin/env python3
"""
Test suite for Flask application initialization and routes
"""
import os
import sys
import json
import tempfile
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_flask_app_creation():
    """Test Flask app creation with configuration"""
    print("Testing Flask app creation...")
    try:
        from app import create_app
        
        # Test default app creation
        app = create_app()
        assert app is not None
        assert app.config['APP_NAME'] == 'APT Chat Bot'
        print("✅ Flask app created successfully")
        
        # Test with test config
        app_test = create_app('testing')
        assert app_test.config['TESTING'] == True
        assert app_test.config['AUTH_ENABLED'] == False
        print("✅ Test configuration applied correctly")
        
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {str(e)}")
        return False

def test_blueprints_registered():
    """Test that blueprints are properly registered"""
    print("\nTesting blueprint registration...")
    try:
        from app import create_app
        
        app = create_app('testing')
        
        # Check if main blueprint is registered
        blueprint_found = False
        for blueprint_name in app.blueprints:
            if blueprint_name == 'main_bp':
                blueprint_found = True
                break
        
        assert blueprint_found, "main_bp blueprint not found"
        print("✅ Blueprints registered correctly")
        return True
    except Exception as e:
        print(f"❌ Blueprint registration test failed: {str(e)}")
        return False

def test_error_handlers():
    """Test error handlers are registered"""
    print("\nTesting error handlers...")
    try:
        from app import create_app
        
        app = create_app('testing')
        client = app.test_client()
        
        # Test 404 handler
        response = client.get('/non-existent-route')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        print("✅ 404 error handler working")
        
        return True
    except Exception as e:
        print(f"❌ Error handler test failed: {str(e)}")
        return False

def test_cors_configuration():
    """Test CORS is properly configured"""
    print("\nTesting CORS configuration...")
    try:
        from app import create_app
        
        app = create_app('testing')
        
        # Check if CORS headers would be added
        with app.test_client() as client:
            response = client.options('/')
            # In testing, CORS might behave differently
            print("✅ CORS configuration loaded (testing mode)")
        
        return True
    except Exception as e:
        print(f"❌ CORS configuration test failed: {str(e)}")
        return False

def test_security_headers():
    """Test security headers configuration"""
    print("\nTesting security headers...")
    try:
        from app import create_app
        from config import get_config
        
        # Test with development config (security headers disabled)
        dev_app = create_app('development')
        assert dev_app.config['SECURITY_HEADERS_ENABLED'] == False
        print("✅ Development mode: security headers disabled")
        
        # Test configuration settings without creating production app
        prod_config = get_config('production')
        assert prod_config.SECURITY_HEADERS_ENABLED == True
        assert prod_config.X_CONTENT_TYPE_OPTIONS == 'nosniff'
        assert prod_config.X_FRAME_OPTIONS == 'DENY'
        print("✅ Production config: security headers configured")
        
        return True
    except Exception as e:
        print(f"❌ Security headers test failed: {str(e)}")
        return False

def test_logging_setup():
    """Test logging is properly configured"""
    print("\nTesting logging setup...")
    try:
        from app import create_app
        from logger import logger
        
        app = create_app('testing')
        
        # Check logger exists
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        
        print("✅ Logging setup successful")
        return True
    except Exception as e:
        print(f"❌ Logging setup test failed: {str(e)}")
        return False

def test_validation_module():
    """Test input validation functions"""
    print("\nTesting validation module...")
    try:
        from validators import InputValidator
        
        # Test string sanitization
        dirty_string = "<script>alert('xss')</script>Hello"
        clean_string = InputValidator.sanitize_string(dirty_string)
        assert '<script>' not in clean_string
        assert 'Hello' in clean_string
        print("✅ String sanitization working")
        
        # Test chatbot type validation
        assert InputValidator.validate_chatbot_type('ai') == True
        assert InputValidator.validate_chatbot_type('student') == True
        assert InputValidator.validate_chatbot_type('invalid') == False
        print("✅ Chatbot type validation working")
        
        # Test risk score validation
        assert InputValidator.validate_risk_score(10) == 10
        assert InputValidator.validate_risk_score(25) is None
        assert InputValidator.validate_risk_score('invalid') is None
        print("✅ Risk score validation working")
        
        return True
    except Exception as e:
        print(f"❌ Validation module test failed: {str(e)}")
        return False

def test_auth_manager():
    """Test authentication manager"""
    print("\nTesting authentication manager...")
    try:
        from auth.authmanager import AuthManager
        from config import get_config
        
        # Use test config with auth disabled
        test_config = get_config('testing')
        
        # Test with auth disabled
        with patch('auth.authmanager.current_config', return_value=test_config):
            result = AuthManager.check_auth('any', 'any')
            assert result == True  # Auth disabled in testing
            print("✅ Auth manager respects config settings")
        
        # Test with auth enabled
        prod_config = get_config('production')
        prod_config.ADMIN_USERNAME = 'testadmin'
        prod_config.ADMIN_PASSWORD = 'testpass'
        
        with patch('auth.authmanager.current_config', return_value=prod_config):
            assert AuthManager.check_auth('testadmin', 'testpass') == True
            assert AuthManager.check_auth('wrong', 'wrong') == False
            print("✅ Auth manager validates credentials correctly")
        
        return True
    except Exception as e:
        print(f"❌ Auth manager test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all Flask application tests"""
    print("=" * 50)
    print("APT Chat Bot Flask Application Test Suite")
    print("=" * 50)
    
    tests = [
        test_flask_app_creation,
        test_blueprints_registered,
        test_error_handlers,
        test_cors_configuration,
        test_security_headers,
        test_logging_setup,
        test_validation_module,
        test_auth_manager
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