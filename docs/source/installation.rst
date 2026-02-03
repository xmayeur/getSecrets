Installation
============

Requirements
------------

* Python 3.6 or higher
* pip package manager

Dependencies
~~~~~~~~~~~~

The package requires the following Python packages:

* ``requests`` - For HTTP communication with Vault
* ``urllib3`` - For advanced URL handling
* ``PyYAML`` - For configuration file parsing
* ``certifi`` - For SSL certificate verification

These dependencies will be automatically installed when you install getSecrets.

Install from PyPI
-----------------

The easiest way to install getSecrets is using pip:

.. code-block:: bash

   pip install get-hc-secrets

Install from Source
-------------------

You can also install the package from source:

.. code-block:: bash

   git clone https://github.com/xmayeur/getSecrets.git
   cd getSecrets
   pip install -e .

Configuration
-------------

Vault Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~

Before using getSecrets, you need to create a configuration file at ``~/.config/.vault/vault.yml`` with the following structure:

.. code-block:: yaml

   vault:
     token: "<your-vault-token>"
     vault_addr: "https://vault.example.com:8200"
     certs: "~/path/to/bundle.pem"

   # Optional: Local secrets (for development/testing)
   my-local-secret:
     item1: value1
     item2: value2
     username: myuser
     password: mypassword

Alternative Configuration Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the user home configuration is not available, getSecrets will look for the configuration at ``/etc/vault/vault.yml``.

Certificate Setup
~~~~~~~~~~~~~~~~~

For secure communication with Vault, you need a certificate bundle (``bundle.pem``). This file should contain, in order:

1. Vault certificate
2. Intermediate certificate
3. Root certificate

.. note::
   If you're connecting to a Vault server on a public network (non-192.168.x.x), the package will automatically use the system's trusted certificates from certifi.

.. warning::
   If no certificate file is found, the package will work in insecure mode (without certificate verification). This is not recommended for production use.

Verifying Installation
----------------------

You can verify the installation by running:

.. code-block:: python

   from getSecrets import get_secret
   print("getSecrets installed successfully!")

Next Steps
----------

Once installed and configured, check out the :doc:`examples` page to see how to use the package.
