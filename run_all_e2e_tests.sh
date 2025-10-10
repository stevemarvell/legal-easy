#!/bin/bash

# End-to-End Test Runner for Case Document Analysis
# This script runs both backend and frontend E2E tests

set -e  # Exit on any error

echo "🚀 Starting End-to-End Tests for Case Document Analysis"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    echo "Checking requirements..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is required but not installed"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is required but not installed"
        exit 1
    fi
    
    print_status "All requirements satisfied"
}

# Start backend server
start_backend() {
    echo "Starting backend server..."
    cd backend
    
    # Install Python dependencies if needed
    if [ ! -d ".venv" ]; then
        print_warning "Creating Python virtual environment..."
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
    else
        source .venv/bin/activate
    fi
    
    # Start backend server in background
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Wait for backend to start
    echo "Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_status "Backend server is running (PID: $BACKEND_PID)"
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_error "Backend server failed to start"
        exit 1
    fi
    
    cd ..
}

# Start frontend server
start_frontend() {
    echo "Starting frontend server..."
    cd frontend
    
    # Install Node dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_warning "Installing Node.js dependencies..."
        npm install
    fi
    
    # Install Playwright if needed
    if [ ! -d "node_modules/@playwright" ]; then
        print_warning "Installing Playwright..."
        npm install @playwright/test
        npx playwright install
    fi
    
    # Start frontend server in background
    npm run dev &
    FRONTEND_PID=$!
    
    # Wait for frontend to start
    echo "Waiting for frontend to start..."
    for i in {1..60}; do
        if curl -s http://localhost:8080 > /dev/null 2>&1; then
            print_status "Frontend server is running (PID: $FRONTEND_PID)"
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:8080 > /dev/null 2>&1; then
        print_error "Frontend server failed to start"
        exit 1
    fi
    
    cd ..
}

# Run backend tests
run_backend_tests() {
    echo ""
    echo "============================================================"
    echo "Running Backend E2E Tests"
    echo "============================================================"
    
    cd backend
    source .venv/bin/activate
    
    if python run_e2e_tests.py; then
        print_status "Backend E2E tests passed"
        BACKEND_TESTS_PASSED=true
    else
        print_error "Backend E2E tests failed"
        BACKEND_TESTS_PASSED=false
    fi
    
    cd ..
}

# Run frontend tests
run_frontend_tests() {
    echo ""
    echo "============================================================"
    echo "Running Frontend E2E Tests"
    echo "============================================================"
    
    cd frontend
    
    if npm run test:e2e; then
        print_status "Frontend E2E tests passed"
        FRONTEND_TESTS_PASSED=true
    else
        print_error "Frontend E2E tests failed"
        FRONTEND_TESTS_PASSED=false
    fi
    
    cd ..
}

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        print_status "Backend server stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        print_status "Frontend server stopped"
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Main execution
main() {
    check_requirements
    start_backend
    start_frontend
    
    # Give servers a moment to fully initialize
    sleep 3
    
    run_backend_tests
    run_frontend_tests
    
    # Summary
    echo ""
    echo "============================================================"
    echo "TEST SUMMARY"
    echo "============================================================"
    
    if [ "$BACKEND_TESTS_PASSED" = true ] && [ "$FRONTEND_TESTS_PASSED" = true ]; then
        print_status "ALL TESTS PASSED! 🎉"
        echo "The case document analysis feature is working correctly."
        exit 0
    else
        print_error "SOME TESTS FAILED!"
        echo "Backend tests: $([ "$BACKEND_TESTS_PASSED" = true ] && echo "PASSED" || echo "FAILED")"
        echo "Frontend tests: $([ "$FRONTEND_TESTS_PASSED" = true ] && echo "PASSED" || echo "FAILED")"
        exit 1
    fi
}

# Run main function
main "$@"