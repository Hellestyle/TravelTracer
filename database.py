import mysql.connector


class Database:
    def __init__(self) -> None:
        dbconfig = {'host': 'kark.uit.no',
                    'user': 'stud_v23_she199',
                    'password': 'Q7TOeuhlLTSj2lfT',
                    'database': 'stud_v23_she199', }
        self.configuration = dbconfig

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    
    def query(self,sql,params=None):
        self.cursor.execute(sql,params)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return None


    def queryOne(self,sql,params=None):
        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None
    

if __name__ == "__main__":
    pass
