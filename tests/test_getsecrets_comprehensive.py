"""
Comprehensive unit tests for getSecrets package.
Uses mocking to avoid requiring actual Vault server access.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import yaml


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

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('socket.gethostbyname', return_value='192.168.1.10')
    @patch('os.path.exists', return_value=True)
    def test_get_secret_from_vault_success(self, mock_exists, mock_gethostbyname, mock_get):
        """Test successful secret retrieval from Vault"""
        from getSecrets import get_secret

        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.vault_response_success
        mock_get.return_value = mock_response

        result = get_secret('test-secret')

        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['password'], 'testpass')
        self.assertEqual(result['host'], 'db.example.com')
        mock_get.assert_called_once()

    @patch('getSecrets._config', {'local-secret': {'key1': 'value1', 'key2': 'value2'}})
    def test_get_secret_from_local_config(self):
        """Test secret retrieval from local config file"""
        from getSecrets import get_secret

        result = get_secret('local-secret')

        self.assertEqual(result['key1'], 'value1')
        self.assertEqual(result['key2'], 'value2')

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('socket.gethostbyname', return_value='192.168.1.10')
    @patch('os.path.exists', return_value=True)
    def test_get_secret_vault_error(self, mock_exists, mock_gethostbyname, mock_get):
        """Test secret retrieval when Vault returns error"""
        from getSecrets import get_secret

        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        result = get_secret('test-secret')

        self.assertEqual(result, {})

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('socket.gethostbyname', return_value='192.168.1.10')
    @patch('os.path.exists', return_value=True)
    def test_get_secret_custom_repo(self, mock_exists, mock_gethostbyname, mock_get):
        """Test secret retrieval from custom repository"""
        from getSecrets import get_secret

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.vault_response_success
        mock_get.return_value = mock_response

        result = get_secret('test-secret', repo='custom-repo')

        # Verify correct URL was called
        call_args = mock_get.call_args
        self.assertIn('custom-repo', call_args[0][0])


class TestGetUserPwd(unittest.TestCase):
    """Test get_user_pwd function"""

    @patch('getSecrets._config', {
        'local-creds': {
            'username': 'localuser',
            'password': 'localpass'
        }
    })
    def test_get_user_pwd_from_local_config(self):
        """Test username/password retrieval from local config"""
        from getSecrets import get_user_pwd

        username, password = get_user_pwd('local-creds')

        self.assertEqual(username, 'localuser')
        self.assertEqual(password, 'localpass')

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_get_user_pwd_from_vault(self, mock_exists, mock_get):
        """Test username/password retrieval from Vault"""
        from getSecrets import get_user_pwd

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

        username, password = get_user_pwd('vault-creds')

        self.assertEqual(username, 'vaultuser')
        self.assertEqual(password, 'vaultpass')

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_get_user_pwd_missing_fields(self, mock_exists, mock_get):
        """Test when secret doesn't have username/password fields"""
        from getSecrets import get_user_pwd

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

        username, password = get_user_pwd('incomplete-secret')

        self.assertIsNone(username)
        self.assertIsNone(password)

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_get_user_pwd_vault_error(self, mock_exists, mock_get):
        """Test username/password retrieval when Vault returns error"""
        from getSecrets import get_user_pwd

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        username, password = get_user_pwd('nonexistent')

        self.assertIsNone(username)
        self.assertIsNone(password)


class TestListSecret(unittest.TestCase):
    """Test list_secret function"""

    @patch('getSecrets.requests.request')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_list_secret_success(self, mock_exists, mock_request):
        """Test successful secret listing"""
        from getSecrets import list_secret

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'keys': ['secret1', 'secret2', 'secret3']
            }
        }
        mock_request.return_value = mock_response

        result = list_secret()

        self.assertEqual(len(result), 3)
        self.assertIn('secret1', result)
        self.assertIn('secret2', result)
        self.assertIn('secret3', result)

    @patch('getSecrets.requests.request')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_list_secret_custom_repo(self, mock_exists, mock_request):
        """Test secret listing from custom repository"""
        from getSecrets import list_secret

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'keys': ['custom-secret1', 'custom-secret2']
            }
        }
        mock_request.return_value = mock_response

        result = list_secret(repo='custom-repo')

        # Verify correct URL was called
        call_args = mock_request.call_args
        self.assertIn('custom-repo', call_args[0][1])

    @patch('getSecrets.requests.request')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_list_secret_error(self, mock_exists, mock_request):
        """Test secret listing when Vault returns error"""
        from getSecrets import list_secret

        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_request.return_value = mock_response

        result = list_secret()

        self.assertEqual(result, (None, None))


