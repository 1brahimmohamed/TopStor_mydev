#!/usr/bin/python3
import sys, subprocess

def createvol(*args):
 datastr = ''
 leaderip = args[0] 
 owner = args[1] 
 ownerip = args[2]
 pool = args[3]
 name = args[4]
 ipaddress = args[5]
 Subnet = args[6]
 size = args[7]
 user = 'system'
 typep = args[8]
 if 'ISCSI' in typep:
  chapuser = 'MoatazNegm'
  chappas = 'MezoAdmin'
  extras = args[9].split('ee_ee')
  portalport =  extras[0]
  initiators = args[1]
  datastr = leaderip+' '+pool+' '+name+' '+size+' '+ipaddress+' '+Subnet+portalport+' '+initiators+' '+chapuser+' '+chappas+' disabled '+user+' '+owner+' '+user
 elif 'CIFSdom' in typep:
  extras = args[9].split('ee_ee')
  domname = extras[0]
  dompass = extras[1]
  domsrv = extras[2]
  domip = extras[3]
  domadmin = extras[4] 
  cmdline=['./encthis.sh',domname,dompass]
  dompass=subprocess.run(cmdline,stdout=subprocess.PIPE).stdout.decode().split('_result')[1].replace('/','@@sep')[:-1]
  datastr = leaderip+' '+pool+' '+name+' '+size+' '+ipaddress+' '+Subnet+' '+user+' '+owner+' '+user+' '+domname+' '+domsrv+' '+ domip+' '+domadmin+' '+dompass 
 else:
  groups = args[9] 
  print(leaderip+' '+pool+' '+name+' '+size+' '+groups+' '+ipaddress+' '+Subnet+' disabled '+user+' '+owner+' '+user)
  datastr = leaderip+' '+pool+' '+name+' '+size+' '+groups+' '+ipaddress+' '+Subnet+' disabled '+user+' '+owner+' '+user
 print('#############################')
 print('/TopStor/VolumeCreate'+typep,datastr)
 print('###########################')
 cmndstring = '/TopStor/VolumeCreate'+typep+' '+datastr
 result=subprocess.run(cmndstring.split(),stdout=subprocess.PIPE)
 return 


if __name__=='__main__':

 createvol(*sys.argv[1:])

