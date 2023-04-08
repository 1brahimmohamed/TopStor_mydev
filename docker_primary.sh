myclusterf='/topstorwebetc/mycluster'
mynodef='/topstorwebetc/mynode'
myhost=`echo $@ | awk '{print $1}'`
myhostip=`echo $@ | awk '{print $2}'`
leaderip=`echo $@ | awk '{print $3}'`
myclusterip=`echo $@ | awk '{print $4}'`
leader=$myhost
nmcli conn up mynode
zpool export -a
eth1='enp0s8'
eth2='enp0s8'
mynodedev=$eth1
myclusterdev=$eth1
data1dev=$eth2
data2dev=$eth2
setenforce 0
#targetcli clearconfig confirm=true
nmcli conn mod cmynode +ipv4.addresses $myclusterip 
nmcli conn up cmynode
myclusterip=$leaderip
pkill iscsiwatch
pkill topstorrecvreply
echo nameserver 10.11.12.7 >  /root/gitrepo/resolv.conf
rm -rf /TopStordata/etcd.sh
cp /TopStor/discovery.sh /TopStordata/etcd.sh
sed -i 's/SLEEP/sleep 10/g' /TopStordata/etcd.sh
echo starting etcd
docker run -itd --rm --name etcd --hostname etcd -v /etc/localtime:/etc/localtime:ro -v /root/gitrepo/resolv.conf:/etc/resolv.conf -p $etcd:2379:2379 -v /TopStor/:/TopStor -v /root/etcddata:/default.etcd  -v /TopStordata/etcd.sh:/runme.sh --net bridge0 moataznegm/quickstor:etcd
newip=`docker exec intdns nslookup etcd | grep Address | grep -v 127 | awk '{print $2}'`
echo newip=$newip
docker rm -f etcd 
rm -rf /TopStordata/etcd.sh
cp /TopStor/discovery.sh /TopStordata/etcd.sh
sed -i 's/SLEEP//g' /TopStordata/etcd.sh
sed -i "s/ETCDIP/$newip/g" /TopStordata/etcd.sh
docker run -itd --rm --name etcd --hostname etcd -v /etc/localtime:/etc/localtime:ro -v /root/gitrepo/resolv.conf:/etc/resolv.conf -p $myclusterip:2379:2379 -v /TopStor/:/TopStor -v /root/etcddata:/default.etcd  -v /TopStordata/etcd.sh:/runme.sh --net bridge0 moataznegm/quickstor:etcd
/pace/etcddel.py $leaderip sync/leader/Add_ --prefix
/pace/etcdput.py $leaderip sync/leader/Add_${myhost}_$myhostip/request leader_$stamp
/pace/etcdput.py $leaderip sync/leader/Add_${myhost}_$myhostip/request/$myhost leader_$stamp
templhttp='/TopStor/httpd_template.conf'
rm -rf /TopStordata/httpd.conf
cp /TopStor/httpd.conf /TopStordata/
shttpdf='/TopStordata/httpd.conf'
cp $templhttp $shttpdf
sed -i "s/MYCLUSTERH/$leaderip/g" $shttpdf
sed -i "s/MYCLUSTER/$leaderip/g" $shttpdf
echo running httpd fowrarder as I am not primary
docker run --rm --name httpd --hostname shttpd --net bridge0 -v /etc/localtime:/etc/localtime:ro -v /root/gitrepo/resolv.conf:/etc/resolv.conf -p $myclusterip:19999:19999 -p $myclusterip:80:80 -p $myclusterip:443:443 -v $shttpdf:/usr/local/apache2/conf/httpd.conf -v /root/topstorwebetc:/usr/local/apache2/topstorwebetc -v /topstorweb:/usr/local/apache2/htdocs/ -itd moataznegm/quickstor:git
docker run -itd --rm --name flask --hostname apisrv -v /etc/localtime:/etc/localtime:ro -v /pace/:/pace -v /pacedata/:/pacedata/ -v /root/gitrepo/resolv.conf:/etc/resolv.conf --net bridge0 -p $myclusterip:5001:5001 -v /TopStor/:/TopStor -v /TopStordata/:/TopStordata moataznegm/quickstor:flask
#/TopStor/topstorrecvreply.py $myhostip & disown
#/pace/iscsiwatchdog.sh $myhostip $myhost >/dev/null 2>/dev/null & disown 
#/pace/syncrequestlooper.sh $leaderip $myhost & disown
#/pace/fapilooper.sh & disown
#/pace/zfsping.py $leaderip $myhost & disown
#/pace/rebootmeplslooper.sh $leaderip $myhost & disown 

/TopStor/ioperf.py $leaderip $myhost
