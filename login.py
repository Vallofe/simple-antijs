# -*- coding: utf-8 -*-
from linepy import *
from akad.ttypes import OpType, Message, TalkException
from threading import Thread
import os, livejson, traceback, time, sys
from data import commands
OT = OpType

fileName = os.path.splitext(os.path.basename(__file__))[0]

db = livejson.File("token/%s.json" % fileName)

if ":" in db['token']:
    app = "ANDROIDLITE\t2.11.1\tAndroid OS\t5.1.1"
else:
    app = "DESKTOPWIN\t5.21.3\tWindows\t10"
try:
    client = LINE(idOrAuthToken=db["token"], appName=app)
except:
    e = traceback.format_exc()
    if "code=20" in e:print("FREEZING");time.sleep(3600);python3 = sys.executable;os.execl(python3, python3, *sys.argv)
    elif "code=8" in e or "code=7" in e:client = LINE(db["mail"],db["pass"],certificate='{}.crt'.format(db["mail"]),appName=app);db['token'] = client.authToken
    else:traceback.print_exc()
uid = client.profile.mid
poll = OEPoll(client)
good = commands(fileName, client, app, uid)
print("LOGIN SUCCESS")
def main_loop(op):
    if op.type == OT.RECEIVE_MESSAGE:good.receive_message(op)
    elif op.type == OT.NOTIFIED_KICKOUT_FROM_GROUP or op.type == 133:good.notif_kick_from_group(op)

while 1:
    try:
        ops = client.poll.fetchOperations(client.revision, 50)
        for op in ops:
            client.revision = max(client.revision, op.revision)
            t1 = Thread(target=main_loop(op,))
            t1.start()
            t1.join()
    except Exception as e:
        e = traceback.format_exc()
        if "EOFError" in e:pass
        elif "ShouldSyncException" in e or "LOG_OUT" in e:python3 = sys.executable;os.execl(python3, python3, *sys.argv)
        else:traceback.print_exc()