# -*- coding: utf-8 -*-
import itchat
from itchat.content import *
from db.mysql import MysqlDB
from simple_settings import settings
import logging
import json
from modules.authentication import Authentication
from modules.robot import Robot
from modules.slack import Slack
from modules.friend import Friend
import _thread

DEBUG = settings.DEBUG

logger = logging.getLogger(__name__)

robotId = 0
robotName = ""
robot = None
mysql_pool = MysqlDB()

def loginRobot():

    logger.info("Robot login")

    Slack.sendLoginNotice("Robot *{}* had login.".format(robotName, robotId))


    sql = "insert into temp (temp) values (%s) "

    connection = mysql_pool.connection()
    cur = connection.cursor()
    cur.execute(sql, ("Robot login"))

    robot.releaseLoginRobot(robotId)
    robot.updateHeartBeat(robotId)

    try:
        _thread.start_new_thread(robot.online, (robotId,))
    except:
        logger.error("Error: unable to start thread")
        exit()

def logoutRobot():

    logger.info("Robot logout")

    Slack.sendLoginNotice("Robot *{}* had logout.".format(robotName, robotId))


    sql = "insert into temp (temp) values (%s) "

    connection = mysql_pool.connection()
    cur = connection.cursor()

    cur.execute(sql, ("Robot logout"))

    #@TODO  we monitor the logout here to restart the service


if __name__ == "__main__":

    loggerItchat = logging.getLogger('itchat')


    robot = Robot()

    robotInfo = robot.acquireLoginRobot()
    robotId = robotInfo[0]
    robotName = robotInfo[1]

    if not robotId:
        logger.error("There is no available robot!")

        loggerItchat.error("There is no available robot!")
        exit()


    itchat.config.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"

    newInstance = itchat.new_instance()


    storageFile = 'newInstance{}.pkl'.format(robotId)

    robot_qrcode_file = "{}/qr{}.png".format(settings.ROBOT_QRCODE_DIR, robotId)

    if not settings.IS_TEST_ENV:
        loggerItchat.info("=================== LOGIN URL =====================")
        loggerItchat.info("Scan QR code at http://199.167.138.175/qr{}.png".format(robotId))

        Slack.sendLoginNotice("Robot *{}* requests to login: http://199.167.138.175/qr{}.png".format(robotName, robotId))


    #picDir=robot_qrcode_file
    newInstance.auto_login(enableCmdQR=settings.enableCmdQR, hotReload=True, statusStorageDir=storageFile,
                           loginCallback=loginRobot, exitCallback=logoutRobot, picDir=robot_qrcode_file )

    # # save group general information
    # GroupInfo = newInstance.get_chatrooms()
    # # GroupNickName = GroupInfo['GroupNickName']
    # for group in GroupInfo:
    #     # get member list for each group
    #     # detailedChatroom = itchat.update_chatroom(group['UserName'], detailedMember=True)
    #     # logger.debug(detailedChatroom)
    #     connection = mysql_pool.connection()
    #     cur = connection.cursor()
    #     # sql = "INSERT INTO msg_log (from_user, msg, msg_time, msg_type, action, robot_id) VALUES (%s, %s,  UNIX_TIMESTAMP(), %s, 'addfriend', %s)"
    #     sql = "INSERT INTO group_info(name) VALUES(%s)"
    #     result = cur.execute(sql, (group['NickName']))


    GroupInfo = newInstance.get_chatrooms()
    @newInstance.msg_register([TEXT, SHARING], isGroupChat=True)
    def group_text(msg):
        global MsgContent
        # which group message in
        chatRoom_id = msg['FromUserName']
        logger.debug(chatRoom_id)
        # id of sender
        currentUserName = msg['ActualNickName']
        logger.debug(currentUserName)
        # save message into database according to their types
        if msg['Type'] == TEXT:
            MsgContent = msg['Content']
            logger.debug(MsgContent)
        elif msg['Type'] == SHARING:
            MsgContent = msg['Text']
            logger.debug(MsgContent)
        connection = mysql_pool.connection()
        cur = connection.cursor()
        query = "INSERT INTO group_chat_content(group_id,user_name,content,content_type, time) VALUES('%s', '%s', '%s', '%s', UNIX_TIMESTAMP())" % (
            chatRoom_id, currentUserName, MsgContent, msg['Type'])
        cur.execute(query)

    newInstance.run()