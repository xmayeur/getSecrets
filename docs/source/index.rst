.. getSecrets documentation master file

Welcome to getSecrets Documentation
====================================

**getSecrets** is a Python package that provides a simple and secure way to retrieve secrets from HashiCorp Vault or local configuration files.

The package supports multiple secret retrieval methods and can seamlessly work with both remote Vault servers and local YAML configuration files for development and testing.

Features
--------

* **Simple API**: Easy-to-use functions for retrieving secrets
* **Flexible Storage**: Works with HashiCorp Vault or local configuration files
* **Multiple Retrieval Methods**: Get complete secrets, user/password pairs, or list available secrets
* **Update Support**: Update existing secrets in the Vault
* **Secure by Default**: Uses certificate validation with fallback options
* **Repository Support**: Can work with multiple secret repositories

Quick Start
-----------

Install the package:

.. code-block:: bash

   pip install get-hc-secrets

Basic usage:

.. code-block:: python

   from getSecrets import get_secret, get_user_pwd

   # Retrieve a complete secret
   data = get_secret('my-secret-id')

   # Retrieve username and password
   username, password = get_user_pwd('database-creds')

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
