# Quick Test Guide

## Prerequisites

Before running tests, install the package dependencies:

```bash
# Option 1: Install in development mode (recommended)
pip install -e .

# Option 2: Install dependencies manually
pip install requests urllib3 PyYAML certifi

# Option 3: Install test dependencies (includes everything)
pip install -r requirements-test.txt
```

## Running Tests

### 1. Simple Verification Test

```bash
# Verify test framework works
python tests/test_simple.py
```

Expected output:

```
test_can_import_mock ... ok
test_can_import_unittest ... ok

Ran 2 tests in 0.XXXs

OK
```

### 2. Comprehensive Unit Tests (Mocked)

```bash
# Run all unit tests with mocking
python -m unittest tests.test_getsecrets_comprehensive -v
```

These tests don't require a Vault server - everything is mocked.

### 3. Integration Tests

```bash
# Run integration tests (requires Vault or local config)
python -m unittest tests.test_getsecrets -v
```

These tests will automatically skip if Vault is not available.

### 4. Run All Tests

```bash
# Run everything
python -m unittest discover tests/ -v
```

## Quick Setup Script

```bash
#!/bin/bash
# Setup and run tests

# Install package in development mode
pip install -e .

# Install test dependencies
pip install PyYAML

# Run unit tests
echo "Running unit tests..."
python -m unittest tests.test_getsecrets_comprehensive -v

# Run integration tests
echo "Running integration tests..."
python -m unittest tests.test_getsecrets -v
```

## Troubleshooting

### "No module named 'requests'"

```bash
pip install requests urllib3 PyYAML certifi
```

### "No module named 'getSecrets'"

```bash
# Install package in development mode
pip install -e .
```

### "No module named 'yaml'"

```bash
pip install PyYAML
```

### Tests import error

```bash
# Make sure you're in the project root directory
cd /Users/xavier/PycharmProjects/getSecrets

# Run tests from project root
python -m unittest tests.test_getsecrets_comprehensive -v
```

## Test Coverage Summary

| Test File                        | Type               | Requires Vault | Test Count |
|----------------------------------|--------------------|----------------|------------|
| test_simple.py                   | Setup verification | No             | 2          |
| test_getsecrets_comprehensive.py | Unit (mocked)      | No             | 10+        |
| test_getsecrets.py               | Integration        | Optional       | 7          |

## Example: Complete Setup and Run

```bash
# 1. Navigate to project directory
cd /Users/xavier/PycharmProjects/getSecrets

# 2. Install dependencies
pip install -e .
pip install PyYAML

# 3. Run simple test
python tests/test_simple.py

# 4. Run unit tests
python -m unittest tests.test_getsecrets_comprehensive -v

# 5. Run integration tests (will skip if no Vault)
python -m unittest tests.test_getsecrets -v
```

## Success Indicators

✅ test_simple.py passes → Test framework is working
✅ test_getsecrets_comprehensive.py passes → Unit tests with mocking work
✅ test_getsecrets.py passes OR skips gracefully → Integration tests configured correctly

## Next Steps

Once tests pass:

1. Review test coverage: `pytest tests/ --cov=getSecrets`
2. Add new tests for new features
3. Run tests before committing code
4. Set up CI/CD with these tests
