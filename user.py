from database import Database
from werkzeug.security import generate_password_hash, check_password_hash

class User():
    def __init__(self, username=None, passhash=None, email=None, isAdmin = False, firstName=None , lastName = None) -> None:
        self.__usernmae = username
        self.__passhash = passhash
        self.__email = email
        self.__isAdmin = isAdmin
        self.__firstName = firstName
        self.__lastName = lastName
        
        
    def login(self, username, password):
        # Check username and hash
        with Database() as db:
            try:
                databaseResult = db.query("SELECT * FROM CHANGEME/USERNAME Where CHANGEME/USERNAMEFIELD = %s ", username)
            except:
                return False
            if check_password_hash(pwhash = databaseResult[0]["CHANGE ME"], password = password):
                self.__passhash = databaseResult[0]["CHANGEME"]
                self.__usernmae = username
                return True
            return False

    
    def registrer(self):
        # Add database check for not a registrered user
        # Add to database
        # Return success/True
        pass     

    c   