import mysql.connector
from config.mariadb import *


class Database:
    def __init__(self, dict_cursor=False) -> None:

        dbconfig = {'host': HOST,
                    'user': USER,
                    'password': PASSWORD,
                    'database': DATABASE, }

        self.configuration = dbconfig

        self.__dict_cursor = dict_cursor

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(dictionary=self.__dict_cursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return None

    def queryOne(self, sql, params=None):
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None

    def commit(self):
        self.conn.commit()


if __name__ == "__main__":
    pass
