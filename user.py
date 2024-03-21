from database import Database
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from flask_login import UserMixin
import mysql.connector
from uuid import uuid4


class Errors(Enum):
    USER_OR_PASSWORD_ERROR = "Username or password is wrong"
    USER_DOES_NOT_EXIST = "Username does not exist"
    PASSWORD_ERROR = "Password is wrong"
    PASSWORDS_MATCH_ERROR = "Passwords do not match"
    EMAIL_ALREADY_EXISTS = "Email Already exists"
    USERNAME_ALREADY_EXISTS = "Username already exists"
    DATABASE_ERROR = "Database error"
    UNKNOWN_ERROR = "Unknown error"


class User(UserMixin):
    def __init__(
            self, id=None, username=None, email=None, firstName=None, lastName=None, avatar=None, isAdmin=False, passhash=None,
            verified=False, open_profile=True, show_real_name=False, show_friend_list=True, current_language=None, current_city=None
        ) -> None:

        self.__id = id
        self.__username = username
        self.__email = email
        self.__firstName = firstName
        self.__lastName = lastName
        self.__avatar = avatar
        self.__isAdmin = isAdmin
        self.__passhash = passhash

        self.__verified = bool(verified)
        self.__open_profile = bool(open_profile)
        self.__show_real_name = bool(show_real_name)
        self.__show_friend_list = bool(show_friend_list)
        self.__current_language = current_language
        self.__current_city = current_city


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


    def get_user_by_email(self, email):
        with Database() as db:
            try:
                result = db.queryOne("SELECT u.*, usm.verified, usm.open_profile, usm.show_real_name, usm.show_friend_list, usm.current_language, usm.current_city FROM user AS u LEFT OUTER JOIN user_system_meta AS usm ON u.id = usm.user_id WHERE u.email=(%s)", (email,))
                if result:
                    return User(*result)
                else:
                    return None
            except mysql.connector.Error as err:
                print(err)


    def get_user_by_id(self, id):
        with Database() as db:
            try:
                result = db.queryOne("SELECT u.*, usm.verified, usm.open_profile, usm.show_real_name, usm.show_friend_list, usm.current_language, usm.current_city FROM user AS u LEFT OUTER JOIN user_system_meta AS usm ON u.id = usm.user_id WHERE u.id=(%s)", (id,))
                if result:
                    return User(*result)
                else:
                    return None
            except mysql.connector.Error as err:
                print(err)


    def get_id(self):
        return str(self.__id)    


    def get_email(self):
        return self.__email


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

                db.commit()

                user_id = db.queryOne('SELECT id FROM user WHERE email = %s', (email,))[0]

                db.query('INSERT INTO user_system_meta (user_id) VALUES (%s)', (user_id,))

                db.query('INSERT INTO verification (user_id, uuid) VALUES (%s, %s)', (user_id, str(uuid4())))

                db.commit()

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


    def changePassword(self, oldPass, newPass, newPassCheck):
        with Database() as db:
            try:
                result = db.queryOne("SELECT email, password FROM user Where email = %s ", (self.__email,))
            except:
                return False, Errors.DATABASE_ERROR
            
            if check_password_hash(result[1], oldPass):
                if newPass == newPassCheck:
                    newPassHash = generate_password_hash(newPass)
                    try:
                        db.queryOne('UPDATE user SET password = %s WHERE `user`.`email` = %s', (newPassHash, self.__email,))
                        return True, "Success"
                    except:
                        return False, Errors.DATABASE_ERROR.value
                else:
                    return False, Errors.PASSWORDS_MATCH_ERROR.value
            else:
                return False, Errors.PASSWORD_ERROR.value


    def changeNames(self, password, newUsername,newFirstName, newLastName):
        with Database() as db:
            try:
                result = db.queryOne("SELECT email, password FROM user Where email = %s ", (self.__email,))
            except:
                return False, Errors.DATABASE_ERROR.value
            if newUsername == "":
                newUsername = self.getUsername()
            if newFirstName == "":
                newFirstName = self.getFirstName()
            if newLastName == "":
                newLastName = self.getLastName()
            if check_password_hash(result[1], password):
                username_availible = self.isUsernameAvailible(newUsername)
                if username_availible:
                    try:
                        db.queryOne('UPDATE user SET username = %s , firstname = %s , lastname = %s WHERE `user`.`email` = %s', (newUsername, newFirstName, newLastName, self.__email,))
                        return True, "Success"
                    except:
                        return False, Errors.DATABASE_ERROR.value
                else:
                    return False, Errors.USERNAME_ALREADY_EXISTS.value
            else:
                return False, Errors.PASSWORD_ERROR.value

    def get_verification_uuid(self):
        with Database() as db:
            try:
                result = db.queryOne("SELECT uuid FROM verification WHERE user_id = %s", (self.__id,))
                return result[0]
            except:
                return False, Errors.DATABASE_ERROR.value
            
    def verify(self, uuid):

        with Database() as db:
            try:
                result = db.queryOne("SELECT user_id FROM verification WHERE uuid = %s", (uuid,))
                if result:
                    db.queryOne("UPDATE user_system_meta SET verified = 1 WHERE user_id = %s", (result[0],))
                    db.queryOne("DELETE FROM verification WHERE uuid = %s", (uuid,))
                    return True, "Success", self.get_user_by_id(result[0])
                else:
                    return False, "Invalid verification link", None
            except:
                return False, Errors.DATABASE_ERROR.value, None
            
    def update_uuid(self):
        with Database() as db:
            try:
                db.queryOne("UPDATE verification SET uuid = %s WHERE user_id = %s", (str(uuid4()), self.__id))
                return True, "Success"
            except:
                return False, Errors.DATABASE_ERROR.value

    def isVerified(self):
        return self.__verified
    
    def getFirstName(self):
        return self.__firstName
    
    def getUsername(self):
        return self.__username
    
    def getLastName(self):
        return self.__lastName

    def __str__(self) -> str:
        string = f"User(id={self.__id}, username={self.__username}, passhash={self.__passhash}, email={self.__email}, isAdmin={self.__isAdmin}, firstName={self.__firstName}, lastName={self.__lastName}"
        return string



if __name__ == "__main__":
    pass
