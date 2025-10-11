#!/usr/bin/env python3
"""Simple test runner for the API"""

import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_api.py", 
        "-v"
    ])
    sys.exit(result.returncode)