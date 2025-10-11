#!/usr/bin/env python3
"""
Comprehensive Test Suite Runner

This script runs all comprehensive API tests and generates a detailed report.
It includes:
- Individual endpoint test suites
- Integration tests
- Performance tests
- Error handling tests
- Security tests
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def run_test_suite(test_file, description):
    """Run a specific test suite and return results"""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_file, 
            "-v", 
            "--tb=short",
            "--color=yes"
        ], capture_output=True, text=True, cwd="tests")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Duration: {duration:.2f} seconds")
        
        if result.returncode == 0:
            print(f"✅ {description} - ALL TESTS PASSED")
            return True, result.stdout, result.stderr, duration
        else:
            print(f"❌ {description} - SOME TESTS FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False, result.stdout, result.stderr, duration
            
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"💥 {description} - ERROR RUNNING TESTS: {str(e)}")
        return False, "", str(e), duration


def generate_test_report(results):
    """Generate a comprehensive test report"""
    report_lines = []
    report_lines.append("# Comprehensive API Test Report")
    report_lines.append(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    total_suites = len(results)
    passed_suites = sum(1 for result in results if result['passed'])
    total_duration = sum(result['duration'] for result in results)
    
    report_lines.append("## Summary")
    report_lines.append(f"- Total Test Suites: {total_suites}")
    report_lines.append(f"- Passed Suites: {passed_suites}")
    report_lines.append(f"- Failed Suites: {total_suites - passed_suites}")
    report_lines.append(f"- Total Duration: {total_duration:.2f} seconds")
    report_lines.append("")
    
    report_lines.append("## Test Suite Results")
    report_lines.append("")
    
    for result in results:
        status = "✅ PASSED" if result['passed'] else "❌ FAILED"
        report_lines.append(f"### {result['description']}")
        report_lines.append(f"- Status: {status}")
        report_lines.append(f"- Duration: {result['duration']:.2f} seconds")
        
        if result['stdout']:
            report_lines.append("- Output:")
            report_lines.append("```")
            report_lines.append(result['stdout'])
            report_lines.append("```")
        
        if result['stderr']:
            report_lines.append("- Errors:")
            report_lines.append("```")
            report_lines.append(result['stderr'])
            report_lines.append("```")
        
        report_lines.append("")
    
    return "\n".join(report_lines)


def main():
    """Main test runner function"""
    print("🚀 Starting Comprehensive API Test Suite")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Define test suites to run
    test_suites = [
        {
            "file": "test_cases_api_comprehensive.py",
            "description": "Cases API Comprehensive Tests"
        },
        {
            "file": "test_documents_api_comprehensive.py", 
            "description": "Documents API Comprehensive Tests"
        },
        {
            "file": "test_corpus_api_comprehensive.py",
            "description": "Corpus API Comprehensive Tests"
        },
        {
            "file": "test_docs_api_comprehensive.py",
            "description": "Documentation API Comprehensive Tests"
        },
        {
            "file": "test_playbooks_api_comprehensive.py",
            "description": "Playbooks API Comprehensive Tests"
        },
        {
            "file": "test_api_comprehensive_suite.py",
            "description": "Cross-Endpoint Integration & Performance Tests"
        }
    ]
    
    results = []
    overall_start_time = time.time()
    
    # Run each test suite
    for suite in test_suites:
        passed, stdout, stderr, duration = run_test_suite(
            suite["file"], 
            suite["description"]
        )
        
        results.append({
            "file": suite["file"],
            "description": suite["description"],
            "passed": passed,
            "stdout": stdout,
            "stderr": stderr,
            "duration": duration
        })
    
    overall_end_time = time.time()
    overall_duration = overall_end_time - overall_start_time
    
    # Generate and save report
    report = generate_test_report(results)
    
    report_file = "comprehensive_test_report.md"
    with open(report_file, "w") as f:
        f.write(report)
    
    # Print summary
    print("\n" + "=" * 60)
    print("🏁 COMPREHENSIVE TEST SUITE COMPLETE")
    print("=" * 60)
    
    total_suites = len(results)
    passed_suites = sum(1 for result in results if result['passed'])
    
    print(f"📊 Results Summary:")
    print(f"   Total Suites: {total_suites}")
    print(f"   Passed: {passed_suites}")
    print(f"   Failed: {total_suites - passed_suites}")
    print(f"   Overall Duration: {overall_duration:.2f} seconds")
    print(f"   Report saved to: {report_file}")
    
    if passed_suites == total_suites:
        print("\n🎉 ALL TEST SUITES PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total_suites - passed_suites} TEST SUITE(S) FAILED")
        print("Check the detailed report for more information.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)