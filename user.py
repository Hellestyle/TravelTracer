from database import Database
from werkzeug.security import generate_password_hash, check_password_hash

class User():
    def __init__(self, id = None, username=None, passhash=None, email=None, isAdmin = False, firstName=None , lastName = None, avatar = None) -> None:
        self.__id = id
        self.__username = username
        self.__passhash = passhash
        self.__email = email
        self.__isAdmin = isAdmin
        self.__firstName = firstName
        self.__lastName = lastName
        self.__avatar = avatar
        
        
    def login(self, username, password):
        # Check username and hash
        with Database() as db:
            try:
                databaseResult = db.queryOne("SELECT * FROM user Where username = %s ", (username,))
            except:
                return False
            if databaseResult != []:
                if check_password_hash(pwhash = databaseResult[-1], password = password):
                    self.__id = databaseResult[0]
                    self.__passhash = databaseResult[-1]
                    self.__username = databaseResult[1]
                    self.__email = databaseResult[2]
                    self.__firstName = databaseResult[3]
                    self.__lastName = databaseResult[4]
                    self.__avatar = databaseResult[5]
                    self.__isAdmin = databaseResult[6]
                    return True
            return False

    
    def registrer(self):
        # Add database check for not a registrered user
        # Add to database
        # Return success/True
        pass        
    

    def __str__(self) -> str:
        string = f"User(username={self.__username}, passhash={self.__passhash}, email={self.__email}, isAdmin={self.__isAdmin}, firstName={self.__firstName}, lastName={self.__lastName})"
        return string
    

if __name__ == "__main__":
    pass