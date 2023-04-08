#!/usr/bin/python3
import subprocess,sys, datetime,socket
from etcdgetlocalpy import etcdget as get
from ast import literal_eval as mtuple

def getall(*bargs):
 #with open('/pacedata/perfmon') as f:
 # perfmon=f.read()
 #if perfmon:
 # queuethis('HostManualconfig.py','running')
 with open('/root/tmp','w') as f:
   f.write('bargs'+str(bargs)+'\n')
 leader = get('leader')[0]
 hosts = get('ready', '--prefix')
 allhosts= [] 
 hostsdict = dict()
 for host in hosts:
  hostname = host[0].replace('ready/','')
  hostip = host[1]
  ntp = get('ntp/'+hostname)[0]
  tz = get('tz/'+hostname)[0]
  gw = get('gw/'+hostname)[0]
  dnsname = get('dnsname/'+hostname)[0]
  dnssearch = get('dnssearch/'+hostname)[0]
  alias = get('alias/'+hostname)[0]
  try:
     ipaddrsubnet = get('ipaddr/'+hostname)[0].split('/')[1]
  except:
    ipaddrsubnet = '24'
  configured = get('configured/'+hostname)[0]
  if ipaddrsubnet == '_1':
   ipaddrsubnet = '24'
  if configured == '_1':
   configured = 'yes' 
  mgmt = get('namespace/mgmtip')[0] 
  allhosts.append({'name':hostname, 'configured':configured, 'alias':alias, 'ipaddr': hostip,'ipaddrsubnet':ipaddrsubnet, 'ntp':ntp, 'tz':tz, 'gw': gw,'dnsname':dnsname, 'dnssearch':dnssearch, 'cluster':mgmt})
  hostsdict[hostname] = { 'configured':configured, 'alias':alias, 'ipaddr': hostip, 'ipaddrsubnet':ipaddrsubnet, 'ntp':ntp, 'tz':tz, 'gw': gw, 'dnsname':dnsname, 'dnssearch':dnssearch, 'cluster':mgmt }

 print(allhosts)
 return hostsdict 

if __name__=='__main__':
 getall(*sys.argv[1:])
