from database import Database
from models.user import User

class Achievement:

    #def __init__(self,aId , icon = "" ,langId=None, name = "",desc="", level=0) -> None:
    #    self.getAchievementData()
    #    self.__name = name
    #    self.__level = level
    #    self.__aId = aId
    #    self.__icon = icon
    #    self.__desc = desc
    #    self.__langID = langId
    
    def __init__(self, db):
        self.__db = db

    def getLevel(self):
        return self.__level
    def getName(self):
        return self.__name
    def getId(self):
        return self.__aId
    
    def getAchievementData(self, id):
        with Database() as db:
            try:
                result = db.queryOne("SELECT a.id, a.icon, am.language_id, am.name, am.description FROM achievement a JOIN achievement_meta am ON a.id = am.achievement_id WHERE a.id = %s AND am.language_id = 1",(id,))
            except:
                return "Error with db"
            self.__aId = id
            self.__icon = result[1]
            self.__name = result[3]
            self.__desc = result[4]
    
    def getAchievements(self, language_id=None):

        try:

            if language_id is None:
                language_id = self.__db.queryOne("SELECT id FROM language WHERE `default` = 1;")['id']

            achievements = self.__db.query("SELECT a.id AS id, a.icon AS icon, am.name AS name, am.description AS description FROM achievement a JOIN achievement_meta am ON a.id = am.achievement_id WHERE am.language_id = %s;", (language_id,))
            
            return True, "success", achievements
        
        except Exception as exception:
            return False, str(exception), None
        
    def getUserAchievements(self, user_id, language_id=None):

        try:

            if language_id is None:
                language_id = self.__db.queryOne("SELECT id FROM language WHERE `default` = 1;")['id']

            achievements = self.__db.query("SELECT a.id AS id, COUNT(a.id) AS count FROM visited_list AS vl JOIN sight AS s ON vl.sight_id = s.id JOIN sight_has_achievement AS sha ON sha.sight_id = s.id JOIN achievement AS a ON a.id = sha.achievement_id JOIN achievement_meta AS am ON a.id = am.achievement_id WHERE user_id = %s AND language_id = %s group by a.id;", (user_id, language_id))
            
            return True, "success", {} if achievements is None else {achievement['id']: achievement['count'] for achievement in achievements}
        
        except Exception as exception:
            return False, str(exception), None
