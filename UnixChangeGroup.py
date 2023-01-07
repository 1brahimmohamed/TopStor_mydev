#!/usr/bin/python3
from privthis import privthis 
import subprocess,sys
from etcdgetpy import etcdget as get
from etcdput import etcdput as put 
from time import time as stamp
from logqueue import queuethis, initqueue
from logmsg import sendlog, initlog

leaderip = ''
myhsot = ''

def main(leaderip, myhost, groupname, groupusers, userreq, ischange):
    ispriv=privthis(leaderip, 'Box_users',userreq)
    if 'rue' not in ispriv:
        return
    leader = get(leaderip,'leader')[0]
    if leader != myhost:
        etcdip = get(leaderip,'ready/'+myhost)[0]
    else:
        etcdip = leaderip
 
    initqueue(leaderip, myhost)
    initlog(leaderip, myhost)

    queuethis('groupchange','running',userreq)
    sendlog('Unst1025','info',userreq, groupname)
    groupusers = groupusers.replace('users','')
    origgrp = get( etcdip, 'usersigroup/'+groupname)[0]
    if groupusers == 'NoUser':
        groupusers = ''
    neworiggrp = origgrp.split('/')
    oldusers = neworiggrp[2] 
    if oldusers == 'NoUser':
        oldusers = ''
    susers = set(groupusers.split(','))
    solds = set(oldusers.split(','))
    toremove = solds - susers
    toadd = susers - solds
    if ischange == 'adddel':
        neworiggrp[2] = ",".join(list(solds.union(susers)))
    else:
        neworiggrp[2] = groupusers
    if neworiggrp[2] == '':
        neworiggrp[2] = 'NoUser'
    if ischange == 'change':
        put( etcdip, 'usersigroup/'+groupname, "/".join(neworiggrp))
    else:
        put( etcdip, 'usersigroup/'+groupname, "/".join(neworiggrp))
    if leader == myhost:
        put( leaderip, 'sync/user/usergroups/request/'+myhost, 'GrpChange_'+groupname+'_'+str(stamp()))
        put( leaderip, 'sync/user/usergroups/request/', 'GrpChange_'+groupname+'_'+str(stamp()))
    
    for user in toremove:
        cmdline='gpasswd -d '+user+' '+groupname
        result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8') 
    for user in toadd:
        cmdline='gpasswd -a '+user+' '+groupname
        result = subprocess.run(cmdline.split(),stdout=subprocess.PIPE).stdout.decode('utf-8') 
    sendlog('Unsu1025','info',userreq, groupname)
    queuethis('groupchange','stop',userreq)
    return
if __name__=='__main__':
    leaderip=sys.argv[1]
    myhost = sys.argv[2]
    groupname=sys.argv[3]
    groupusers=sys.argv[4]
    userreq=sys.argv[5]
    ischange=sys.argv[6]
    main(leaderip, myhost, groupname, groupusers, userreq, ischange)
