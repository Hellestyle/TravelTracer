from database import Database
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from flask_login import UserMixin
import mysql.connector 



class Errors(Enum):
    USER_OR_PASSWORD_ERROR = "Username or password is wrong"
    USER_DOES_NOT_EXIST = "Username does not exist"
    PASSWORD_ERROR = "Password is wrong"
    EMAIL_ALREADY_EXISTS = "Email Already exists"
    USERNAME_ALREADY_EXISTS = "Username already exists"
    DATABASE_ERROR = "Database error"
    UNKNOWN_ERROR = "Unknown error"


class User(UserMixin):
    def __init__(self, id=None, username=None, email=None, firstName=None, lastName=None, avatar=None, isAdmin=False, passhash=None) -> None:
        self.__id = id
        self.__username = username
        self.__email = email
        self.__firstName = firstName
        self.__lastName = lastName
        self.__avatar = avatar
        self.__isAdmin = isAdmin
        self.__passhash = passhash
        

    def get_email(self, email):
        with Database() as db:
            try:
                result = db.queryOne("SELECT * FROM user WHERE  email=(%s)", (email,))
            except mysql.connector.Error as err:
                    print(err)
            if result:
                return User(*result)
            else:
                return None
    
    def get_user_by_id(self, id):
        with Database() as db:
            try:
                result = db.queryOne("SELECT * FROM user WHERE  id=(%s)", (id,))
            except mysql.connector.Error as err:
                    print(err)
            return result
            
    
    def get_id(self):
        return str(self.__id)    
    
    def check_password(self, password):
        return check_password_hash(self.__passhash, password)
    
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
