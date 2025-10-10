#!/usr/bin/env python3
"""
Test runner for corpus-related unit tests.

This script runs all the unit tests for the corpus functionality including:
- Corpus API endpoints
- DataService corpus methods  
- Corpus models validation

Usage:
    python run_corpus_tests.py
    python run_corpus_tests.py --verbose
    python run_corpus_tests.py --coverage
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(verbose=False, coverage=False, specific_test=None):
    """Run corpus unit tests with optional coverage and verbosity."""
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Test files to run
    test_files = [
        "tests/unit/test_corpus_api.py",
        "tests/unit/test_data_service_corpus.py", 
        "tests/unit/test_corpus_models.py"
    ]
    
    if specific_test:
        test_files = [f"tests/unit/{specific_test}"]
    
    # Add test files to command
    cmd.extend(test_files)
    
    # Add verbosity flag
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Add coverage if requested
    if coverage:
        cmd.extend([
            "--cov=app.api.corpus",
            "--cov=app.services.data_service", 
            "--cov=app.models.corpus",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov/corpus"
        ])
    
    # Add other useful flags
    cmd.extend([
        "--tb=short",  # Shorter traceback format
        "--strict-markers",  # Strict marker checking
        "-x"  # Stop on first failure
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Run corpus unit tests")
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Run tests in verbose mode"
    )
    parser.add_argument(
        "-c", "--coverage", 
        action="store_true", 
        help="Run tests with coverage reporting"
    )
    parser.add_argument(
        "-t", "--test", 
        help="Run specific test file (e.g., test_corpus_api.py)"
    )
    parser.add_argument(
        "--install-deps", 
        action="store_true", 
        help="Install test dependencies before running"
    )
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        subprocess.run([
            "pip", "install", "-r", "requirements-test.txt"
        ], cwd=Path(__file__).parent)
        print("-" * 60)
    
    # Run the tests
    exit_code = run_tests(
        verbose=args.verbose,
        coverage=args.coverage,
        specific_test=args.test
    )
    
    if exit_code == 0:
        print("\n✅ All corpus tests passed!")
        if args.coverage:
            print("📊 Coverage report generated in htmlcov/corpus/")
    else:
        print("\n❌ Some tests failed!")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())