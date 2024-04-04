class Sight_location:

    def __init__(self, db):
        self.__db = db

    def get_all_sight_locations(self):
        query = "SELECT name FROM city_meta WHERE city_id = 1;"
        return self.__db.query(query)