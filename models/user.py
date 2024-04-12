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

    def update(self):

        with Database(dict_cursor=True) as db:

            try:
            
                user_info = db.queryOne("SELECT * FROM user AS u LEFT OUTER JOIN user_system_meta AS usm ON u.id = usm.user_id WHERE u.id = %s", (self.__id,))

                if user_info:

                    self.__username = user_info["username"]
                    self.__email = user_info["email"]
                    self.__firstName = user_info["firstname"]
                    self.__lastName = user_info["lastname"]
                    self.__avatar = user_info["avatar"]
                    self.__isAdmin = user_info["admin"]
                    self.__passhash = user_info["password"]

                    self.__verified = bool(user_info["verified"])
                    self.__open_profile = bool(user_info["open_profile"])
                    self.__show_real_name = bool(user_info["show_real_name"])
                    self.__show_friend_list = bool(user_info["show_friend_list"])
                    self.__current_language = user_info["current_language"]
                    self.__current_city = user_info["current_city"]

                    return True, "Success"
                
                else:
                    return False, Errors.USER_DOES_NOT_EXIST.value
                
            except:
                return False, Errors.DATABASE_ERROR.value
            

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


    def isUsernameAvailible(self, username, exclude_current_user=False):

        with Database() as db:

            if exclude_current_user:
                usernameResult = db.query("SELECT * FROM user Where username = %s AND id != %s", (username, self.__id))
            else:
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
                username_availible = self.isUsernameAvailible(newUsername, exclude_current_user=True)
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


    def add_password_recovery_uuid(self, uuid):

        with Database() as db:

            try:

                old_uuid = db.queryOne("SELECT uuid FROM password_recovery WHERE user_id = %s", (self.__id,))

                if old_uuid:
                    db.queryOne("UPDATE password_recovery SET uuid = %s WHERE user_id = %s", (uuid, self.__id))
                else:
                    db.queryOne("INSERT INTO password_recovery (user_id, uuid) VALUES (%s, %s)", (self.__id, uuid))

                return True, "Success"
            
            except:
                return False, Errors.DATABASE_ERROR.value


    def get_user_by_password_recovery_uuid(self, uuid):

        with Database() as db:

            try:

                result = db.queryOne("SELECT user_id FROM password_recovery WHERE uuid = %s", (uuid,))

                if result:
                    return self.get_user_by_id(result[0])
                else:
                    return None
            
            except:
                return None


    def recover_password(self, password):

        with Database() as db:

            try:

                db.queryOne("UPDATE user SET password = %s WHERE id = %s", (generate_password_hash(password), self.__id))

                return True, "Success"
            
            except:
                return False, Errors.DATABASE_ERROR.value


    def get_user_info(self):
        with Database() as db:
            try:
                user = db.query("SELECT u.id, u.username, u.email, u.firstname, u.lastname, u.avatar, \
                            COUNT(DISTINCT vl.sight_id) AS visited, COUNT(DISTINCT wl.sight_id) AS wishlist \
                            FROM user AS u LEFT OUTER JOIN visited_list AS vl ON vl.user_id = u.id \
                            LEFT OUTER JOIN wishlist AS wl ON wl.user_id = u.id WHERE u.id = %s GROUP BY u.id;", (self.__id,))
            except:
                return False, Errors.DATABASE_ERROR.value
            
            if user:
                user_tuple = user[0]
                user_info = {
                    "id": user_tuple[0],
                    "username": user_tuple[1],
                    "email": user_tuple[2],
                    "first_name": user_tuple[3],
                    "last_name": user_tuple[4],
                    "avatar": user_tuple[5],
                    "visited": user_tuple[6],
                    "wishlist": user_tuple[7]
                }
                return True, user_info
            else:
                return False, Errors.USER_DOES_NOT_EXIST.value


    def get_friend_amount(self):
        with Database() as db:
            try:
                friend = db.query("SELECT f1.follower AS user_id, COUNT(f2.follower) AS friends \
                                FROM friend AS f1 JOIN friend AS f2 ON f1.follower = f2.following AND f1.following = f2.follower \
                                WHERE f1.follower = %s GROUP BY f1.follower;", (self.__id,))
            except:
                return False, Errors.DATABASE_ERROR.value
        
        if friend:
            friend_tuple = friend[0]
            friend_list = {
                "user_id": friend_tuple[0],
                "friends": friend_tuple[1]
            }
            return True, friend_list
        else:
            return True, {"user_id": self.__id, "friends": 0}
    
    def get_friendlist(self):
        with Database() as db:
            try:
                friendlist = db.query("SELECT f1.follower AS user_id, f2.follower AS friend_id, u.username, u.firstname, u.lastname, usm.open_profile, usm.show_real_name, usm.show_friend_list FROM friend AS f1 \
                                    LEFT OUTER JOIN friend AS f2 ON f1.follower = f2.following AND f1.following = f2.follower \
                                    LEFT OUTER JOIN user AS u ON u.id = f2.follower \
                                    LEFT OUTER JOIN user_system_meta AS usm ON usm.user_id = f2.follower \
                                    WHERE f2.follower IS NOT NULL AND f1.follower = %s;", (self.__id,))
            except:
                return False, Errors.DATABASE_ERROR.value

            if friendlist:
                friends = []
                for friend in friendlist:
                    friends.append({
                        "user_id": friend[0],
                        "friend_id": friend[1],
                        "username": friend[2],
                        "first_name": friend[3],
                        "last_name": friend[4],
                        "open_profile": friend[5],
                        "show_real_name": friend[6],
                        "show_friend_list": friend[7]
                    })
                return True, friends
            else:
                return True, []
            
    def is_friend(self, user_id):

        with Database() as db:

            try:

                result = db.queryOne("SELECT * FROM friend WHERE follower = %s AND following = %s", (self.__id, user_id))

                if not result:
                    return False
                
                result = db.queryOne("SELECT * FROM friend WHERE follower = %s AND following = %s", (user_id, self.__id))

                if not result:
                    return False
                
                return True
            
            except:
                return False
            
    def updatePrivacySettings(self,showProfile,showFriendslist,showRealName):
        
        showProfileInt = 1 if showProfile else 0
        showFriendslistInt = 1 if showFriendslist else 0
        showRealNameInt = 1 if showRealName else 0
        
        with Database() as db:
            try:
                db.queryOne("UPDATE `user_system_meta` SET `open_profile` = '%s', `show_real_name` = '%s', `show_friend_list` = '%s' WHERE `user_system_meta`.`user_id` = %s", (showProfileInt,showRealNameInt,showFriendslistInt,self.__id,))
            except:
                return False, Errors.DATABASE_ERROR.value
        self.__open_profile = showProfile
        self.__show_real_name = showRealName
        self.__show_friend_list = showFriendslist
        return True, "Changes to privacy settings made succsessfully"
        

    def get_friend_requests(self):
        with Database() as db:
            try:
                friend_requests = db.query("SELECT f2.follower AS user_id, u.id, u.username, u.firstname, u.lastname, usm.open_profile, usm.show_real_name, usm.show_friend_list \
                                        FROM friend AS f2 \
                                        LEFT OUTER JOIN friend AS f1 ON f1.following = f2.follower AND f1.follower = f2.following \
                                        LEFT OUTER JOIN user AS u ON u.id = f2.follower \
                                        LEFT OUTER JOIN user_system_meta AS usm ON usm.user_id = f2.follower \
                                        WHERE f1.follower IS NULL AND f2.following = %s;", (self.__id,))
            except:
                return False, Errors.DATABASE_ERROR.value
        
            if friend_requests:
                requests = []
                for request in friend_requests:
                    requests.append({
                        "user_id": request[0],
                        "following_id": request[1],
                        "username": request[2],
                        "first_name": request[3],
                        "last_name": request[4],
                        "open_profile": request[5],
                        "show_real_name": request[6],
                        "show_friend_list": request[7]
                    })
                return True, requests
            else:
                return True, []


    def get_usernames_and_user_id(self):
        with Database() as db:
            try:
                usernames = db.query("SELECT id, username FROM user;")
            except:
                return False, Errors.DATABASE_ERROR.value
            
            if usernames:
                users = [{"id": user[0], "username": user[1]} for user in usernames]
                return True, users
            else:
                return False, Errors.UNKNOWN_ERROR.value


    def accept_friend_request(self, sender_id):
        with Database() as db:
            try:
                db.query("INSERT INTO friend (follower, following) VALUES (%s, %s);", (self.__id, sender_id))
                return True, "Friend request accepted!"
            except:
                return False, Errors.DATABASE_ERROR.value


    def decline_friend_request(self, sender_id):
        with Database() as db:
            try:
                db.query("DELETE FROM friend WHERE follower = %s AND following = %s;", (sender_id, self.__id))
                return True, "Friend request declined!"
            except:
                return False, Errors.DATABASE_ERROR.value
            
        
    def send_friend_request(self, receiver_id):
        with Database() as db:
            result = db.queryOne("SELECT * FROM friend WHERE follower = %s AND following = %s;", (self.__id, receiver_id))
            if result:
                return False, "Friend request already sent!"
            else:
                try:
                    db.query("INSERT INTO friend (follower, following) VALUES (%s, %s);", (self.__id, receiver_id))
                    return True, "Friend request sent!"
                except:
                    return False, Errors.DATABASE_ERROR.value

           
    def check_sent_friend_request(self, receiver_id):
        with Database() as db:
            result = db.queryOne("SELECT * FROM friend WHERE follower = %s AND following = %s;", (self.__id, receiver_id))
            if result:
                return True
            else:
                return False


    def show_sent_friend_request(self):
        with Database() as db:
            try:
                sent_friend_requests = db.query("SELECT f1.follower, f1.following, u.id, u.username, u.firstname, u.lastname, usm.show_real_name \
                                            FROM friend AS f1 LEFT JOIN friend AS f2 \
                                            ON f1.follower = f2.following AND f1.following = f2.follower \
                                            LEFT JOIN user AS u ON u.id = f1.following \
                                            LEFT JOIN user_system_meta AS usm ON usm.user_id = f1.following \
                                            WHERE f2.follower IS NULL AND f1.follower = %s;", (self.__id,))
            except:
                return False, Errors.DATABASE_ERROR.value
            
            if sent_friend_requests:
                sent_requests = []
                for request in sent_friend_requests:
                    sent_requests.append({
                        "user_id": request[1],
                        "follower_id": request[2],
                        "username": request[3],
                        "first_name": request[4],
                        "last_name": request[5],
                        "show_real_name": request[6]
                    })
                return True, sent_requests
            else:
                return True, []
    

    def cancel_friend_request(self, receiver_id):
        with Database() as db:
            try:
                db.query("DELETE FROM friend WHERE follower = %s AND following = %s;", (self.__id, receiver_id))
                return True, "Friend request canceled!"
            except:
                return False, Errors.DATABASE_ERROR.value


    def remove_friend(self, friend_id):
        with Database() as db:
            try:
                db.query("DELETE FROM friend WHERE follower = %s AND following = %s;", (self.__id, friend_id))
                db.query("DELETE FROM friend WHERE follower = %s AND following = %s;", (friend_id, self.__id))
                return True, "Friend removed!"
            except:
                return False, Errors.DATABASE_ERROR.value
            
    
    def check_if_user_is_admin(self):
        return self.__isAdmin

    def isVerified(self):
        return self.__verified
    
    def isOpenProfile(self):
        return self.__open_profile
    
    def isPublicFriendslist(self):
        return self.__show_friend_list
    
    def isPublicRealName(self):
        return self.__show_real_name
    
    def getFirstName(self):
        return self.__firstName
    
    def getUsername(self):
        return self.__username
    
    def getLastName(self):
        return self.__lastName
    
    def get_points(self):

        try:

            with Database() as db:

                points = db.queryOne("SELECT SUM(st.points) AS points FROM visited_list AS vl JOIN sight AS s ON vl.sight_id = s.id JOIN sight_has_sight_type AS sst ON s.id = sst.sight_id JOIN sight_type AS st ON st.id = sst.sight_type_id WHERE user_id = %s;", (self.__id,))[0]

                return True, "Success", points if points else 0
            
        except Exception as exception:
            return False, str(exception), None
        
    
    def get_user_wishlist_and_visited_list(self):
        try:
            with Database() as db:
                wishlist = db.query("SELECT s.id FROM sight AS s \
                                JOIN wishlist AS wl \
                                ON wl.sight_id = s.id \
                                WHERE wl.user_id = %s;", (self.__id,))

                visited = db.query("SELECT s.id \
                                FROM sight AS s \
                                JOIN visited_list AS vl \
                                ON vl.sight_id = s.id \
                                WHERE vl.user_id = %s;", (self.__id,))
                
                user_wishlist = [sight[0] for sight in wishlist] if wishlist else []
                user_visited_list = [sight[0] for sight in visited] if visited else []
                return True, "Success", user_wishlist, user_visited_list
            
        except Exception as exception:
            return False, str(exception), [], []


    def __str__(self) -> str:
        string = f"User(id={self.__id}, username={self.__username}, passhash={self.__passhash}, email={self.__email}, isAdmin={self.__isAdmin}, firstName={self.__firstName}, lastName={self.__lastName})"
        return string


if __name__ == "__main__":
    pass
