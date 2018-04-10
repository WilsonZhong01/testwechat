import itchat, time, sys
from itchat.content import TEXT
def output_info(msg):
    print('[INFO] %s' % msg)

def open_QR():
    for get_count in range(10):
        output_info('Getting uuid')
        uuid = itchat.get_QRuuid()
        while uuid is None: uuid = itchat.get_QRuuid();time.sleep(1)
        output_info('Getting QR Code')
        if itchat.get_QR(uuid): break
        elif get_count >= 9:
            output_info('Failed to get QR Code, please restart the program')
            sys.exit()
        return uuid
    output_info('Please scan the QR Code')


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
        output_info('Reloading QR Code')
        uuid = open_QR()
        waitForConfirm = False
userInfo = itchat.web_init()
itchat.show_mobile_login()
itchat.get_friends(True)

output_info('Login successfully as %s'%userInfo['User']['NickName'])
itchat.start_receiving()
@itchat.msg_register(TEXT)
def simple_reply(msg):
    if msg['Type']=='Text':
        print('I received: %s'%msg.text)


itchat.run()