class TestUpdSecret(unittest.TestCase):
    """Test upd_secret function"""

    def test_upd_secret_local_config(self):
        """Test updating local config secret"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            test_config = {
                'vault': {
                    'vault_addr': 'https://vault.example.com:8200',
                    'token': 'test-token',
                    'certs': '~/certs/bundle.pem'
                },
                'local-secret': {
                    'key1': 'value1'
                }
            }
            yaml.safe_dump(test_config, f)
            temp_file = f.name

        try:
            with patch('getSecrets._config', test_config):
                with patch('getSecrets._home', os.path.dirname(temp_file)):
                    with patch('getSecrets._config_file', os.path.basename(temp_file)):
                        from getSecrets import upd_secret

                        new_data = {'key1': 'updated_value', 'key2': 'new_value'}
                        status = upd_secret('local-secret', new_data)

                        self.assertEqual(status, 200)
        finally:
            os.unlink(temp_file)

    @patch('getSecrets.requests.request')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_upd_secret_vault_success(self, mock_exists, mock_request):
        """Test successful secret update in Vault"""
        from getSecrets import upd_secret

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

        new_data = {'key': 'updated_value'}
        status = upd_secret('vault-secret', new_data)

        self.assertEqual(status, 200)
        self.assertEqual(mock_request.call_count, 2)

    @patch('getSecrets.requests.request')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('os.path.exists', return_value=True)
    def test_upd_secret_vault_get_error(self, mock_exists, mock_request):
        """Test update when GET fails"""
        from getSecrets import upd_secret

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response

        status = upd_secret('nonexistent', {'key': 'value'})

        self.assertEqual(status, (None, None))


class TestCertificateHandling(unittest.TestCase):
    """Test certificate validation logic"""

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('socket.gethostbyname', return_value='8.8.8.8')
    @patch('getSecrets.where', return_value='/etc/ssl/certs/ca-bundle.crt')
    @patch('os.path.exists', return_value=True)
    def test_public_network_uses_certifi(self, mock_exists, mock_where, mock_gethostbyname, mock_get):
        """Test that public networks use certifi certificates"""
        from getSecrets import get_secret

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'data': {'key': 'value'}
            }
        }
        mock_get.return_value = mock_response

        get_secret('test-secret')

        # Verify certifi was called for public IP
        mock_where.assert_called_once()

    @patch('getSecrets.requests.get')
    @patch('getSecrets.urllib3.disable_warnings')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('socket.gethostbyname', return_value='192.168.1.10')
    @patch('os.path.exists', return_value=False)
    def test_missing_cert_works_insecure(self, mock_exists, mock_gethostbyname, mock_disable_warnings, mock_get):
        """Test that missing certificates trigger insecure mode"""
        from getSecrets import get_secret

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'data': {'key': 'value'}
            }
        }
        mock_get.return_value = mock_response

        get_secret('test-secret')

        # Verify warnings were disabled
        mock_disable_warnings.assert_called()

        # Verify request was made with verify=False
        call_args = mock_get.call_args
        self.assertEqual(call_args[1]['verify'], False)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    @patch('getSecrets._config', {})
    def test_get_secret_missing_config_key(self):
        """Test behavior when secret key doesn't exist in config"""
        from getSecrets import get_secret

        # Should attempt Vault lookup, which will fail without vault config
        with self.assertRaises(KeyError):
            get_secret('nonexistent-secret')

    @patch('getSecrets.requests.get')
    @patch('getSecrets._config', {'vault': {'vault_addr': 'https://vault.example.com:8200', 'token': 'test-token',
                                            'certs': '~/certs/bundle.pem'}})
    @patch('getSecrets._home', '/home/testuser')
    @patch('socket.gethostbyname', return_value='192.168.1.10')
    @patch('os.path.exists', return_value=True)
    def test_empty_secret_response(self, mock_exists, mock_gethostbyname, mock_get):
        """Test handling of empty secret data"""
        from getSecrets import get_secret

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'data': {}
            }
        }
        mock_get.return_value = mock_response

        result = get_secret('empty-secret')

        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()
