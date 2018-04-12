import itchat, threading, time
from itchat.content import TEXT

@itchat.msg_register(TEXT)
def Auto_reply(msg):

    print(msg['FromUserName'])
    print(msg.text)
    print(msg['User']['NickName'])
    print(msg)

@itchat.run()
def self_detect():
    global uuid
    print('we are testing...')
    robot_status = itchat.check_login(uuid)
    if robot_status != '200':
        itchat.auto_login(hotReload=True)
        itchat.run()

    # Rebuild the timer
    timer = threading.Timer(1, main)
    timer.start()


def main():
    global uuid
    itchat.auto_login(hotReload=True)
    uuid = itchat.get_QRuuid()
    timer = threading.Timer(1, Timer_Fun)
    timer.start()
    time.sleep(100 * 1)
    timer.cancel()


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()


