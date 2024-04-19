class SightType:

    def __init__(self, db):
        self.__db = db

    def getAllSightTypes(self, language_id=None):

        if language_id is None:
            language_id = self.__db.query("SELECT id FROM language WHERE `default` = 1;")[0]['id']

        query = "SELECT st.id AS id, stm.name AS name, stm.description AS description FROM sight_type AS st LEFT OUTER JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id WHERE stm.language_id = %s;"

        return self.__db.query(query, [language_id])
    
    
    def get_sight_types(self, language_id=None):
        try:
            if language_id is None:
                language_id = self.__db.query("SELECT id FROM language WHERE `default` = 1;")[0]['id']

            sight_types = self.__db.query("SELECT st.id AS id, stm.name AS name, stm.description AS description, st.points as points FROM sight_type AS st LEFT OUTER JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id WHERE stm.language_id = %s;", (language_id,))

            return True, "success", sight_types
            
        except Exception as exception:
            return False, str(exception), None

    def get_sight_type_data(self, id):
            try:
                result = self.__db.queryOne("SELECT s.id, s.points,  sm.name, sm.description FROM sight_type s JOIN sight_type_meta sm ON s.id = sm.sight_type_id WHERE s.id = %s AND sm.language_id = 1",(id,))
            
            except Exception as e:
                print(e)
            
            return result

    def add_sight_type(self, name, desc, points):
        try:
            self.__db.query("INSERT INTO sight_type (points) VALUES (%s)", (points,))
            id = self.__db.query("SELECT LAST_INSERT_ID();")[0]['LAST_INSERT_ID()']
            self.__db.query("INSERT INTO sight_type_meta (name, description, sight_type_id, language_id) VALUES (%s, %s, %s, 1)", (name, desc, id))

            return True

        except Exception as e:
            print(e)
            return False


    def update(self,id,name,desc, points):
        try:
            self.__db.query("UPDATE `sight_type_meta` SET `name` = %s , `description` = %s WHERE `sight_type_meta`.`sight_type_id` = %s AND `sight_type_meta`.`language_id` = 1 ",(name,desc, id,))
            self.__db.query("UPDATE sight_type SET points = %s WHERE id = %s", (points, id,))

            return True
        except Exception as e:
            print(e)
            return False

    def delete_sight_type(self, id):
        try:
            self.__db.query("DELETE FROM sight_type_meta WHERE sight_type_id = %s", (id,))
            self.__db.query("DELETE FROM sight_has_sight_type WHERE sight_type_id = %s", (id,))
            self.__db.query("DELETE FROM sight_type WHERE id = %s", (id,))

            return True

        except Exception as e:
            print(e)
            return False 
