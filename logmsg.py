#!/usr/bin/python3
import subprocess,sys, datetime
import json
from etcdget import etcdget as get
from etcdput import etcdput as put 
from ast import literal_eval as mtuple
from sendhost import sendhost
def sendlog(leaderip,myhost, *args):
 z=[]
 knowns=[]
 dt=datetime.datetime.now().strftime("%m/%d/%Y")
 tm=datetime.datetime.now().strftime("%H:%M:%S")
 z=['/TopStor/logmsg2.sh', dt, tm, myhost ]
 for arg in args:
  z.append(arg)
 knowninfo=get(leaderip, 'known','--prefix')
 for k in knowninfo:
  knowns.append(k[1])
 msg={'req': 'msg2', 'reply':z}
 put(leaderip, 'notification',' '.join(z))
 sendhost(leaderip, str(msg),'recvreply',myhost)
 for k in knowninfo:
  sendhost(k[1], str(msg),'recvreply',myhost)
  knowns.append(k[1])

if __name__=='__main__':
 sendlog(*sys.argv[1:])
