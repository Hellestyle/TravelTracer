import unittest
from user import User

class UserClass(unittest.TestCase):

    
        

    def test_registrering(self):
        user = User()
        self.assertEqual(user.registrer("Mathias", "Pettersen", "Mathiaspettersen@hotmail.no", "MP", "123456789"), True)

    def test_login(self):
        user = User()
        username = "Mathiaspettersen@hotmail.no"
        password = "123456789"
        
        self.assertEqual(user.login(username,password), True)
        

 

    def test_registrering(self):
        user = User()
        success, error = user.registrer("Mathias", "Pettersen", "Mathiaspettersen@hotmail.no", "MP", "123456789")
        if not success:
            print("Registration failed: ", error.value)
        else:
            print("Registration succeed!")
            self.assertTrue(success, "Registration should succeed")

    def test_usernameNOTAvailible(self):
        user = User()
        self.assertEqual(user.isUsernameAvailible("MP"),False)
    
    def test_usernameAvailible(self):
        user = User()
        self.assertEqual(user.isUsernameAvailible("DonaldDuck1"),True)
    
    def test_emailAvailible(self):
        user = User()
        self.assertEqual(user.isEmailAvailible("donalduck1@andeby.no"),True)
    
    def test_emailNOTAvailible(self):
        user = User()
        self.assertEqual(user.isEmailAvailible("Mathiaspettersen@hotmail.no"),False)
    

    def test_login(self):
        user = User()
        username = "MP"
        password = "123456789"
        
        self.assertEqual(user.login(username,password), True)

if __name__ == '__main__':
    unittest.main()


    