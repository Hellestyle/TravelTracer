import unittest
from unittest.mock import patch, MagicMock
from user import User, Errors
from database import Database


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


    # Test if the new username is already taken
    def test_changeUsernameFAIL(self):
        test_user = User()
        test_user.login("test1234@uit.no", "12345678")
        result, message = test_user.changeUsername("12345678", "12345678", "Isak")
        expected = (False, Errors.USERNAME_ALREADY_EXISTS.value)
        return self.assertEqual((result, message), expected)


    # Test if the new passwords do not match
    def test_changePasswordFAIL(self):
        test_user = User()
        test_user.login("test1234@uit.no", "12345678")
        result, message = test_user.changePassword("12345678", "newpassword", "differentpassword")
        excepted = (False, Errors.PASSWORDS_MATCH_ERROR.value)
        return self.assertEqual((result, message), excepted)
    

    #Need to change password every time this test is run
    #def test_changePassword(self):
        #test_user = User()
        #test_user.login("test1234@uit.no", "newhashed")
        #result, message = test_user.changePassword("newhashed", "12345678", "12345678")
        #self.assertTrue(result)


    #Need to change username every time this test is run
    #def test_changeUsername(self):
        #test_user = User()
        #test_user.login("test1234@uit.no", "12345678")
        #result, message = test_user.changeUsername("12345678", "12345678", "test_username")
        #self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
