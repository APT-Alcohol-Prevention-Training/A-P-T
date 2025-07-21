#!/usr/bin/env python3
"""
Test suite for APT Chat Bot configuration system
"""
import os
import sys
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_loading():
    """Test basic configuration loading"""
    print("Testing configuration loading...")
    try:
        from config import get_config, current_config
        
        # Test default config
        config = current_config()
        assert config.APP_NAME == "APT Chat Bot"
        assert config.APP_VERSION == "1.0.0"
        print("✅ Default configuration loaded successfully")
        
        # Test development config
        dev_config = get_config('development')
        assert dev_config.DEBUG == True
        print("✅ Development configuration loaded successfully")
        
        # Test production config
        prod_config = get_config('production')
        assert prod_config.DEBUG == False
        assert prod_config.SECURITY_HEADERS_ENABLED == True
        print("✅ Production configuration loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {str(e)}")
        return False

def test_config_validation():
    """Test configuration validation"""
    print("\nTesting configuration validation...")
    try:
        from config import Config
        
        # Test directory creation
        with tempfile.TemporaryDirectory() as tmpdir:
            Config.BASE_DIR = Path(tmpdir)
            Config.LOG_DIR = Config.BASE_DIR / "logs"
            Config.SESSION_LOG_DIR = Config.LOG_DIR / "session_logs"
            Config.ACTIVE_SESSION_DIR = Config.SESSION_LOG_DIR / "active"
            Config.COMPLETED_SESSION_DIR = Config.SESSION_LOG_DIR / "completed"
            
            Config.create_directories()
            
            assert Config.LOG_DIR.exists()
            assert Config.SESSION_LOG_DIR.exists()
            assert Config.ACTIVE_SESSION_DIR.exists()
            assert Config.COMPLETED_SESSION_DIR.exists()
            print("✅ Directory creation successful")
        
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {str(e)}")
        return False

def test_openai_config():
    """Test OpenAI configuration"""
    print("\nTesting OpenAI configuration...")
    try:
        from config import current_config
        
        config = current_config()
        openai_config = config.get_openai_config()
        
        # Check all required fields
        required_fields = ['api_key', 'model', 'temperature', 'max_tokens', 
                          'top_p', 'frequency_penalty', 'presence_penalty', 
                          'timeout', 'max_retries']
        
        for field in required_fields:
            assert field in openai_config
            print(f"  ✓ {field}: {openai_config[field] if field != 'api_key' else '***'}")
        
        print("✅ OpenAI configuration structure valid")
        return True
    except Exception as e:
        print(f"❌ OpenAI configuration test failed: {str(e)}")
        return False

def test_cors_config():
    """Test CORS configuration"""
    print("\nTesting CORS configuration...")
    try:
        from config import current_config
        
        config = current_config()
        cors_config = config.get_cors_config()
        
        assert 'origins' in cors_config
        assert 'allow_headers' in cors_config
        assert 'methods' in cors_config
        assert 'supports_credentials' in cors_config
        
        print(f"  ✓ CORS origins: {len(cors_config['origins'])} configured")
        print(f"  ✓ Allowed methods: {', '.join(cors_config['methods'])}")
        print("✅ CORS configuration valid")
        return True
    except Exception as e:
        print(f"❌ CORS configuration test failed: {str(e)}")
        return False

def test_logging_config():
    """Test logging configuration"""
    print("\nTesting logging configuration...")
    try:
        from config import current_config
        
        config = current_config()
        logging_config = config.get_logging_config()
        
        required_fields = ['level', 'format', 'date_format', 'file_max_bytes',
                          'file_backup_count', 'log_to_file', 'log_to_console', 'log_dir']
        
        for field in required_fields:
            assert field in logging_config
            print(f"  ✓ {field}: {logging_config[field]}")
        
        print("✅ Logging configuration valid")
        return True
    except Exception as e:
        print(f"❌ Logging configuration test failed: {str(e)}")
        return False

def test_environment_specific():
    """Test environment-specific configurations"""
    print("\nTesting environment-specific configurations...")
    try:
        from config import DevelopmentConfig, TestingConfig, ProductionConfig
        
        # Development specific
        assert DevelopmentConfig.DEBUG == True
        assert DevelopmentConfig.CORS_ORIGINS == ["*"]
        print("✅ Development config has relaxed settings")
        
        # Testing specific
        assert TestingConfig.TESTING == True
        assert TestingConfig.AUTH_ENABLED == False
        assert TestingConfig.RATE_LIMIT_ENABLED == False
        print("✅ Testing config has appropriate test settings")
        
        # Production specific
        assert ProductionConfig.DEBUG == False
        assert ProductionConfig.SESSION_COOKIE_SECURE == True
        assert ProductionConfig.SECURITY_HEADERS_ENABLED == True
        print("✅ Production config has strict security settings")
        
        return True
    except Exception as e:
        print(f"❌ Environment-specific test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all configuration tests"""
    print("=" * 50)
    print("APT Chat Bot Configuration Test Suite")
    print("=" * 50)
    
    tests = [
        test_config_loading,
        test_config_validation,
        test_openai_config,
        test_cors_config,
        test_logging_config,
        test_environment_specific
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