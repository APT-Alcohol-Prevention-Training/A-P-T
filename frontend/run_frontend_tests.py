#!/usr/bin/env python3
"""
Frontend Test Runner for APT Chat Bot
"""
import os
import subprocess
import sys
import json
from datetime import datetime

class FrontendTestRunner:
    def __init__(self):
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'summary': {}
        }
        
    def check_dependencies(self):
        """Check if Node.js and npm are installed"""
        print("🔍 Checking dependencies...")
        
        try:
            node_version = subprocess.check_output(['node', '--version'], text=True).strip()
            print(f"✅ Node.js {node_version} found")
        except:
            print("❌ Node.js not found. Please install Node.js")
            return False
            
        try:
            npm_version = subprocess.check_output(['npm', '--version'], text=True).strip()
            print(f"✅ npm {npm_version} found")
        except:
            print("❌ npm not found. Please install npm")
            return False
            
        return True
    
    def install_test_dependencies(self):
        """Install testing dependencies"""
        print("\n📦 Installing test dependencies...")
        
        # Check if node_modules exists
        if not os.path.exists('node_modules'):
            print("Installing project dependencies...")
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
        
        # Install test-specific dependencies
        test_deps = [
            '@testing-library/react@^14.1.2',
            '@testing-library/jest-dom@^6.1.5',
            '@testing-library/user-event@^14.5.1',
            'jest@^29.7.0',
            'jest-environment-jsdom@^29.7.0'
        ]
        
        print("Installing testing libraries...")
        for dep in test_deps:
            print(f"  Installing {dep}...")
            result = subprocess.run(['npm', 'install', '--save-dev', dep], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  ⚠️  Warning: Failed to install {dep}")
        
        return True
    
    def run_component_tests(self):
        """Run component unit tests"""
        print("\n🧪 Running Component Tests...")
        
        test_files = [
            'app/page.test.js',
            'app/components/ChooseAvatar.test.js',
            'app/\\[role\\]/page.test.js',  # Escape brackets for Jest
            'app/api/chat/route.test.js'
        ]
        
        results = {}
        for test_file in test_files:
            # Remove escape characters for file existence check
            actual_path = test_file.replace('\\', '')
            if os.path.exists(actual_path):
                print(f"\n  Testing {actual_path}...")
                result = subprocess.run(
                    ['npx', 'jest', test_file, '--verbose'],
                    capture_output=True,
                    text=True
                )
                
                # Jest returns 0 for success, non-zero for failure
                # Console errors during tests don't mean test failure
                if result.returncode == 0:
                    print(f"  ✅ {actual_path} passed")
                    results[actual_path] = {'status': 'passed', 'output': result.stdout}
                else:
                    print(f"  ❌ {actual_path} failed")
                    # Include both stdout and stderr for debugging
                    output = result.stdout + "\n" + result.stderr if result.stderr else result.stdout
                    results[actual_path] = {'status': 'failed', 'output': output}
            else:
                print(f"  ⚠️  {actual_path} not found")
                results[actual_path] = {'status': 'skipped', 'output': 'File not found'}
        
        self.test_results['tests']['components'] = results
        return all(r['status'] == 'passed' for r in results.values() if r['status'] != 'skipped')
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("\n🔗 Running Integration Tests...")
        
        if os.path.exists('integration.test.js'):
            result = subprocess.run(
                ['npx', 'jest', 'integration.test.js', '--verbose'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Integration tests passed")
                self.test_results['tests']['integration'] = {
                    'status': 'passed',
                    'output': result.stdout
                }
                return True
            else:
                print("❌ Integration tests failed")
                self.test_results['tests']['integration'] = {
                    'status': 'failed',
                    'output': result.stderr
                }
                return False
        else:
            print("⚠️  Integration test file not found")
            self.test_results['tests']['integration'] = {
                'status': 'skipped',
                'output': 'File not found'
            }
            return True
    
    def run_coverage_report(self):
        """Generate coverage report"""
        print("\n📊 Generating Coverage Report...")
        
        result = subprocess.run(
            ['npx', 'jest', '--coverage', '--coverageReporters=json-summary'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and os.path.exists('coverage/coverage-summary.json'):
            with open('coverage/coverage-summary.json', 'r') as f:
                coverage_data = json.load(f)
                self.test_results['coverage'] = coverage_data.get('total', {})
                
                # Print coverage summary
                if 'total' in coverage_data:
                    total = coverage_data['total']
                    print(f"  Lines: {total.get('lines', {}).get('pct', 0)}%")
                    print(f"  Statements: {total.get('statements', {}).get('pct', 0)}%")
                    print(f"  Functions: {total.get('functions', {}).get('pct', 0)}%")
                    print(f"  Branches: {total.get('branches', {}).get('pct', 0)}%")
        else:
            print("⚠️  Coverage report generation failed")
            self.test_results['coverage'] = {}
    
    def validate_frontend_structure(self):
        """Validate frontend project structure"""
        print("\n🏗️  Validating Frontend Structure...")
        
        required_files = [
            'package.json',
            'next.config.js',
            'app/layout.js',
            'app/page.js',
            'app/[role]/page.js',
            'app/api/chat/route.js',
            'app/components/ChooseAvatar.js'
        ]
        
        missing = []
        for file in required_files:
            if not os.path.exists(file):
                missing.append(file)
        
        if missing:
            print(f"❌ Missing required files: {', '.join(missing)}")
            return False
        else:
            print("✅ All required files present")
            return True
    
    def check_environment_setup(self):
        """Check environment configuration"""
        print("\n🔧 Checking Environment Setup...")
        
        env_file = '.env.local'
        if os.path.exists(env_file):
            print(f"✅ {env_file} found")
            with open(env_file, 'r') as f:
                content = f.read()
                if 'NEXT_PUBLIC_API_URL' in content:
                    print("  ✓ NEXT_PUBLIC_API_URL configured")
                else:
                    print("  ⚠️  NEXT_PUBLIC_API_URL not configured")
                    
                if 'BACKEND_API_URL' in content:
                    print("  ✓ BACKEND_API_URL configured")
                else:
                    print("  ⚠️  BACKEND_API_URL not configured")
        else:
            print(f"⚠️  {env_file} not found")
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("📋 FRONTEND TEST REPORT")
        print("="*60)
        
        # Count results
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        skipped_tests = 0
        
        for category, tests in self.test_results['tests'].items():
            if isinstance(tests, dict):
                if 'status' in tests:  # Single test
                    total_tests += 1
                    if tests['status'] == 'passed':
                        passed_tests += 1
                    elif tests['status'] == 'failed':
                        failed_tests += 1
                    else:
                        skipped_tests += 1
                else:  # Multiple tests
                    for test_name, test_result in tests.items():
                        total_tests += 1
                        if test_result['status'] == 'passed':
                            passed_tests += 1
                        elif test_result['status'] == 'failed':
                            failed_tests += 1
                        else:
                            skipped_tests += 1
        
        self.test_results['summary'] = {
            'total': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'skipped': skipped_tests,
            'success_rate': f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
        }
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Skipped: {skipped_tests}")
        print(f"\nSuccess Rate: {self.test_results['summary']['success_rate']}")
        
        # Save detailed report
        with open('frontend_test_report.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n📄 Detailed report saved to frontend_test_report.json")
        
        return failed_tests == 0
    
    def run_all_tests(self):
        """Run all frontend tests"""
        print("🚀 APT Chat Bot Frontend Test Suite")
        print("="*60)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Validate structure
        if not self.validate_frontend_structure():
            print("\n❌ Frontend structure validation failed")
            return False
        
        # Check environment
        self.check_environment_setup()
        
        # Install dependencies
        if not self.install_test_dependencies():
            print("\n❌ Failed to install dependencies")
            return False
        
        # Run tests
        component_pass = self.run_component_tests()
        integration_pass = self.run_integration_tests()
        
        # Generate coverage
        self.run_coverage_report()
        
        # Generate report
        all_passed = self.generate_report()
        
        if all_passed:
            print("\n🎉 All frontend tests passed!")
        else:
            print("\n⚠️  Some tests failed. Check the report for details.")
        
        return all_passed


if __name__ == "__main__":
    runner = FrontendTestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)