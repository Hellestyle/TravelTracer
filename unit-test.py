import unittest
from user import User

class UserClass(unittest.TestCase):
    
    def test_login(self):
        user = User("name","passhash")
        username = "name"
        password = "123"
        
        self.assertEqual(user.login(username,password), False)
        

    def test_print(self):
        user = User("JohnDoe12",email="Johndoe12@gmail.com", isAdmin=True,firstName="John", lastName="Doe")
        self.assertEqual(User.__str__,True)

if __name__ == '__main__':
    unittest.main()