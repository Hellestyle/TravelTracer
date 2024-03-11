class SightName:

    def __init__(self, db):
        self.__db = db

    def getAllSightNames(self):
        query = "SELECT s.id AS id, sm.name AS name FROM sight_meta AS sm LEFT OUTER JOIN sight AS s ON sm.sight_id = s.id;"
        return self.__db.query(query)
