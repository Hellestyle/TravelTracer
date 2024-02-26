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
                databaseResult = db.query("SELECT * FROM user Where username = %s ", username)[0]
            except:
                return False
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

    def checkIfUserExist(self, username, email):
        with Database() as db:
            try:
                existResultat = db.query("SELECT * FROM user Where username = %s ", (username,))[0]
                existResultat2 = db.query("SELECT * FROM user Where email = %s ", (email,))[0]
            except:
                return False
        if (existResultat[1] == username) or (existResultat2[2] == email):
            return True
        else:
            return False
    
    def registrer(self, firstName, lastName, email, username, passhash):
        # Add database check for not a registrered user
        # Add to database
        # Return success/True
        passhash = generate_password_hash(passhash)
        if self.checkIfUserExist(username, email) == False:
            with Database() as db:
                try:
                    db.query('INSERT INTO user (username, email, firstname, lastname, password, admin) VALUES (%s, %s, %s, %s, %s, %s)',(username, email, firstName, lastName, passhash,0,))
                    return True
                except:
                    return False
        else:
            return False

    def __str__(self) -> str:
        string = f"User(username={self.__username}, passhash={self.__passhash}, email={self.__email}, isAdmin={self.__isAdmin}, firstName={self.__firstName}, lastName={self.__lastName})"
        return string
    

if __name__ == "__main__":
    pass
