import itchat
from itchat.content import TEXT
import pdb
@itchat.msg_register(TEXT)
def text_reply(msg):

    verifycode = msg.text
    print(verifycode)

pdb.set_trace()
itchat.auto_login()
pdb.set_trace()
itchat.start_receiving()

pdb.set_trace()
