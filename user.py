from database import Database
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum


class Errors(Enum):
    USER_OR_PASSWORD_ERROR = "Username or password is wrong"
    USER_DOES_NOT_EXIST = "Username does not exist"
    PASSWORD_ERROR = "Password is wrong"
    EMAIL_ALREADY_EXISTS = "Email Already exists"
    USERNAME_ALREADY_EXISTS = "Username already exists"
    DATABASE_ERROR = "Database error"
    UNKNOWN_ERROR = "Unknown error"


class User():
    def __init__(self, id=None, username=None, passhash=None, email=None, isAdmin=False, firstName=None , lastName=None, avatar=None, is_authenticated=None, is_active = None, is_anonymous=None) -> None:
      
        self.__id = id
        self.__username = username
        self.__passhash = passhash
        self.__email = email
        self.__isAdmin = isAdmin
        self.__firstName = firstName
        self.__lastName = lastName
        self.__avatar = avatar
        #Flask Login Manager stuff
        self.__is_authenticated = is_authenticated
        self.__is_active = is_active
        self.__is_anonymous = is_anonymous
        
        
    def login(self, email, password):
        with Database() as db:
            try:
                databaseResult = db.queryOne("SELECT * FROM user Where email = %s ", (email,))

                if databaseResult:
                    check_password_result = check_password_hash(pwhash=databaseResult[-1], password=password)

                    if check_password_result:
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
                        return False, Errors.USER_OR_PASSWORD_ERROR.value
                else:
                    return False, Errors.USER_OR_PASSWORD_ERROR.value
            except:
                return False, Errors.DATABASE_ERROR.value

        
    def isUsernameAvailible(self, username):
        with Database() as db:
            usernameResult = db.query("SELECT * FROM user Where username = %s ", (username,))
            if usernameResult == None:
                return True
            else:
                return False
        

    def isEmailAvailible(self, email):
        email = email.lower()
        with Database() as db:
            emailResult = db.query("SELECT * FROM user Where email = %s ", (email,))
            if emailResult == None:
                return True
            else:
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


    def deleteUser(self):
        email = self.__email
        with Database() as db:
            try:
                db.queryOne('DELETE FROM user WHERE email = %s ', (email,))
                return True, "Sucess"
            except:
                return False, Errors.DATABASE_ERROR.value
            
    def changePassword(self,oldPass,newPass,newPassCheck):
        with Database() as db:
            try:
                result = db.queryOne("SELECT email,password FROM user Where email = %s ", (self.__email,))
                if check_password_hash(result[1],oldPass) and newPass == newPassCheck:
                    newPassHash = generate_password_hash(newPass)
                    try:
                        db.queryOne('UPDATE user SET password = %s WHERE `user`.`email` = %s', (newPassHash,self.__email,))
                    except:
                        return False, Errors.DATABASE_ERROR.value
                    return True, "Success"
            except:
                return False, Errors.DATABASE_ERROR.value
            
    def get_id(self, email):
        with Database() as db:
            try:
                databaseResult = db.queryOne("SELECT * FROM user Where email = %s ", (email,))
                self.__id = databaseResult[0]
                self.__passhash = databaseResult[-1]
                self.__username = databaseResult[1]
                self.__email = databaseResult[2]
                self.__firstName = databaseResult[3]
                self.__lastName = databaseResult[4]
                self.__avatar = databaseResult[5]
                self.__isAdmin = databaseResult[6]
                return self
            except:
                return None
            
    def changeUsername(self,password,verifyPassword,newUsername):
        with Database() as db:
            try:
                result = db.queryOne("SELECT email,password FROM user Where email = %s ", (self.__email,))
                if check_password_hash(result[1],password) and password == verifyPassword:
                    
                    try:
                        db.queryOne('UPDATE user SET username = %s WHERE `user`.`email` = %s', (newUsername,self.__email,))
                    except:
                        return False, Errors.DATABASE_ERROR.value
                    return True, "Success"
            except:
                return False, Errors.DATABASE_ERROR.value
                


    def __str__(self) -> str:
        string = f"User(username={self.__username}, passhash={self.__passhash}, email={self.__email}, isAdmin={self.__isAdmin}, firstName={self.__firstName}, lastName={self.__lastName})"
        return string
    

if __name__ == "__main__":
     pass
