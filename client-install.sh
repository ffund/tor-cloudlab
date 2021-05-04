wget https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc
sudo apt-key add < A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc
sudo sh -c 'echo "deb http://deb.torproject.org/torproject.org/ bionic main" >> /etc/apt/sources.list.d/tor.list'
sudo apt-get update
sudo apt-get -y --force-yes install tor vim curl tor-arm proxychains libvlc5 

sudo service tor stop
sudo pkill -9 tor

sudo -u debian-tor tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor/

sudo service tor stop

sleep 360

sudo bash -c "cat >/etc/tor/torrc <<EOL
TestingTorNetwork 1
DataDirectory /var/lib/tor
RunAsDaemon 1
ConnLimit 60
ShutdownWaitLength 0
PidFile /var/lib/tor/pid
Log notice file /var/log/tor/notice.log
Log info file /var/log/tor/info.log
Log debug file /var/log/tor/debug.log
ProtocolWarnings 1
SafeLogging 0
DisableDebuggerAttachment 0
SocksPort 9050
ControlPort 9051
UseEntryGuards 0
EOL"

DIRS=$(cat /etc/hosts | grep dir | cut -d ' ' -f 3)
for d in $DIRS
do
    nc -z "$d" 80
	until [ "$?" == "0" ]
	do
		echo "Waiting for $d to come online..."
		sleep 5
	    nc -z "$d" 80
   done
   wget -qO- http://"$d"/fingerprint  | sudo tee -a /etc/tor/torrc
done


HOSTNAME=$(hostname -s)
echo "Nickname $HOSTNAME" | sudo tee -a /etc/tor/torrc
ADDRESS=$(hostname -I | tr " " "\n" | grep "10.10")
echo "Address $ADDRESS" | sudo tee -a /etc/tor/torrc

sudo cat /etc/tor/torrc

sudo service tor restart
