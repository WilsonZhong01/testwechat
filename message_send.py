import itchat
from itchat.content import TEXT

@itchat.msg_register(TEXT)
def Auto_reply(msg):

    verifycode = msg.text
    print(msg['FromUserName'])
    print(msg['CreateTime'])
    print(msg['User']['NickName'])
    print(msg)

itchat.auto_login(hotReload=True)
itchat.run()

