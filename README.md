# getSecrets

[![Documentation Status](https://readthedocs.org/projects/getsecrets/badge/?version=latest)](https://getsecrets.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A Python package for securely retrieving secrets from HashiCorp Vault or local configuration files.

## Features

- **Simple API**: Easy-to-use functions for retrieving secrets
- **Flexible Storage**: Works with HashiCorp Vault or local YAML configuration files
- **Multiple Retrieval Methods**: Get complete secrets, username/password pairs, or list available secrets
- **Update Support**: Update existing secrets in Vault
- **Secure by Default**: Automatic certificate validation with intelligent fallback
- **Repository Support**: Work with multiple secret repositories

## Installation

Install from PyPI:

```bash
pip install get-hc-secrets
```

Or install from source:

```bash
git clone https://github.com/yourusername/getSecrets.git
cd getSecrets
pip install -e .
```

## Quick Start

### Configuration

Create a configuration file at `~/.config/.vault/vault.yml`:

```yaml
vault:
  token: "your-vault-token"
  vault_addr: "https://vault.example.com:8200"
  certs: "~/path/to/bundle.pem"

# Optional: Local secrets for development
local-db:
  host: localhost
  port: 5432
  username: dev_user
  password: dev_password
```

### Basic Usage

```python
from getSecrets import get_secret, get_user_pwd, list_secret, upd_secret

# Retrieve a complete secret
database_config = get_secret('my-database-config')
print(database_config)
# {'host': 'db.example.com', 'port': 5432, 'database': 'myapp'}

# Retrieve username and password
username, password = get_user_pwd('postgres-credentials')

# List all secrets in a repository
secrets = list_secret('secret')
print(secrets)
# ['database-config', 'api-keys', 'admin-credentials']

# Update a secret
new_data = {'host': 'new-db.example.com', 'port': 5432}
status = upd_secret('my-database-config', new_data)
```

### Working with Custom Repositories

```python
# Retrieve from a custom repository
api_keys = get_secret('api-credentials', repo='production-secrets')

# Update in custom repository
upd_secret('api-credentials', new_data, repo='production-secrets')
```

## API Reference

### `get_secret(id, repo='secret')`

Retrieves a complete secret as a dictionary.

**Parameters:**

- `id` (str): The ID of the secret to retrieve
- `repo` (str, optional): The repository name (default: 'secret')

**Returns:** `dict` - Key-value pairs from the secret, or empty dict on error

### `get_user_pwd(id, repo='secret')`

Retrieves username and password from a secret.

**Parameters:**

- `id` (str): The ID of the secret to retrieve
- `repo` (str, optional): The repository name (default: 'secret')

**Returns:** `tuple` - (username, password) or (None, None) if not found

### `list_secret(repo='secret')`

Lists all available secret IDs in a repository.

**Parameters:**

- `repo` (str, optional): The repository name (default: 'secret')

**Returns:** `list` - List of secret IDs

### `upd_secret(id, data, repo='secret')`

Updates an existing secret with new data.

**Parameters:**

- `id` (str): The ID of the secret to update
- `data` (dict): The new data to store
- `repo` (str, optional): The repository name (default: 'secret')

**Returns:** `int` - HTTP status code (200 on success)

## Certificate Configuration

For secure communication with Vault, create a `bundle.pem` file containing (in order):

1. Vault certificate
2. Intermediate certificate
3. Root certificate

**Note:**

- For public networks: The package automatically uses system certificates via certifi
- For internal networks (192.168.x.x): Custom certificates from config are used
- If no certificates are found: Works in insecure mode (not recommended for production)

## Configuration File Locations

The package searches for configuration in the following order:

1. `~/.config/.vault/vault.yml`
2. `/etc/vault/vault.yml`

## Documentation

Full documentation is available at: [https://getsecrets.readthedocs.io](https://getsecrets.readthedocs.io)

## Examples

### Database Connection

```python
import psycopg2
from getSecrets import get_secret

db_config = get_secret('postgres-production')

connection = psycopg2.connect(
    host=db_config['host'],
    port=db_config.get('port', 5432),
    database=db_config['database'],
    user=db_config['username'],
    password=db_config['password']
)
```

### API Authentication

```python
import requests
from getSecrets import get_secret

api_config = get_secret('external-api', repo='api-secrets')

headers = {
    'Authorization': f"Bearer {api_config['api_token']}"
}

response = requests.get(api_config['api_url'], headers=headers)
```

## Development

To build the documentation locally:

```bash
cd docs
pip install -r requirements.txt
make html
```

## License

[Your License Here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Version

Current version: 1.5.23