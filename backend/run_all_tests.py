#!/usr/bin/env python3
"""
Run all tests for APT Chat Bot
"""
import os
import subprocess
import sys

def run_test(test_file, description):
    """Run a single test file and return results"""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print('='*60)
    
    # Set test environment variables
    env = os.environ.copy()
    env['FLASK_ENV'] = 'testing'
    env['OPENAI_API_KEY'] = 'test-key-for-testing'
    env['ADMIN_USERNAME'] = 'testadmin'
    env['ADMIN_PASSWORD'] = 'testpass123'
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            env=env,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run {test_file}: {e}")
        return False

def main():
    """Run all tests and summarize results"""
    print("🧪 APT Chat Bot Complete Test Suite")
    print("="*60)
    
    tests = [
        ("test_config.py", "Configuration System Tests"),
        ("test_flask_app.py", "Flask Application Tests"),
        ("test_integration.py", "Integration Tests")
    ]
    
    results = []
    
    for test_file, description in tests:
        success = run_test(test_file, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "="*60)
    print("📊 FINAL TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description}: {status}")
    
    print("-"*60)
    print(f"Total: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All tests passed! The system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())