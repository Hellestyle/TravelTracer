import unittest
from user import User

class UserClass(unittest.TestCase):
    
    def test_login(self):
        user = User()
        username = "MP"
        password = "123456789"
        
        self.assertEqual(user.login(username,password), True)
        

    

if __name__ == '__main__':
    unittest.main()