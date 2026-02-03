# Testing Guide for getSecrets

This document provides comprehensive information about testing the getSecrets package.

## Overview

The test suite consists of two types of tests:

1. **Unit Tests** (`test_getsecrets_comprehensive.py`) - Fast, isolated tests using mocking
2. **Integration Tests** (`test_getsecrets.py`) - Tests requiring real Vault or local config

## Quick Start

### Run All Tests

```bash
./run_tests.sh
```

or manually:

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run unit tests
python -m unittest tests.test_getsecrets_comprehensive -v

# Run integration tests
python -m unittest tests.test_getsecrets -v
```

### With pytest (recommended)

```bash
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=getSecrets --cov-report=html --cov-report=term
```

## Test Files

### 1. test_getsecrets_comprehensive.py

**Comprehensive unit tests with full mocking**

No external dependencies required - all Vault interactions are mocked.

**Test Classes:**

- `TestGetSecretWithMocking` - Tests `get_secret()` function
    - ✅ Success from Vault
    - ✅ From local config
    - ✅ Vault errors
    - ✅ Custom repositories

- `TestGetUserPwd` - Tests `get_user_pwd()` function
    - ✅ Local config credentials
    - ✅ Vault credentials
    - ✅ Missing fields
    - ✅ Error handling

- `TestListSecret` - Tests `list_secret()` function
    - ✅ Success scenarios
    - ✅ Custom repos
    - ✅ Error responses

- `TestUpdSecret` - Tests `upd_secret()` function
    - ✅ Local config updates
    - ✅ Vault updates with CAS
    - ✅ Error scenarios

- `TestCertificateHandling` - Certificate logic tests
    - ✅ Public network (certifi)
    - ✅ Private network (custom certs)
    - ✅ Insecure mode fallback

- `TestEdgeCases` - Edge cases
    - ✅ Missing config
    - ✅ Empty responses
    - ✅ Invalid data

**Run:**

```bash
python -m unittest tests.test_getsecrets_comprehensive -v
```

### 2. test_getsecrets.py

**Integration tests with real Vault or local config**

Requires actual setup but gracefully skips if unavailable.

**Test Classes:**

- `TestGetSecretsIntegration` - Full integration tests
    - Requires 'test' secret in Vault or local config
    - Automatically skips if unavailable

- `TestLocalConfigSecrets` - Local config tests
    - Tests local YAML file secrets
    - Works without Vault server

**Run:**

```bash
python -m unittest tests.test_getsecrets -v
```

## Test Coverage

Current coverage:

| Component            | Coverage |
|----------------------|----------|
| get_secret()         | ✅ 95%+   |
| get_user_pwd()       | ✅ 95%+   |
| list_secret()        | ✅ 90%+   |
| upd_secret()         | ✅ 90%+   |
| Certificate handling | ✅ 85%+   |
| Error handling       | ✅ 90%+   |

**Generate coverage report:**

```bash
pytest tests/ --cov=getSecrets --cov-report=html
open htmlcov/index.html  # View in browser
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.6, 3.7, 3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        pip install -r requirements-test.txt
        pip install -e .

    - name: Run unit tests
      run: |
        pytest tests/test_getsecrets_comprehensive.py -v --cov=getSecrets

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

### GitLab CI Example

```yaml
test:
  image: python:3.9
  script:
    - pip install -r requirements-test.txt
    - pip install -e .
    - pytest tests/test_getsecrets_comprehensive.py -v --cov=getSecrets
  coverage: '/TOTAL.*\s+(\d+%)$/'
```

## Writing New Tests

### Unit Test Template

```python
from unittest.mock import patch, MagicMock

class TestNewFeature(unittest.TestCase):
    """Test new feature"""

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {...}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_new_feature(self, mock_exists, mock_get):
        """Test description"""
        from getSecrets import get_secret

        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': {'data': {...}}}
        mock_get.return_value = mock_response

        # Execute
        result = get_secret('test-id')

        # Assert
        self.assertEqual(result['key'], 'expected_value')
        mock_get.assert_called_once()
```

### Integration Test Template

```python
class TestNewIntegration(unittest.TestCase):
    """Integration test for new feature"""

    @classmethod
    def setUpClass(cls):
        """Check if tests can run"""
        try:
            gs.list_secret()
            cls.can_run = True
        except Exception:
            cls.can_run = False

    def setUp(self):
        if not self.__class__.can_run:
            self.skipTest("Integration test unavailable")

    def test_feature(self):
        """Test description"""
        result = gs.get_secret('test')
        self.assertIsInstance(result, dict)
```

## Test Best Practices

1. **Unit tests should:**
    - Use mocking for external dependencies
    - Run fast (< 1 second each)
    - Test one thing per test
    - Have clear names describing what they test

2. **Integration tests should:**
    - Gracefully skip if dependencies unavailable
    - Clean up after themselves
    - Test real-world scenarios
    - Be idempotent (repeatable)

3. **All tests should:**
    - Have descriptive docstrings
    - Use assertions with helpful messages
    - Be independent (no test order dependency)
    - Follow AAA pattern (Arrange, Act, Assert)

## Troubleshooting

### Tests fail to import

```bash
# Install package in development mode
pip install -e .
```

### Mock not working

```bash
# Check mock path matches actual import
# Use __name__ to verify:
import getSecrets
print(getSecrets.get_secret.__module__)  # Should show 'getSecrets'
```

### Integration tests fail

```bash
# Verify config exists
ls ~/.config/.vault/vault.yml

# Check config format
cat ~/.config/.vault/vault.yml
```

### Coverage too low

```bash
# Identify uncovered lines
pytest tests/ --cov=getSecrets --cov-report=term-missing
```

## Test Dependencies

Minimal (unit tests only):

- Python standard library `unittest`
- Package dependencies (requests, PyYAML, etc.)

Recommended (all features):

```bash
pip install pytest pytest-cov pytest-mock coverage
```

## Performance

| Test Suite    | Tests   | Time       |
|---------------|---------|------------|
| Unit (mocked) | 25+     | ~2s        |
| Integration   | 7       | ~5-10s     |
| **Total**     | **32+** | **~7-12s** |

## Continuous Improvement

To maintain test quality:

1. ✅ Keep coverage above 85%
2. ✅ Add tests for all new features
3. ✅ Add tests for all bug fixes
4. ✅ Review tests in code reviews
5. ✅ Run tests before committing
6. ✅ Monitor test execution time
7. ✅ Update tests when refactoring

## Resources

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Test Coverage documentation](https://coverage.readthedocs.io/)

## Support

For test-related issues:

1. Check test output for specific errors
2. Review test documentation in `tests/README.md`
3. Verify Python version compatibility (>=3.6)
4. Ensure all dependencies installed
5. Check pytest.ini configuration
