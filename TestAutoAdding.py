#-*- coding:UTF-8 -*-
import itchat, time
from itchat.content import TEXT, FRIENDS
import pymysql

# connect to datebase
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
# auto adding friend
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT)
def text_reply(msg):

    msgLeng = int(len(msg.text))
    msgDig = 0
    if msgLeng == 8:
        code = msg.text
        UserID = msg['FromUserName']

        # connect database
        query = "UPDATE login_request SET wechat_id='" + UserID + "', login_time=UNIX_TIMESTAMP() WHERE login_code='" + code + "'"
        # update database with user info
        db = DB()
        db.queryBySql(query)
        time.sleep(1)
        msg.user.send('服务器接收到您的请求，已经在进行处理')

    else:
        msg.user.send('请确认验证码并重新发送')
        pass

itchat.auto_login(hotReload=True)
itchat.run()