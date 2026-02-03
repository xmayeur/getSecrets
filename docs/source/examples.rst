Usage Examples
==============

This page provides practical examples for using the getSecrets package.

Basic Secret Retrieval
-----------------------

Retrieve a Complete Secret
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most common use case is to retrieve a complete secret as a dictionary:

.. code-block:: python

   from getSecrets import get_secret

   # Retrieve secret from default 'secret' repository
   secret_data = get_secret('my-database-config')

   print(secret_data)
   # Output: {'host': 'db.example.com', 'port': 5432, 'database': 'myapp'}

   # Access individual values
   db_host = secret_data.get('host')
   db_port = secret_data.get('port')

Retrieve from Custom Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your secrets are stored in a different repository:

.. code-block:: python

   from getSecrets import get_secret

   # Retrieve from a custom repository
   api_keys = get_secret('api-keys', repo='production-secrets')

   aws_key = api_keys.get('aws_access_key')
   aws_secret = api_keys.get('aws_secret_key')

Username and Password Retrieval
--------------------------------

Simple Credential Retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For secrets that contain username and password fields:

.. code-block:: python

   from getSecrets import get_user_pwd

   # Retrieve database credentials
   username, password = get_user_pwd('postgres-db')

   # Use in connection string
   connection_string = f"postgresql://{username}:{password}@localhost/mydb"

Custom Repository Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import get_user_pwd

   # Retrieve from custom repository
   user, pwd = get_user_pwd('admin-account', repo='admin-secrets')

   if user and pwd:
       # Credentials found
       authenticate(user, pwd)
   else:
       print("No credentials found or missing username/password fields")

Listing Available Secrets
--------------------------

List Secrets in Default Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import list_secret

   # List all secrets in default 'secret' repository
   secrets = list_secret()

   print("Available secrets:")
   for secret_id in secrets:
       print(f"  - {secret_id}")

List Secrets in Custom Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import list_secret

   # List secrets in a specific repository
   prod_secrets = list_secret(repo='production-secrets')

   for secret_id in prod_secrets:
       print(f"Production secret: {secret_id}")

Updating Secrets
----------------

Update Existing Secret
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import upd_secret

   # Prepare new data
   new_data = {
       'host': 'new-db.example.com',
       'port': 5432,
       'database': 'myapp',
       'ssl': True
   }

   # Update the secret
   status = upd_secret('my-database-config', new_data)

   if status == 200:
       print("Secret updated successfully")
   else:
       print(f"Failed to update secret: {status}")

Update in Custom Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import upd_secret

   # Update secret in custom repository
   new_credentials = {
       'username': 'new_admin',
       'password': 'new_secure_password'
   }

   status = upd_secret('admin-account', new_credentials, repo='admin-secrets')

Local Configuration Secrets
----------------------------

Reading from Local Config
~~~~~~~~~~~~~~~~~~~~~~~~~~

If a secret ID exists in your ``vault.yml`` configuration file, it will be read from there instead of the Vault server:

**vault.yml:**

.. code-block:: yaml

   vault:
     token: "token123"
     vault_addr: "https://vault.example.com:8200"
     certs: "~/certs/bundle.pem"

   local-db:
     host: localhost
     port: 5432
     username: dev_user
     password: dev_password

**Python code:**

.. code-block:: python

   from getSecrets import get_secret, get_user_pwd

   # This will read from local config, not Vault
   db_config = get_secret('local-db')

   # This also works with get_user_pwd
   user, pwd = get_user_pwd('local-db')

Updating Local Config Secrets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import upd_secret

   # Update local config secret
   new_config = {
       'host': 'localhost',
       'port': 3306,
       'username': 'updated_user',
       'password': 'updated_password'
   }

   # This will update the vault.yml file
   status = upd_secret('local-db', new_config)

Error Handling
--------------

Handling Missing Secrets
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import get_secret

   secret = get_secret('non-existent-secret')

   if not secret:
       print("Secret not found or error occurred")
   else:
       # Process secret
       pass

Handling Missing Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from getSecrets import get_user_pwd

   username, password = get_user_pwd('my-secret')

   if username is None or password is None:
       print("Could not retrieve credentials")
       # Handle error or use defaults
   else:
       # Use credentials
       connect(username, password)

Complete Application Example
-----------------------------

Database Connection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import psycopg2
   from getSecrets import get_secret

   def connect_to_database():
       """Connect to PostgreSQL database using secrets from Vault."""

       # Retrieve database configuration
       db_config = get_secret('postgres-production')

       if not db_config:
           raise ValueError("Could not retrieve database configuration")

       # Connect to database
       connection = psycopg2.connect(
           host=db_config.get('host'),
           port=db_config.get('port', 5432),
           database=db_config.get('database'),
           user=db_config.get('username'),
           password=db_config.get('password')
       )

       return connection

   # Use the connection
   try:
       conn = connect_to_database()
       cursor = conn.cursor()
       cursor.execute("SELECT version();")
       print(f"Connected to: {cursor.fetchone()}")
       cursor.close()
       conn.close()
   except Exception as e:
       print(f"Database connection failed: {e}")

API Client Example
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import requests
   from getSecrets import get_secret

   def call_external_api():
       """Call external API using credentials from Vault."""

       # Retrieve API credentials
       api_config = get_secret('external-api-keys', repo='api-secrets')

       if not api_config:
           raise ValueError("Could not retrieve API configuration")

       # Make API call
       headers = {
           'Authorization': f"Bearer {api_config.get('api_token')}",
           'Content-Type': 'application/json'
       }

       response = requests.get(
           api_config.get('api_url'),
           headers=headers
       )

       return response.json()

   # Use the API
   try:
       data = call_external_api()
       print(f"API Response: {data}")
   except Exception as e:
       print(f"API call failed: {e}")

Best Practices
--------------

1. **Error Handling**: Always check if secrets are successfully retrieved before using them
2. **Repository Organization**: Use different repositories for different environments (dev, staging, production)
3. **Local Development**: Use local config file entries for development to avoid hitting the Vault server
4. **Certificate Management**: Always use proper certificates in production environments
5. **Token Security**: Keep your Vault tokens secure and rotate them regularly
6. **Minimal Permissions**: Use Vault tokens with minimal required permissions for each application
