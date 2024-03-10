from datetime import datetime as dt

class Sight:

    def __init__(self, db):
        self.__db = db

    def getAllSights(self, language_id=None, country_id=None, city_id=None, age_category_id=None, sight_types=None, active_only=True):

        if sight_types == []:
            return []

        if language_id is None:
            language_id = self.__db.query("SELECT id FROM language WHERE `default` = 1;")[0]['id']

        sights_query = """SELECT s.id AS id, sm.name AS name, sm.description AS description, sm.address AS address, cm.name AS city, ctrm.name AS country, s.google_maps_url AS google_maps_url, s.active AS active, s.open_time AS open_time, s.close_time AS close_time,
            acm.name AS age_category, stm.name AS sight_type,
            (SELECT COUNT(*) FROM visited_list WHERE user_id IS NOT NULL AND sight_id = s.id) AS visited
            FROM sight AS s
            LEFT OUTER JOIN city AS c ON s.city_id = c.id
            LEFT OUTER JOIN country AS ctr ON ctr.id = c.country_id
            LEFT OUTER JOIN city_meta AS cm ON c.id = cm.city_id
            LEFT OUTER JOIN country_meta AS ctrm ON ctr.id = ctrm.country_id
            LEFT OUTER JOIN sight_meta AS sm ON s.id = sm.sight_id
            LEFT OUTER JOIN age_category AS ac ON s.age_category_id = ac.id
            LEFT OUTER JOIN age_category_meta AS acm ON ac.id = acm.age_category_id
            LEFT OUTER JOIN sight_has_sight_type AS sst ON s.id = sst.sight_id
            LEFT OUTER JOIN sight_type AS st ON st.id = sst.sight_type_id
            LEFT OUTER JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id
            WHERE cm.language_id = %s AND sm.language_id = %s AND ctrm.language_id = %s AND stm.language_id = %s AND acm.language_id = %s"""
        
        if active_only:
            sights_query += " AND s.active = 1"
        
        parameters = [language_id, language_id, language_id, language_id, language_id]
        
        if age_category_id is not None:

            sights_query += " AND ac.id = %s"

            parameters.append(age_category_id)
        
        if country_id is not None and city_id is not None:

            sights_query += " AND c.country_id = %s AND c.id = %s"
        
            parameters.extend([country_id, city_id])

        elif country_id is not None:

            sights_query += " AND c.country_id = %s"

            parameters.append(country_id)

        elif city_id is not None:

            sights_query += " AND c.id = %s"

            parameters.append(city_id)

        if sight_types is not None:

            sights_query += f" AND st.id IN ({','.join(['%s' for _ in sight_types])});"

            parameters.extend(sight_types)

        else:
            sights_query += ";"

        sight_records = self.__db.query(sights_query, parameters)

        sights = {}

        for sight_record in sight_records:

            sight_id = sight_record['id']

            if sight_id not in sights:
                sights[sight_id] = {
                    'id': sight_id,
                    'name': sight_record['name'],
                    'description': sight_record['description'],
                    'city': sight_record['city'],
                    'country': sight_record['country'],
                    'google_maps_url': sight_record['google_maps_url'],
                    'active': sight_record['active'],
                    'open_time': None if sight_record['open_time'] is None else dt.strptime(sight_record['open_time'], '%H:%M').time(),
                    'close_time': None if sight_record['close_time'] is None else dt.strptime(sight_record['close_time'], '%H:%M').time(),
                    'age_category': sight_record['age_category'],
                    'visited': sight_record['visited'],
                    'sight_types': []
                }

            sights[sight_id]['sight_types'].append(sight_record['sight_type'])

        sights = list(sights.values())

        for i in range(len(sights)):

            sights[i]['achievements'] = self.__db.query("""SELECT a.*, am.name AS name, am.description AS description FROM achievement AS a
                LEFT OUTER JOIN sight_has_achievement AS sa ON a.id = sa.achievement_id
                LEFT OUTER JOIN achievement_meta AS am ON a.id = am.achievement_id
                WHERE sa.sight_id = %s AND am.language_id = %s;""", (sights[i]['id'], language_id))
            
            sights[i]['photos'] = [photo['photo'] for photo in self.__db.query("SELECT photo FROM sight_photo WHERE sight_id = %s;", (sights[i]['id'],))]

        return sights

    def getSight(self, sight_id, language_id=None):

        if language_id is None:
            language_id = self.__db.query("SELECT id FROM language WHERE `default` = 1;")[0]['id']

        sight = self.__db.query("""SELECT s.id AS id, sm.name AS name, sm.description AS description, sm.address AS address, cm.name AS city, ctrm.name AS country, s.google_maps_url AS google_maps_url, s.active AS active, s.open_time AS open_time, s.close_time AS close_time,
            acm.name AS age_category, stm.name AS sight_type
            FROM sight AS s
            LEFT OUTER JOIN city AS c ON s.city_id = c.id
            LEFT OUTER JOIN country AS ctr ON ctr.id = c.country_id
            LEFT OUTER JOIN city_meta AS cm ON c.id = cm.city_id
            LEFT OUTER JOIN country_meta AS ctrm ON ctr.id = ctrm.country_id
            LEFT OUTER JOIN sight_meta AS sm ON s.id = sm.sight_id
            LEFT OUTER JOIN age_category AS ac ON s.age_category_id = ac.id
            LEFT OUTER JOIN age_category_meta AS acm ON ac.id = acm.age_category_id
            LEFT OUTER JOIN sight_has_sight_type AS sst ON s.id = sst.sight_id
            LEFT OUTER JOIN sight_type AS st ON st.id = sst.sight_type_id
            LEFT OUTER JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id
            WHERE sm.language_id = %s AND cm.language_id = %s AND ctrm.language_id = %s AND stm.language_id = %s AND acm.language_id = %s AND s.id = %s;""", (language_id, language_id, language_id, language_id, language_id, sight_id))

        if len(sight) == 0:
            return None

        sight = sight[0]

        if sight['open_time'] is not None and sight['close_time'] is not None:

            sight['open_time'] = dt.strptime(sight['open_time'], '%H:%M').time()
            sight['close_time'] = dt.strptime(sight['close_time'], '%H:%M').time()

        sight['achievements'] = self.__db.query("""SELECT a.*, am.name AS name, am.description AS description FROM achievement AS a
            LEFT OUTER JOIN sight_has_achievement AS sa ON a.id = sa.achievement_id
            LEFT OUTER JOIN achievement_meta AS am ON a.id = am.achievement_id
            WHERE sa.sight_id = %s AND am.language_id = %s;""", (sight_id, language_id))

        sight['photos'] = [photo['photo'] for photo in self.__db.query("SELECT photo FROM sight_photo WHERE sight_id = %s;", (sight_id,))]

        return sight


    def getSightByCategory(self, category, language_id=None, active_only=True):
            
        if language_id is None:
            language_id = self.__db.query("SELECT id FROM language WHERE `default` = 1;")[0]['id']

        query = """SELECT s.id AS id, sm.name AS name, sm.description AS description, cm.name AS city, ctrm.name AS country, s.google_maps_url AS google_maps_url, s.active AS active, s.open_time AS open_time, s.close_time AS close_time,
            acm.name AS age_category, stm.name AS sight_type,
            (SELECT COUNT(*) FROM visited_list WHERE user_id IS NOT NULL AND sight_id = s.id) AS visited
            FROM sight AS s
            LEFT OUTER JOIN city AS c ON s.city_id = c.id
            LEFT OUTER JOIN country AS ctr ON ctr.id = c.country_id
            LEFT OUTER JOIN city_meta AS cm ON c.id = cm.city_id
            LEFT OUTER JOIN country_meta AS ctrm ON ctr.id = ctrm.country_id
            LEFT OUTER JOIN sight_meta AS sm ON s.id = sm.sight_id
            LEFT OUTER JOIN age_category AS ac ON s.age_category_id = ac.id
            LEFT OUTER JOIN age_category_meta AS acm ON ac.id = acm.age_category_id
            LEFT OUTER JOIN sight_has_sight_type AS sst ON s.id = sst.sight_id
            LEFT OUTER JOIN sight_type AS st ON st.id = sst.sight_type_id
            LEFT OUTER JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id
            WHERE sm.language_id = %s AND cm.language_id = %s AND ctrm.language_id = %s AND stm.language_id = %s AND acm.language_id = %s AND stm.name = %s"""

        if active_only:
            query += " AND s.active = 1"

        query += ";"

        sights = self.__db.query(query, (language_id, language_id, language_id, language_id, language_id, category))

        if sights is None:
            return None
        
        sights_dict = {}
        for sight in sights:
            sight_id = sight['id']

            if sight_id not in sights_dict:
                sights_dict[sight_id] = sight
                sights_dict[sight_id]['sight_types'] = []

            sights_dict[sight_id]['sight_types'].append(sight['sight_type'])

        sights = list(sights_dict.values())


        for i in range(len(sights)):
            sights[i]['achievements'] = self.__db.query("""SELECT a.*, am.name AS name, am.description AS description FROM achievement AS a
                LEFT OUTER JOIN sight_has_achievement AS sa ON a.id = sa.achievement_id
                LEFT OUTER JOIN achievement_meta AS am ON a.id = am.achievement_id
                WHERE sa.sight_id = %s AND am.language_id = %s;""", (sights[i]['id'], language_id))
                
            sights[i]['photos'] = [photo['photo'] for photo in self.__db.query("SELECT photo FROM sight_photo WHERE sight_id = %s;", (sights[i]['id'],))]

        return sights
