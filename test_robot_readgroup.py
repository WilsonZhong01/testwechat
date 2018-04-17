# -*- coding:UTF-8 -*-
import itchat
from itchat.content import TEXT, SHARING, SYSTEM
import pymysql, time, pdb, json, logging
from db.mysql import MysqlDB
from simple_settings import settings

DEBUG = settings.DEBUG
logger = logging.getLogger()

mysql_pool = MysqlDB()
itchat.auto_login(hotReload=True)
# Get all info about groups which are saved in the groupchat list
GroupInfo = itchat.get_chatrooms()

for group in GroupInfo:
    # get member list for each group
    detailedChatroom = itchat.update_chatroom(group['UserName'], detailedMember=True)
    # pdb.set_trace()
    connection = mysql_pool.connection()
    cur = connection.cursor()
    # query = "INSERT INTO group_member_info(member_num,name) VALUES(%s)"   # name,detailedChatroom['NickName'],
    # cur.execute(query, (detailedChatroom['MemberCount'], detailedChatroom['NickName']))
    memberlist_group = detailedChatroom['MemberList']
    for member in memberlist_group:
        jsonMem = json.dumps(member)
        # logger.debug(jsonMem)
        query = "INSERT INTO group_member_info(member_num, group_name, member_info) VALUES(%s, %s, %s)"
        cur.execute(query,(detailedChatroom['MemberCount'], detailedChatroom['NickName'],jsonMem))
        # pdb.set_trace()
# pdb.set_trace()

itchat.run()