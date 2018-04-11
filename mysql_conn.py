import pymysql

class DB:
    conn = None
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root',passwd='',db='mq_admin',port=3306)

    def queryBySql(self,sql):
        cursor = self.conn.cursor()
        result=cursor.fetchmany(cursor.execute(sql))
        self.conn.commit()
        return result

    def __del__(self):
        self.conn.close() # close database connection


# main

db = DB()
a = 1234578
b = 'yourname'
print(a)
db.queryBySql("INSERT INTO robots (id, wechat_id) VALUES ('%s', '%s')" %(a, b))
