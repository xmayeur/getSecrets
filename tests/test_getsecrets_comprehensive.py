"""
Comprehensive unit tests for getSecrets package.
Uses mocking to avoid requiring actual Vault server access.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src import getSecrets
except ImportError:
    try:
        import getSecrets
    except ImportError:
        print("ERROR: Cannot import getSecrets module")
        sys.exit(1)

try:
    import yaml
except ImportError:
    print("Warning: PyYAML not installed. Installing it is recommended.")
    yaml = None


class TestGetSecretWithMocking(unittest.TestCase):
    """Test get_secret function with various scenarios"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token-123',
                'certs': '~/certs/bundle.pem'
            },
            'local-secret': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }

        self.vault_response_success = {
            'data': {
                'data': {
                    'username': 'testuser',
                    'password': 'testpass',
                    'host': 'db.example.com'
                },
                'metadata': {
                    'version': 1
                }
            }
        }

    def test_get_secret_from_local_config(self):
        """Test secret retrieval from local config file"""
        # Temporarily patch the _config
        with patch.object(getSecrets, '_config', {'local-secret': {'key1': 'value1', 'key2': 'value2'}}):
            result = getSecrets.get_secret('local-secret')

            self.assertEqual(result['key1'], 'value1')
            self.assertEqual(result['key2'], 'value2')

    @patch('src.getSecrets.requests.get')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_get_secret_from_vault_success(self, mock_gethostbyname, mock_exists, mock_get):
        """Test successful secret retrieval from Vault"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.vault_response_success
        mock_get.return_value = mock_response

        # Temporarily patch config
        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                result = getSecrets.get_secret('test-secret')

                self.assertEqual(result['username'], 'testuser')
                self.assertEqual(result['password'], 'testpass')
                self.assertEqual(result['host'], 'db.example.com')

    @patch('src.getSecrets.requests.get')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_get_secret_vault_error(self, mock_gethostbyname, mock_exists, mock_get):
        """Test secret retrieval when Vault returns error"""
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                result = getSecrets.get_secret('test-secret')
                self.assertEqual(result, {})


class TestGetUserPwd(unittest.TestCase):
    """Test get_user_pwd function"""

    def test_get_user_pwd_from_local_config(self):
        """Test username/password retrieval from local config"""
        test_config = {
            'local-creds': {
                'username': 'localuser',
                'password': 'localpass'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            username, password = getSecrets.get_user_pwd('local-creds')

            self.assertEqual(username, 'localuser')
            self.assertEqual(password, 'localpass')

    @patch('src.getSecrets.requests.get')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_get_user_pwd_from_vault(self, mock_gethostbyname, mock_exists, mock_get):
        """Test username/password retrieval from Vault"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'data': {
                    'username': 'vaultuser',
                    'password': 'vaultpass'
                }
            }
        }
        mock_get.return_value = mock_response

        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                username, password = getSecrets.get_user_pwd('vault-creds')

                self.assertEqual(username, 'vaultuser')
                self.assertEqual(password, 'vaultpass')

    @patch('src.getSecrets.requests.get')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_get_user_pwd_missing_fields(self, mock_gethostbyname, mock_exists, mock_get):
        """Test when secret doesn't have username/password fields"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'data': {
                    'key1': 'value1',
                    'key2': 'value2'
                }
            }
        }
        mock_get.return_value = mock_response

        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                username, password = getSecrets.get_user_pwd('incomplete-secret')

                self.assertIsNone(username)
                self.assertIsNone(password)


class TestListSecret(unittest.TestCase):
    """Test list_secret function"""

    @patch('src.getSecrets.requests.request')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_list_secret_success(self, mock_gethostbyname, mock_exists, mock_request):
        """Test successful secret listing"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'keys': ['secret1', 'secret2', 'secret3']
            }
        }
        mock_request.return_value = mock_response

        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                result = getSecrets.list_secret()

                self.assertEqual(len(result), 3)
                self.assertIn('secret1', result)
                self.assertIn('secret2', result)
                self.assertIn('secret3', result)

    @patch('src.getSecrets.requests.request')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_list_secret_error(self, mock_gethostbyname, mock_exists, mock_request):
        """Test secret listing when Vault returns error"""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_request.return_value = mock_response

        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                result = getSecrets.list_secret()
                self.assertEqual(result, (None, None))


class TestUpdSecret(unittest.TestCase):
    """Test upd_secret function"""

    def test_upd_secret_local_config(self):
        """Test updating local config secret"""
        if yaml is None:
            self.skipTest("PyYAML not installed")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            temp_file = f.name
            test_config = {
                'vault': {
                    'vault_addr': 'https://vault.example.com:8200',
                    'token': 'test-token',
                    'certs': '~/certs/bundle.pem'
                },
                'local-secret': {
                    'key1': 'value1'
                },
                'config_file': os.path.basename(temp_file)
            }
            yaml.safe_dump(test_config, f)


        try:
            with patch.object(getSecrets, '_config', test_config):
                with patch.object(getSecrets, '_home', os.path.dirname(temp_file)):
                    new_data = {'key1': 'updated_value', 'key2': 'new_value'}
                    status = getSecrets.upd_secret('local-secret', new_data)

                    self.assertEqual(status, 200)
        finally:
            os.unlink(temp_file)

    @patch('src.getSecrets.requests.request')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_upd_secret_vault_success(self, mock_gethostbyname, mock_exists, mock_request):
        """Test successful secret update in Vault"""
        # Mock GET response (to get version)
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'data': {
                'data': {'key': 'value'},
                'metadata': {'version': 5}
            }
        }

        # Mock POST response (update)
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200

        mock_request.side_effect = [mock_get_response, mock_post_response]

        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                new_data = {'key': 'updated_value'}
                status = getSecrets.upd_secret('vault-secret', new_data)

                self.assertEqual(status, 200)
                self.assertEqual(mock_request.call_count, 2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    @patch('src.getSecrets.requests.get')
    @patch('src.getSecrets.os.path.exists', return_value=True)
    @patch('src.getSecrets.socket.gethostbyname', return_value='192.168.1.10')
    def test_empty_secret_response(self, mock_gethostbyname, mock_exists, mock_get):
        """Test handling of empty secret data"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'data': {}
            }
        }
        mock_get.return_value = mock_response

        test_config = {
            'vault': {
                'vault_addr': 'https://vault.example.com:8200',
                'token': 'test-token',
                'certs': '~/certs/bundle.pem'
            }
        }

        with patch.object(getSecrets, '_config', test_config):
            with patch.object(getSecrets, '_home', '/home/testuser'):
                result = getSecrets.get_secret('empty-secret')
                self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
