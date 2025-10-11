#!/usr/bin/env python3
"""
Unit test runner for the Legal AI System services
"""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Run unit tests with coverage reporting"""
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    
    print("Running unit tests for Legal AI System services...")
    print("=" * 60)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/unit/",
        "-v",
        "--tb=short",
        "--cov=app/services",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=80"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=backend_dir, check=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✅ All tests passed!")
            print("📊 Coverage report generated in htmlcov/index.html")
        else:
            print("\n" + "=" * 60)
            print("❌ Some tests failed or coverage is below threshold")
            
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest pytest-cov")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)