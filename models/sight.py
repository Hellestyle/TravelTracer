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
            acm.age_category_id, acm.name AS age_category, stm.name AS sight_type, s.active AS active, stm.sight_type_id AS sight_type_id
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

        if sight is None:
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
            ac.id AS age_id, acm.name AS age_category, stm.name AS sight_type,
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

    
    def getSightByAge(self, age, language_id=None, active_only=True):
        if language_id is None:
            language_id = self.__db.query("SELECT id FROM language WHERE `default` = 1;")[0]['id']
        
        query = """SELECT s.id AS id, sm.name AS name, sm.description AS description, cm.name AS city, ctrm.name AS country, s.active AS active, stm.name AS sight_type,
            ac.id AS age_id, acm.name AS age_category,
            (SELECT COUNT(*) FROM visited_list WHERE user_id IS NOT NULL AND sight_id = s.id) AS visited
            FROM sight AS s
            LEFT OUTER JOIN sight_meta AS sm ON s.id = sm.sight_id
            LEFT OUTER JOIN city AS c ON s.city_id = c.id
            LEFT OUTER JOIN city_meta AS cm ON c.id = cm.city_id
            LEFT OUTER JOIN country AS ctr ON ctr.id = c.country_id
            LEFT OUTER JOIN country_meta AS ctrm ON ctr.id = ctrm.country_id
            LEFT OUTER JOIN sight_has_sight_type AS sst ON s.id = sst.sight_id
            LEFT OUTER JOIN sight_type AS st ON st.id = sst.sight_type_id
            LEFT OUTER JOIN sight_type_meta AS stm ON st.id = stm.sight_type_id
            LEFT OUTER JOIN age_category AS ac ON s.age_category_id = ac.id
            LEFT OUTER JOIN age_category_meta AS acm ON ac.id = acm.age_category_id
            WHERE sm.language_id = %s AND cm.language_id = %s AND ctrm.language_id = %s AND stm.language_id = %s AND acm.language_id = %s"""
        
        if active_only:
            query += " AND s.active = 1"

        query += ";"

        sights = self.__db.query(query, (language_id, language_id, language_id, language_id, language_id))

        if sights is None:
            return None
        
        sights_dict = {}

        for sight in sights:
            if sight['age_id'] == age:
                sight_id = sight['id']

                if sight_id not in sights_dict:
                    sights_dict[sight_id] = {
                        'id': sight_id,
                        'name': sight['name'],
                        'description': sight['description'],
                        'city': sight['city'],
                        'country': sight['country'],
                        'active': sight['active'],
                        'sight_types': [],
                        'age_id': sight['age_id'],
                        'age_category': sight['age_category'],
                        'visited': sight['visited']
                    }
                
                sights_dict[sight_id]['sight_types'].append(sight['sight_type'])

        sights = list(sights_dict.values())

        for i in range(len(sights)):
            sights[i]['achievements'] = self.__db.query("""SELECT a.*, am.name AS name, am.description AS description FROM achievement AS a
                LEFT OUTER JOIN sight_has_achievement AS sa ON a.id = sa.achievement_id
                LEFT OUTER JOIN achievement_meta AS am ON a.id = am.achievement_id
                WHERE sa.sight_id = %s AND am.language_id = %s;""", (sights[i]['id'], language_id))
                
            sights[i]['photos'] = [photo['photo'] for photo in self.__db.query("SELECT photo FROM sight_photo WHERE sight_id = %s;", (sights[i]['id'],))]

        return sights
    

    def update_sight(self, id, name, age_category_id, address, google_maps_url, active, open_time, close_time, description, image_names, sight_type_id, old_sight_type_id):
        try:
            self.__db.query("UPDATE sight SET age_category_id = %s, google_maps_url = %s, active = %s, open_time = %s, close_time = %s WHERE id = %s;", (age_category_id, google_maps_url, active, open_time, close_time, id))
            self.__db.query("UPDATE sight_meta SET name = %s, address = %s, description = %s WHERE sight_id = %s;", (name, address, description, id))
            self.__db.query("UPDATE sight_has_sight_type SET sight_type_id = %s WHERE sight_id = %s AND sight_type_id = %s",(sight_type_id, id, old_sight_type_id))
            if image_names != "":
                self.update_sight_image(id, image_names)
            return True, "Sight updated successfully."
        
        except Exception as e:
            return False, str(e)
        
    def update_sight_image(self,sight_id,image_names):
        for image_name in image_names:
            self.__db.query("INSERT INTO `sight_photo` (`id`, `sight_id`, `photo`) VALUES (NULL, %s,%s)",(sight_id, image_name,))


        
    
    def add_sight(self, name, age_category_id, address, google_maps_url, active, open_time, close_time, description, sight_type_id,city_id=None, language_id=None):
        try:
            city_id = 3 if city_id is None else city_id
            language_id = 1 if language_id is None else language_id
            self.__db.query("INSERT INTO sight (city_id, age_category_id, google_maps_url, active, open_time, close_time) VALUES (%s, %s, %s, %s, %s, %s);", (city_id, age_category_id, google_maps_url, active, open_time, close_time))
            sight_id = self.__db.query("SELECT LAST_INSERT_ID();")[0]['LAST_INSERT_ID()']
            self.__db.query("INSERT INTO sight_meta (sight_id, language_id, name, address, description) VALUES (%s, %s, %s, %s, %s);", (sight_id, language_id, name, address, description))
            self.__db.query("INSERT INTO `sight_has_sight_type` (`sight_id`, `sight_type_id`) VALUES (%s, %s)",(sight_id,sight_type_id))


            return True, "Sight added successfully."
        
        except Exception as e:
            return False, str(e)

    def add_sight_image(self, sight_id, image_name):
        try:
            self.__db.query("INSERT INTO `sight_photo` (`id`, `sight_id`, `photo`) VALUES (NULL, %s, %s)", (sight_id, image_name,))
            return True, "Image added to new sight successfully"
            
        except Exception as e:
            return False, str(e)
        
    def delete_sight_image(self, image_path):
        try:
            self.__db.query("DELETE FROM `sight_photo` WHERE photo = %s;",(image_path,))
            return True, "Image deleted from sight successfully"
            
        except Exception as e:
            return False, str(e)
        
    def get_image_ids(self, sight_id):
        try:
            ids = self.__db.query("SELECT id, photo from sight_photo WHERE sight_id = %s;", (sight_id,))
            return ids
        except Exception as e:
            return False, str(e)

    def update_image_order(self, ids, sight_id, image_names):
        #Can probably be rewritten to only send one single update query rather than one per image
        try:
            for i in range(len(image_names)):
                self.__db.query("UPDATE sight_photo SET photo = %s WHERE id = %s AND sight_id = %s;", (image_names[i], ids[i], sight_id,))

        except Exception as e:
            return False, str(e)
        
    
    def get_a_single_sight_statistic(self, sight_id):
        result = self.__db.queryOne("SELECT COUNT(vl1.liked = 1) AS liked, COUNT(vl2.liked = 0) AS disliked \
                        FROM (SELECT DISTINCT id FROM visited_list WHERE sight_id = %s) AS ids \
                        LEFT JOIN visited_list AS vl1 ON ids.id = vl1.id AND vl1.liked = 1 \
                        LEFT JOIN visited_list AS vl2 ON ids.id = vl2.id AND vl2.liked = 0", (sight_id,))
        if result:
            statistic = {
                'liked': str(result['liked']),
                'disliked': str(result['disliked'])
            }
            return statistic
        else:
            return {}


    def get_all_sight_statistics(self):
        results = self.__db.query("SELECT sights.sight_id, COUNT(vl1.liked = 1) AS liked, COUNT(vl2.liked = 0) AS disliked \
                                FROM (SELECT DISTINCT sight_id FROM visited_list) AS sights \
                                LEFT JOIN visited_list AS vl1 ON sights.sight_id = vl1.sight_id AND vl1.liked = 1 \
                                LEFT JOIN visited_list AS vl2 ON sights.sight_id = vl2.sight_id AND vl2.liked = 0 \
                                GROUP BY sights.sight_id;")
        if results:
            return results
        else:
            return {}
