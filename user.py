from datatbase import Database

class User():
    def __init__(self, username=None, passhash=None, email=None, isAdmin = False) -> None:
        self.__usernmae = username
        self.__passhash = passhash
        self.__email = email
        self.__isAdmin = isAdmin
        
    def login(self):
        # Check username and hash
        # return true
        pass
    
    def registrer(self):
        # Add database check for not a registrered user
        # Add to database
        # Return success/True
        pass        