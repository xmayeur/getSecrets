import unittest

import getSecrets as gs


class TestGetSecrets(unittest.TestCase):

    def test_listsecret(self):
        secrets = gs.list_secret()
        self.assertTrue('test' in secrets)

    def test_getsecrets(self):
        secret = gs.get_secret('test')
        self.assertTrue('test' in secret)
        self.assertEqual(secret['test'], 'test')

    def test_usr_pwd(self):
        usr, pwd = gs.get_user_pwd('test')
        self.assertEqual(usr, 'test')
        self.assertEqual(pwd, 'test')


if __name__ == '__main__':
    unittest.main()
