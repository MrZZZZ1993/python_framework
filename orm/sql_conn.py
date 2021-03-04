import mysql.connector.pooling


class BaseDB:
    def __init__(self, user, password, database, host='127.0.0.1', port=3306):
        self.__config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
        self.pool = self.connect()

    def connect(self):
        try:
            pool = mysql.connector.pooling.MySQLConnectionPool(**self.__config, pool_size=10)
            return pool
        except Exception as e:
            print(e)
        return None

    def execute(self, sql, params=None):
        try:
            con = self.pool.get_connection()
            cursor = con.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                sql = 'INSERT INTO users (`id`, `password`, `name`) VALUES (9, `12222`, `1233`)'
                print(sql)
                cursor.execute(sql)

            # result = cursor.fetchall()
            return None
        except Exception as e:
            print(e)
        finally:
            if 'con' in dir():
                con.close()



