import unittest
from user import User

class UserClass(unittest.TestCase):
    
    def test_login(self):
        user = User("name","passhash")
        username = "name"
        password = "123"
        
        self.assertEqual(user.login(username,password), False)
        



if __name__ == '__main__':
    unittest.main()