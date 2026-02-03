#!/bin/bash
# Test runner script for getSecrets

echo "================================"
echo "getSecrets Test Suite"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements-test.txt 2>/dev/null
pip install -q -e . 2>/dev/null

echo ""
echo "================================"
echo "Running Unit Tests (with mocking)"
echo "================================"
echo ""

# Try pytest first
if command -v pytest &> /dev/null; then
    pytest tests/test_getsecrets_comprehensive.py -v --tb=short
else
    # Fall back to unittest
    python -m unittest tests.test_getsecrets_comprehensive -v
fi

echo ""
echo "================================"
echo "Running Integration Tests"
echo "================================"
echo ""

if command -v pytest &> /dev/null; then
    pytest tests/test_getsecrets.py -v --tb=short
else
    python -m unittest tests.test_getsecrets -v
fi

echo ""
echo "================================"
echo "Test Summary"
echo "================================"
echo ""
echo "Unit tests: Completed (no external dependencies required)"
echo "Integration tests: Check output above"
echo ""
echo "For coverage report, run:"
echo "  pytest tests/ --cov=getSecrets --cov-report=html"
echo ""
