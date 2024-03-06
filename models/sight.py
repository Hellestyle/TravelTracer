class Sight:

    def __init__(self, db):
        self.__db = db

    def getAllSights(self):
        return self.__db.query("SELECT * FROM sight;")
