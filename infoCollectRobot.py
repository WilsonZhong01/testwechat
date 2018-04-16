#-*- coding:UTF-8 -*-
import itchat
from itchat.content import TEXT, SHARING,SYSTEM
import pymysql, time, pdb


class DB:
    conn = None
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root',passwd='',db='mq_admin',port=3306, charset="utf8")
        # self.conn = pymysql.connect(host='199.167.138.175', user='wilson', passwd='Hdf23Bxe', db='mq_admin', port=3306)
    def queryBySql(self,sql):
        cursor = self.conn.cursor()
        result=cursor.fetchmany(cursor.execute(sql))
        self.conn.commit()
        return result

    def __del__(self):
        self.conn.close() # close database connection

db = DB()

# @itchat.msg_register([TEXT,SHARING, SYSTEM ])
# def text_reply(msg):
#     print(msg)

itchat.auto_login(hotReload=True)
# Get all info about groups which are saved in the groupchat list
GroupInfo = itchat.get_chatrooms()

# test different funcitons within contact.py

pdb.set_trace()
friendsInfo = itchat.get_friends()
# GroupNickName = GroupInfo['GroupNickName']
for group in GroupInfo:
    # get member list for each group
    detailedChatroom = itchat.update_chatroom(group['UserName'], detailedMember=True)
    print(detailedChatroom)
    query = "INSERT INTO group_info(group_name, member_num) VALUES('%s', '%s')" % (group['NickName'], group['MemberCount'])

    db.queryBySql(query)
pdb.set_trace()


# collecting group chat info

@itchat.msg_register([TEXT,SHARING], isGroupChat=True)
def group_text(msg):
    global MsgContent
    # which group message in
    chatRoom_id = msg['FromUserName']
    print(chatRoom_id)
    # id of sender
    currentUserName = msg['ActualNickName']
    print(currentUserName)
    # sava message into database according to their types
    if msg['Type'] == TEXT:
        MsgContent = msg['Content']
        print(MsgContent)
    elif msg['Type'] == SHARING:
        MsgContent = msg['Text']
        print(MsgContent)
    query = "INSERT INTO group_chat_content(group_id,user_name,content,content_type, time) VALUES('%s', '%s', '%s', '%s', UNIX_TIMESTAMP())" % (chatRoom_id, currentUserName, MsgContent, msg['Type'])
    db.queryBySql(query)

itchat.run()