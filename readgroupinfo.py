# -*- coding:UTF-8 -*-

import itchat

from itchat.content import TEXT, SHARING, SYSTEM

import pymysql, time, pdb, json, logging

from db.mysql import MysqlDB

from simple_settings import settings



DEBUG = settings.DEBUG

logger = logging.getLogger()

robotId=0

mysql_pool = MysqlDB()

itchat.auto_login(hotReload=True)

# Get all info about groups which are saved in the groupchat list

GroupInfo = itchat.get_chatrooms()

connection = mysql_pool.connection()

cur = connection.cursor()

for group in GroupInfo:

    # get member list for each group

    query_group = "INSERT INTO group_info (name, number_members, notice) VALUES (%s, %s, %s)"

    cur.execute(query_group,(group['NickName'], group['MemberCount'], group['Self']['NickName']))

    # logger.debug(group)print

    detailedChatroom = itchat.update_chatroom(group['UserName'], detailedMember=True)

    memberlist_group = detailedChatroom['MemberList']

    for member in memberlist_group:


        query_member = "INSERT INTO member_info(user_name, nick_name, region ,city) VALUES(%s,%s,%s,%s)"

        cur.execute(query_member,(member['UserName'], member['NickName'], member['Province'],member['City']))


        # pdb.set_trace()


itchat.run()