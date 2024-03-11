class SightType:

    def __init__(self, db):
        self.__db = db

    def getAllSightTypes(self, language_id=None):

        if language_id is None:
            language_id = self.__db.query("SELECT id FROM language WHERE `default` = 1;")[0]['id']

        query = "SELECT st.id AS id, stm.name AS name, stm.description AS description FROM sight_type AS st LEFT OUTER JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id WHERE stm.language_id = %s;"

        return self.__db.query(query, [language_id])
