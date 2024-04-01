class Wishlist:

    def __init__(self, db):
        self.__db = db

    def getWishlist(self, user_id, language_id=None):

        try:

            if language_id is None:
                language_id = self.__db.queryOne("SELECT id FROM language WHERE `default` = 1;")['id']

            wishlist = self.__db.query("SELECT s.id AS id, sm.name AS name, sm.description AS description, s.active AS active, s.open_time AS open_time, s.close_time AS close_time, s.age_category_id AS age_category_id FROM wishlist AS w JOIN sight AS s ON w.sight_id = s.id JOIN sight_meta AS sm ON s.id = sm.sight_id WHERE w.user_id = %s AND sm.language_id = %s;", (user_id, language_id))
            
            if wishlist is None:
                return True, "success", []

            for i in range(len(wishlist)):
                
                age_category = self.__db.queryOne("SELECT acm.name AS name FROM age_category AS ac JOIN age_category_meta AS acm ON ac.id = acm.age_category_id WHERE ac.id = %s AND acm.language_id = %s;", (wishlist[i]['age_category_id'], language_id))

                wishlist[i]['age_category'] = age_category['name']

                types = self.__db.query("SELECT stm.name AS name FROM sight_has_sight_type AS sst JOIN sight_type AS st ON sst.sight_type_id = st.id JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id WHERE sst.sight_id = %s AND stm.language_id = %s;", (wishlist[i]['id'], language_id))

                wishlist[i]['types'] = [type['name'] for type in types]

                photos = self.__db.query("SELECT photo FROM sight_photo WHERE sight_id = %s;", (wishlist[i]['id'],))

                wishlist[i]['photos'] = [photo['photo'] for photo in photos]

                number_of_visits = self.__db.queryOne("SELECT COUNT(*) AS count FROM visited_list WHERE sight_id = %s;", (wishlist[i]['id'],))

                wishlist[i]['visited'] = number_of_visits['count']

            return True, "success", wishlist
        
        except Exception as exception:
            return False, str(exception), None

    def sightInWishlist(self, sight_id, user_id):
        return self.__db.queryOne("SELECT * FROM wishlist WHERE sight_id=%s AND user_id=%s", (sight_id, user_id)) is not None

    def addSightToWishlist(self, sight_id, user_id):

        try:

            if self.__db.queryOne("SELECT * FROM wishlist WHERE sight_id=%s AND user_id=%s", (sight_id, user_id)) is not None:
                return False, "Sight already in wishlist"

            self.__db.query("INSERT INTO wishlist (sight_id, user_id) VALUES (%s, %s)", (sight_id, user_id))

            self.__db.commit()

            return True, "Success"
        
        except Exception as exception:
            return False, str(exception)
        
    def removeSightFromWishlist(self, sight_id, user_id):

        try:

            if self.__db.queryOne("SELECT * FROM wishlist WHERE sight_id=%s AND user_id=%s", (sight_id, user_id)) is None:
                return False, "Sight not in wishlist"

            self.__db.query("DELETE FROM wishlist WHERE sight_id=%s AND user_id=%s", (sight_id, user_id))

            self.__db.commit()

            return True, "Success"
        
        except Exception as exception:
            return False, str(exception)
