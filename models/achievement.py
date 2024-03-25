from database import Database
from user import User

class Achievement:
    def __init__(self,aId , icon = "" ,langId=None, name = "",desc="", level=0) -> None:
        self.getAchievementData()
        self.__name = name
        self.__level = level
        self.__aId = aId
        self.__icon = icon
        self.__desc = desc
        self.__langID = langId
        

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
            