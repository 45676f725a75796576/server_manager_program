import unittest
from src import users

class TestUserAuthorization(unittest.TestCase):
    def test_sign_in(self):
        _users = users.Users()
        _users.add_user('user1', '123456')
        self.assertEqual(_users.get_user('user1'), { "username": 'user1' })

    def test_hash(self):
        _users = users.Users()
        _users.add_user('user1', '123456')
        self.assertNotEqual(_users.show_password('user1'), { "password": '123456' })
    
    def test_authorization(self):
        _users = users.Users()
        _users.add_user('user1', '123456')
        self.assertTrue(_users.authorize('user1', '123456'))

if __name__ == '__main__':
    unittest.main()