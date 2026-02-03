API Reference
=============

This page contains the complete API reference for the getSecrets package.

Main Module
-----------

.. automodule:: getSecrets
   :members:
   :undoc-members:
   :show-inheritance:

Functions
---------

get_secret()
~~~~~~~~~~~~

.. autofunction:: getSecrets.get_secret

**Description:**

Retrieves a secret from HashiCorp Vault or local configuration file.

**Parameters:**

* **id** (*str*) - The ID of the secret to retrieve
* **repo** (*str*) - The name of the secrets repository (default: 'secret')

**Returns:**

* *dict* - A dictionary containing key-value pairs from the secret, or an empty dict if retrieval fails

**Behavior:**

1. First checks if the secret exists in the local configuration file
2. If not found locally, queries the Vault server
3. Automatically handles certificate validation
4. Falls back to insecure mode if certificates are not available

**Example:**

.. code-block:: python

   secret = get_secret('database-config')
   # Returns: {'host': 'db.example.com', 'port': 5432}

get_user_pwd()
~~~~~~~~~~~~~~

.. autofunction:: getSecrets.get_user_pwd

**Description:**

Retrieves username and password from a secret.

**Parameters:**

* **id** (*str*) - The ID of the secret to retrieve
* **repo** (*str*) - The name of the secrets repository (default: 'secret')

**Returns:**

* *tuple* - A tuple of (username, password) or (None, None) if retrieval fails or fields don't exist

**Behavior:**

1. Retrieves the secret using the same logic as get_secret()
2. Extracts 'username' and 'password' fields if they exist
3. Returns (None, None) if either field is missing

**Example:**

.. code-block:: python

   username, password = get_user_pwd('postgres-creds')
   # Returns: ('dbuser', 'securepassword123')

list_secret()
~~~~~~~~~~~~~

.. autofunction:: getSecrets.list_secret

**Description:**

Lists all available secret IDs in a repository.

**Parameters:**

* **repo** (*str*) - The name of the secrets repository (default: 'secret')

**Returns:**

* *list* - A list of secret IDs (keys) available in the repository, or (None, None) on error

**Behavior:**

1. Queries the Vault metadata endpoint for the specified repository
2. Returns the list of available secret keys
3. Does not retrieve actual secret values

**Example:**

.. code-block:: python

   secrets = list_secret()
   # Returns: ['database-config', 'api-keys', 'admin-creds']

upd_secret()
~~~~~~~~~~~~

.. autofunction:: getSecrets.upd_secret

**Description:**

Updates an existing secret with new data.

**Parameters:**

* **id** (*str*) - The ID of the secret to update
* **data** (*dict*) - The new data to store in the secret
* **repo** (*str*) - The name of the secrets repository (default: 'secret')

**Returns:**

* *int* - HTTP status code (200 on success), or (None, None) on error

**Behavior:**

1. If the secret exists in local config, updates the local YAML file
2. Otherwise, retrieves current version from Vault
3. Uses Check-And-Set (CAS) to safely update the secret
4. Prevents concurrent modification conflicts

**Example:**

.. code-block:: python

   new_data = {'host': 'newdb.example.com', 'port': 5432}
   status = upd_secret('database-config', new_data)
   # Returns: 200

Configuration
-------------

Configuration File Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The package looks for configuration in the following locations (in order):

1. ``~/.config/.vault/vault.yml``
2. ``/etc/vault/vault.yml``

Configuration File Format
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   vault:
     token: "your-vault-token"
     vault_addr: "https://vault.example.com:8200"
     certs: "~/path/to/bundle.pem"

   # Optional local secrets
   secret-id:
     key1: value1
     key2: value2

Certificate Validation
~~~~~~~~~~~~~~~~~~~~~~

The package uses the following logic for certificate validation:

1. If connecting to internal network (192.168.x.x): Uses custom certificate bundle
2. If connecting to public network: Uses system certificates (via certifi)
3. If no certificates found: Works in insecure mode (with warning)

**Custom Certificate Bundle:**

The bundle.pem file should contain certificates in this order:

1. Vault server certificate
2. Intermediate CA certificate
3. Root CA certificate

Logging
-------

The package uses Python's standard logging module with INFO level by default.

**Log Format:**

.. code-block:: text

   MM/DD/YYYY HH:MM:SS AM/PM message

**Example Logs:**

.. code-block:: text

   02/03/2026 10:30:45 AM No vault bundle.pem found at /path/to/cert - working insecure !!
   02/03/2026 10:30:46 AM Vault api error <Response [403]>

Exceptions and Error Handling
------------------------------

The package handles errors gracefully:

* **Configuration Not Found**: Logs error and exits with code 1
* **Certificate Not Found**: Logs warning and continues in insecure mode
* **HTTP Errors**: Logs error and returns empty dict or None values
* **Missing Fields**: Returns None values for get_user_pwd()

**System Exit Conditions:**

The package will call ``sys.exit(1)`` only if:

* No configuration file found in any expected location

All other errors are handled gracefully with logging and error return values.

Type Hints
----------

While the current implementation uses basic type hints in docstrings, the functions accept and return:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Function
     - Parameters
     - Returns
   * - get_secret()
     - id: str, repo: str
     - dict
   * - get_user_pwd()
     - id: str, repo: str
     - tuple[str | None, str | None]
   * - list_secret()
     - repo: str
     - list[str] | tuple[None, None]
   * - upd_secret()
     - id: str, data: dict, repo: str
     - int | tuple[None, None]
