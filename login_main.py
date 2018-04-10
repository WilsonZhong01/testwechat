# -*- coding:utf-8 -*-
import itchat, time, sys
from itchat.content import TEXT

def output_info(msg):
    print('[INFO] %s' % msg)

def open_QR():
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
            sys.exit()
        return uuid
    output_info('请扫描二维码')

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
            output_info('请点击确认键')
            waitForConfirm = True
    elif status == '408':
        print(status)
        output_info('重新加载二维码')
        uuid = open_QR()
        waitForConfirm = False
userInfo = itchat.web_init()
itchat.show_mobile_login()
itchat.get_friends(True)

output_info('Login successfully as %s' %userInfo['User']['NickName'])


















if __name__ == '__main__':
