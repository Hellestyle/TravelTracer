import unittest
from user import User

class UserClass(unittest.TestCase):


    def test_login(self):
        user = User()
        result, error = user.login("Mathiaspettersen@hotmail.no","123456789")
        self.assertTrue(result)
    
    def test_deleteUser(self):
        user = User(email="testuser@uit.no")
        result, error = user.deleteUser()
        self.assertTrue(result)

        
    def test_registreringAndDeletion(self):
        user = User()
        email = "testuser@uit.no"
        if not user.isEmailAvailible(email):
            self.test_deleteUser()
        success, error = user.registrer("Test", "Testersen", email, "tester123", "123456789")
        self.assertTrue(success, "Registration should succeed")
        if not success:
            print("Registration failed: ", error)
        else:
            print("Registration succeed!")
            

    def test_registreringFAIL(self):
        user = User()
        success, error = user.registrer("Mathias", "Pettersen", "Mathiaspettersen@hotmail.no", "MP", "123456789")
        self.assertFalse(success, "Registration should fail")
        if not success:
            print("Registration failed: ", error)
            
        else:
            print("Registration succeed!")
            

    def test_loginSTOR(self):
        user = User()
        result, error = user.login("MATHIASPETTERSEN@hotMAIL.No","123456789")
        self.assertTrue(result)
    
    def test_emailAvailible(self):
        user = User()
        result = user.isEmailAvailible("donalduck1@andeby.no")
        self.assertTrue(result)
    

    def test_emailNOTAvailible(self):
        user = User()
        result = user.isEmailAvailible("Mathiaspettersen@hotmail.no")
        self.assertFalse(result)




if __name__ == '__main__':
    unittest.main()