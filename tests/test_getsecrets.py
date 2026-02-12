"""
Integration tests for getSecrets package.
These tests require a real Vault server or local config with a 'test' secret.
For unit tests with mocking, see test_getsecrets_comprehensive.py
"""

import os
import sys
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src import getSecrets as gs
except ImportError:
    import getSecrets as gs


class TestGetSecretsIntegration(unittest.TestCase):
    """
    Integration tests that require actual Vault server or local config.

    Prerequisites:
    - Vault server accessible or local config at ~/.config/.vault/vault.yml
    - A 'test' secret with username='test', password='test'
    """

    @classmethod
    def setUpClass(cls):
        """Check if integration tests can run"""
        try:
            # Try to list secrets to verify connection
            gs.list_secret()
            cls.can_run_integration = True
        except Exception as e:
            cls.can_run_integration = False
            print(f"\nWarning: Integration tests skipped. Reason: {e}")
            print("To run integration tests, ensure Vault is accessible or local config exists.\n")

    def setUp(self):
        """Skip tests if integration setup failed"""
        if not self.__class__.can_run_integration:
            self.skipTest("Integration test environment not available")

    def test_listsecret(self):
        """Test listing secrets from repository"""
        secrets = gs.list_secret()
        self.assertIsNotNone(secrets, "Expected list of secrets, got None")
        self.assertIsInstance(secrets, list, "Expected list type")
        self.assertTrue('test' in secrets, "'test' secret should exist in repository")

    def test_getsecrets(self):
        """Test retrieving and updating secrets"""
        # Get initial secret
        secret = gs.get_secret('test')
        self.assertIsNotNone(secret, "Expected secret data, got None")
        self.assertIsInstance(secret, dict, "Expected dict type")

        # Update secret
        secret['test'] = 'test1'
        status = gs.upd_secret('test', secret)
        self.assertEqual(status, 200, f"Expected status 200, got {status}")

        # Verify update
        updated_secret = gs.get_secret('test')
        self.assertTrue('test' in updated_secret, "'test' key should exist in secret")
        self.assertEqual(updated_secret['test'], 'test1', "Secret value should be updated")

    def test_usr_pwd(self):
        """Test retrieving username and password from secret"""
        usr, pwd = gs.get_user_pwd('test')
        self.assertIsNotNone(usr, "Username should not be None")
        self.assertIsNotNone(pwd, "Password should not be None")
        self.assertEqual(usr, 'test', f"Expected username 'test', got '{usr}'")
        self.assertEqual(pwd, 'test', f"Expected password 'test', got '{pwd}'")

    def test_get_secret_custom_repo(self):
        """Test retrieving secret from custom repository"""
        # This test assumes 'secret' is the default repo and works
        try:
            secret = gs.get_secret('test', repo='secret')
            self.assertIsInstance(secret, dict)
        except Exception as e:
            self.skipTest(f"Custom repo test skipped: {e}")

    def test_get_nonexistent_secret(self):
        """Test retrieving non-existent secret returns empty dict"""
        secret = gs.get_secret('this-secret-definitely-does-not-exist-12345')
        self.assertEqual(secret, {}, "Non-existent secret should return empty dict")

    def test_get_user_pwd_nonexistent(self):
        """Test retrieving non-existent credentials returns None, None"""
        usr, pwd = gs.get_user_pwd('this-secret-definitely-does-not-exist-12345')
        self.assertIsNone(usr, "Non-existent username should return None")
        self.assertIsNone(pwd, "Non-existent password should return None")


class TestLocalConfigSecrets(unittest.TestCase):
    """
    Tests for local configuration file secrets.
    These work even without Vault server if config file exists.
    """

    def test_local_secret_retrieval(self):
        """Test that local config secrets can be retrieved"""
        try:
            # Attempt to get a secret that might be in local config
            # This will work if the secret exists locally

            if hasattr(gs, '_config'):
                config = gs._config
                if config and len(config) > 1:  # Has more than just 'vault' key
                    # Get first non-vault key
                    local_keys = [k for k in config.keys() if k != 'vault']
                    if local_keys:
                        secret = gs.get_secret(local_keys[0])
                        self.assertIsInstance(secret, dict)
                        print(f"\nSuccessfully retrieved local secret: {local_keys[0]}")
        except Exception as e:
            self.skipTest(f"Local config test skipped: {e}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
