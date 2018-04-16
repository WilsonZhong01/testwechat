# -*- coding:UTF-8 -*-
import itchat
from itchat.content import TEXT, SHARING, SYSTEM
import pymysql, time, pdb


class DB:
    conn = None

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', passwd='', db='mq_admin', port=3306, charset="utf8")
        # self.conn = pymysql.connect(host='199.167.138.175', user='wilson', passwd='Hdf23Bxe', db='mq_admin', port=3306)

    def queryBySql(self, sql):
        cursor = self.conn.cursor()
        result = cursor.fetchmany(cursor.execute(sql))
        self.conn.commit()
        return result

    def __del__(self):
        self.conn.close()  # close database connection


db = DB()

itchat.auto_login(hotReload=True)
# Get all info about groups which are saved in the groupchat list
GroupInfo = itchat.get_chatrooms()

for group in GroupInfo:
    # get member list for each group
    detailedChatroom = itchat.update_chatroom(group['UserName'], detailedMember=True)
    pdb.set_trace()
    print(detailedChatroom)
    query = "INSERT INTO group_chat_content(group_id, member_num) VALUES('%s', '%s')" % (group['NickName'], group['MemberCount'])
    db.queryBySql(query)
# pdb.set_trace()


itchat.run()