class VisitedList:

    def __init__(self, db):
        self.__db = db

    def sightInVisitedList(self, sight_id, user_id):
        return self.__db.queryOne("SELECT * FROM visited_list WHERE sight_id=%s AND user_id=%s", (sight_id, user_id)) is not None
    
    def addSightToVisitedList(self, sight_id, user_id, liked=None):
            
        try:
    
            if self.__db.queryOne("SELECT * FROM visited_list WHERE sight_id=%s AND user_id=%s", (sight_id, user_id)) is not None:
                return False, "Sight already in visited list"
    
            self.__db.query("INSERT INTO visited_list (sight_id, user_id, liked) VALUES (%s, %s, %s)", (sight_id, user_id, liked))

            self.__db.query("DELETE FROM wishlist WHERE sight_id=%s AND user_id=%s", (sight_id, user_id))
    
            self.__db.commit()
    
            return True, "Success"
            
        except Exception as exception:
            return False, str(exception)
        
    def removeSightFromVisitedList(self, sight_id, user_id):

        try:

            if self.__db.queryOne("SELECT * FROM visited_list WHERE sight_id=%s AND user_id=%s", (sight_id, user_id)) is None:
                return False, "Sight not in visited list"

            self.__db.query("DELETE FROM visited_list WHERE sight_id=%s AND user_id=%s", (sight_id, user_id))

            self.__db.commit()

            return True, "Success"
        
        except Exception as exception:
            return False, str(exception)
