# getSecrets Tests

This directory contains comprehensive tests for the getSecrets package.

## Test Structure

### Unit Tests (test_getsecrets_comprehensive.py)

Comprehensive unit tests using mocking to test all functionality without requiring a Vault server:

- **TestGetSecretWithMocking**: Tests for `get_secret()` function
    - Success scenarios from Vault
    - Local config retrieval
    - Error handling
    - Custom repository support

- **TestGetUserPwd**: Tests for `get_user_pwd()` function
    - Local and Vault retrieval
    - Missing fields handling
    - Error scenarios

- **TestListSecret**: Tests for `list_secret()` function
    - Success scenarios
    - Custom repositories
    - Error handling

- **TestUpdSecret**: Tests for `upd_secret()` function
    - Local config updates
    - Vault updates with CAS
    - Error conditions

- **TestCertificateHandling**: Certificate validation logic
    - Public network using certifi
    - Private network using custom certs
    - Insecure mode fallback

- **TestEdgeCases**: Edge cases and error conditions
    - Missing configuration
    - Empty responses
    - Invalid data

### Integration Tests (test_getsecrets.py)

Tests that require actual Vault server or local configuration:

- Real Vault server interactions
- End-to-end secret retrieval and updates
- Local configuration file secrets
- Automatically skips if Vault not available

## Running Tests

### Run All Tests

```bash
# Using pytest (recommended)
pytest tests/

# Using unittest
python -m unittest discover tests/
```

### Run Unit Tests Only

```bash
pytest tests/test_getsecrets_comprehensive.py -v
```

### Run Integration Tests Only

```bash
pytest tests/test_getsecrets.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=getSecrets --cov-report=html --cov-report=term
```

The HTML coverage report will be in `htmlcov/index.html`.

### Run Specific Test Class

```bash
pytest tests/test_getsecrets_comprehensive.py::TestGetSecretWithMocking -v
```

### Run Specific Test Method

```bash
pytest tests/test_getsecrets_comprehensive.py::TestGetSecretWithMocking::test_get_secret_from_vault_success -v
```

## Test Requirements

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

Or install individual packages:

```bash
pip install pytest pytest-cov pytest-mock coverage
```

## Integration Test Setup

Integration tests require either:

### Option 1: Vault Server

- Running Vault server
- Configuration at `~/.config/.vault/vault.yml`:
  ```yaml
  vault:
    token: "your-token"
    vault_addr: "https://vault.example.com:8200"
    certs: "~/certs/bundle.pem"
  ```
- A `test` secret with:
  ```yaml
  username: test
  password: test
  ```

### Option 2: Local Config Only

- Configuration file with embedded secrets:
  ```yaml
  vault:
    token: "dummy"
    vault_addr: "https://vault.example.com:8200"
    certs: "~/certs/bundle.pem"

  test:
    username: test
    password: test
  ```

If neither option is available, integration tests will be automatically skipped.

## Test Coverage

Current test coverage includes:

✅ Secret retrieval from Vault
✅ Secret retrieval from local config
✅ Username/password extraction
✅ Secret listing
✅ Secret updates (local and Vault)
✅ Certificate validation logic
✅ Error handling and edge cases
✅ Custom repository support
✅ HTTP error responses
✅ Missing configuration handling

## Continuous Integration

To run tests in CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: |
    pip install -r requirements-test.txt
    pip install -e .

- name: Run unit tests
  run: pytest tests/test_getsecrets_comprehensive.py -v --cov=getSecrets

- name: Upload coverage
  uses: codecov/codecov-action@v2
```

## Writing New Tests

### Unit Test Template

```python
@patch('getSecrets.requests.get')
@patch('getSecrets._config', {'vault': {...}})
@patch('getSecrets._home', '/home/testuser')
@patch('os.path.exists', return_value=True)
def test_new_feature(self, mock_exists, mock_get):
    """Test description"""
    from getSecrets import get_secret

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': {'data': {...}}}
    mock_get.return_value = mock_response

    result = get_secret('test-id')

    self.assertEqual(result, expected_value)
```

### Integration Test Template

```python
def test_new_integration(self):
    """Integration test description"""
    result = gs.get_secret('test')
    self.assertIsInstance(result, dict)
    # Add assertions
```

## Debugging Tests

### Run with verbose output

```bash
pytest tests/ -vv
```

### Run with print statements visible

```bash
pytest tests/ -s
```

### Run and stop at first failure

```bash
pytest tests/ -x
```

### Run and enter debugger on failure

```bash
pytest tests/ --pdb
```

## Test Markers (for future use)

Tests can be marked with custom markers in pytest.ini:

```python
@pytest.mark.unit
def test_something():
    pass


@pytest.mark.integration
def test_integration():
    pass


@pytest.mark.slow
def test_slow_operation():
    pass
```

Run specific markers:

```bash
pytest -m unit  # Run only unit tests
pytest -m "not slow"  # Run all except slow tests
```

## Contributing

When adding new features:

1. Add unit tests in `test_getsecrets_comprehensive.py`
2. Add integration tests in `test_getsecrets.py` if needed
3. Ensure all tests pass: `pytest tests/`
4. Check coverage: `pytest tests/ --cov=getSecrets`
5. Aim for >80% code coverage

## Test Results

After running tests, check:

- All tests passed ✅
- Code coverage report
- No warnings or errors
- Integration tests ran or were appropriately skipped

## Support

For issues with tests:

1. Ensure all dependencies are installed
2. Check Python version (>=3.6)
3. Verify test configuration in `pytest.ini`
4. Review test output for specific error messages
