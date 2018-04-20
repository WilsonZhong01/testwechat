# -*- coding: utf-8 -*-
import itchat
from itchat.content import *
from db.mysql import MysqlDB
from simple_settings import settings
import logging, time
import json
from modules.authentication import Authentication
from modules.robot import Robot
from modules.slack import Slack
from modules.friend import Friend
from modules.group import Group
import _thread, signal, sys, os, subprocess

DEBUG = settings.DEBUG

logger = logging.getLogger(__name__)

robotId = 0
robotName = ""
robot = None
mysql_pool = MysqlDB()

def loginRobot():

    logger.info("Robot login")
    if not settings.IS_TEST_ENV:
        Slack.sendLoginNotice("Robot *{}* had login.".format(robotName, robotId))

    robot.releaseLoginRobot(robotId)
    robot.updateHeartBeat(robotId)

    try:
        _thread.start_new_thread(robot.online, (robotId,))
    except:
        logger.error("Error: unable to start thread")
        sys.exit(0)


    group = Group(newInstance, robotId)
    try:
        _thread.start_new_thread(group.fetechAndAddGroupRepeat, ())
    except:
        logger.error("Error: unable to start thread")
        sys.exit(0)



def logoutRobot():

    logger.info("Robot logout")
    if not settings.IS_TEST_ENV:
        Slack.sendLoginNotice("Robot *{}* had logout.".format(robotName, robotId))

    robot.logout(robotId)
    #@TODO  we monitor the logout here to restart the service

def signal_term_handler(signal, frame):
    logoutRobot()
    if not settings.IS_TEST_ENV:
        parent_id = os.getpid()
        ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_id, shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read()
        retcode = ps_command.wait()
        for pid_str in ps_output.strip().split("\n")[:-1]:
            os.kill(int(pid_str), signal.SIGTERM)

    sys.exit(0)

if __name__ == "__main__":

    signal.signal(signal.SIGTERM, signal_term_handler)
    signal.signal(signal.SIGINT, signal_term_handler)


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


    @newInstance.msg_register(FRIENDS)
    def add_friend(msg):
        msg.user.verify()

        jsonMsg = json.dumps(msg)
        logger.debug(jsonMsg)

        fromUser = msg.FromUserName
        msgType = msg.MsgType

        friend = Friend(newInstance)
        friend.addFriendFromMsg(robotId, msg)

        robot.logMessage(fromUser, jsonMsg, msgType, 'friends', robotId)

        #msg.user.send('请回复验证码')


    @newInstance.msg_register([TEXT])
    def text_reply(msg):

        jsonMsg = json.dumps(msg)
        logger.debug(jsonMsg)

        msgText = msg.text
        fromUser = msg.FromUserName

        msgType = msg.MsgType

        if len(msgText) < 6:
            logger.info("trying to authorize user")
            friend = Friend(newInstance)
            alias = friend.addFriendFromMsg(robotId, msg)

            auth = Authentication()
            attemptNum = auth.attemptNumbers(fromUser)
            if attemptNum > 10:
                msg.user.send("验证失败，尝试过多")
            else:
                try:
                    loginCode = int(msgText)
                    nick_name = msg.User.NickName
                    loginId = auth.login(loginCode, alias, nick_name)
                    if loginId:
                        msg.user.send("验证成功， 登录 http://console.masterqun.com/client/directLogin/{}/{}/".format(loginCode, loginId))
                        logger.error("login ok code: {} text: {}".format(loginCode, msgText))
                    else:
                        logger.error("failed code: {} text: {}".format(loginCode, msgText))
                        msg.user.send("验证失败")
                except Exception:
                    pass


        robot.logMessage(fromUser, jsonMsg, msgType, 'login', robotId)

        #newInstance.send('Hello, filehelper', toUserName='filehelper')

    @newInstance.msg_register([MAP, CARD, NOTE, SHARING])
    def text_reply(msg):

        jsonMsg = json.dumps(msg)
        logger.debug(jsonMsg)


        fromUser = msg.FromUserName
        msgType = msg.MsgType

        friend = Friend(newInstance)
        friend.addFriendFromMsg(robotId, msg)

        robot.logMessage(fromUser, jsonMsg, msgType, 'others', robotId)



    @newInstance.msg_register([SYSTEM])
    def system_notice(msg):

        jsonMsg = json.dumps(msg)
        logger.debug(jsonMsg)

        fromUser = msg.FromUserName

        msgType = 0

        robot.logMessage(fromUser, jsonMsg, msgType, 'system', robotId)




    @newInstance.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def download_files(msg):
        #jsonMsg = json.dumps(msg)
        #logger.debug(jsonMsg)

        #msg.download(msg.fileName)
        pass
        ''''
        msg.download(msg.fileName)
        typeSymbol = {
            PICTURE: 'img',
            VIDEO: 'vid', }.get(msg.type, 'fil')
        return '@%s@%s' % (typeSymbol, msg.fileName)
        '''


    @newInstance.msg_register([TEXT, SHARING, MAP, PICTURE], isGroupChat=True)
    def group_text(msg):
        global MsgContent
        # which group message in
        chatRoom_id = msg['User']['NickName']
        # logger.debug(msg)
        # id of sender
        currentUserName = msg['ActualNickName']

        friend = Friend(newInstance)
        member_alias = friend.addFriendFromMsg(robotId, msg)
        # logger.debug(alias)
        # save message into database according to their types
        if msg['Type'] == TEXT:
            MsgContent = msg['Content']
            # logger.debug(MsgContent)
        elif msg['Type'] == SHARING:
            MsgContent = msg['Text']
            # logger.debug(MsgContent)
        elif (msg['Type'] != SHARING or msg['Type'] != TEXT):
            MsgContent = '1'

        connection = mysql_pool.connection()
        cur = connection.cursor()
        query = "INSERT INTO group_chat_content(group_id, user_nickname, content, member_id, content_type, time) VALUES(%s, %s, %s, %s, %s, UNIX_TIMESTAMP())"
        cur.execute(query, (chatRoom_id, currentUserName, MsgContent, member_alias, msg['Type']))


    newInstance.auto_login(enableCmdQR=settings.enableCmdQR, hotReload=True, statusStorageDir=storageFile,
                           loginCallback=loginRobot, exitCallback=logoutRobot, picDir=robot_qrcode_file )

    newInstance.run()

