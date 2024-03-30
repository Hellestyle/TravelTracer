class Wishlist:

    def __init__(self, db):
        self.__db = db

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
