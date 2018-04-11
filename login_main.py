# -*- coding:utf-8 -*-
import itchat, time, sys
from itchat.content import TEXT
import threading

global uuid

def output_info(msg):
    print('[INFO] %s' % msg)

def open_QR():
    global uuid
    for get_count in range(15):
        output_info('Getting uuid')
        uuid = itchat.get_QRuuid()
        while uuid is None:
            uuid = itchat.get_QRuuid()
            time.sleep(1)
        output_info('Getting QR code')
        if itchat.get_QR(uuid):
            break
        elif get_count>= 9:
            output_info('没有正常获取二维码，请刷新页面')
        return uuid
    output_info('请扫描二维码')

def read_status():

    global count, timer, uuid
    count += 1
    print('timer runs every 1 second, and this is the %s' %count +' time')
    status = itchat.check_login(uuid)
    print('The present status for # robot service is: %s'%status)

    # rebuild timer
    timer = threading.Timer(5,read_status)
    timer.start()

def timer_fun():
    # count = 0
    global timer, count
    count = 0
    timer = threading.Timer(1, read_status)
    timer.start()
    # read_status()

# login Wechat
def main():
    global timer
    uuid = open_QR()
    waitForConfirm = False
    while 1:
        status = itchat.check_login(uuid)
        if status == '200':
            print(status)
            break
        elif status == '201':
            print(status)
            if waitForConfirm:
                output_info('Please press confirm')
                waitForConfirm = True
        elif status == '408':
            print(status)
            output_info('Reloading QR code')
            uuid = open_QR()
            waitForConfirm = False
    userInfo = itchat.web_init()
    itchat.show_mobile_login()
    itchat.get_friends()
    output_info('login successfully with %s' % userInfo['User']['NickName'])
    itchat.start_receiving()

    @itchat.msg_register(TEXT)
    def simple_reply(msg):
        if msg['Type'] == 'Text':
            print('I received: %s' % msg.text)

    timer_fun()
    # time.sleep(20 * 5)
    # timer.cancel()
    itchat.run()

if __name__ == '__main__':
    # run fun every 1 min
    main()
    # count = 0



