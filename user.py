from database import Database
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum


class Errors(Enum):
    LOGIN_ERROR = "Username or password is wrong"
    EMAIL_ALREADY_EXISTS = "Email Already exists"
    USERNAME_ALREADY_EXISTS = "Username already exists"
    DATABASE_ERROR = "Database error"
    UNKNOWN_ERROR = "Unknown error"


class User():
    def __init__(self, id=None, username=None, passhash=None, email=None, isAdmin=False, firstName=None , lastName=None, avatar=None) -> None:
      
        self.__id = id
        self.__username = username
        self.__passhash = passhash
        self.__email = email
        self.__isAdmin = isAdmin
        self.__firstName = firstName
        self.__lastName = lastName
        self.__avatar = avatar
        
        
    def login(self, email, password):

        with Database() as db:
            try:
                databaseResult = db.queryOne("SELECT * FROM user Where email = %s ", (email,))
                if databaseResult and check_password_hash(pwhash=databaseResult[-1], password=password):

                    self.__id = databaseResult[0]
                    self.__passhash = databaseResult[-1]
                    self.__username = databaseResult[1]
                    self.__email = databaseResult[2]
                    self.__firstName = databaseResult[3]
                    self.__lastName = databaseResult[4]
                    self.__avatar = databaseResult[5]
                    self.__isAdmin = databaseResult[6]

                    return True, "No errors"
                else:
                    return False, Errors.LOGIN_ERROR.value
            except:
                return False, Errors.DATABASE_ERROR.value


        
    def isUsernameAvailible(self, username):
        with Database() as db:
            try:
                usernameResult = db.query("SELECT * FROM user Where username = %s ", (username,))
                if not usernameResult:
                    return True
            except:
                return False
        

    def isEmailAvailible(self, email):

        email = email.lower()

        with Database() as db:
            try:
                emailResult = db.query("SELECT * FROM user Where email = %s ", (email,))
                if not emailResult:
                    return True
            except:
                return False


    

    def registrer(self, firstName, lastName, email, username, password):

        email = email.lower()
        passhash = generate_password_hash(password)

        if not self.isEmailAvailible(email):
            return False, Errors.EMAIL_ALREADY_EXISTS.value
        if not self.isUsernameAvailible(username):
            return False, Errors.USERNAME_ALREADY_EXISTS.value

        
        with Database() as db:
            try:
                db.query('INSERT INTO user (username, email, firstname, lastname, password, admin) VALUES (%s, %s, %s, %s, %s, %s)', (username, email, firstName, lastName, passhash, 0,))
                return True, "No errors"
            except:
                return False, Errors.DATABASE_ERROR.value




    def __str__(self) -> str:
        string = f"User(username={self.__username}, passhash={self.__passhash}, email={self.__email}, isAdmin={self.__isAdmin}, firstName={self.__firstName}, lastName={self.__lastName})"
        return string
    

if __name__ == "__main__":
     pass
