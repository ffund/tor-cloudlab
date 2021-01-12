wget https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc
sudo apt-key add < A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc
sudo sh -c 'echo "deb http://deb.torproject.org/torproject.org/ bionic main" >> /etc/apt/sources.list.d/tor.list'
sudo apt-get update 
sudo apt-get -y --force-yes install tor vim curl tor-arm apache2 libapache2-mod-php expect

sudo service tor stop
sudo pkill -9 tor

sudo -u debian-tor mkdir /var/lib/tor/keys

sleep 2

sudo /usr/bin/expect /local/repository/dir.exp

sleep 2

sudo -u debian-tor tor --list-fingerprint --orport 1 --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" --datadirectory /var/lib/tor/

sudo service tor stop

finger1=$(sudo cat /var/lib/tor/keys/authority_certificate  | grep fingerprint | cut -f 2 -d ' ')
finger2=$(sudo cat /var/lib/tor/fingerprint | cut -f 2 -d ' ')

HOSTNAME=$(hostname -s)
ADDRESS=$(hostname -I | tr " " "\n" | grep "10.10")

sudo bash -c "cat >/etc/tor/torrc <<EOL
TestingTorNetwork 1
DataDirectory /var/lib/tor
RunAsDaemon 1
ConnLimit 60
Nickname $HOSTNAME
ShutdownWaitLength 0
PidFile /var/lib/tor/pid
Log notice file /var/log/tor/notice.log
Log info file /var/log/tor/info.log
Log debug file /var/log/tor/debug.log
ProtocolWarnings 1
SafeLogging 0
DisableDebuggerAttachment 0
SocksPort 0
OrPort 5000
ControlPort 9051
Address $ADDRESS
DirPort 7000
# An exit policy that allows exiting to IPv4 LAN
ExitPolicy accept 10.10.0.0/16:*
AuthoritativeDirectory 1
V3AuthoritativeDirectory 1
ContactInfo auth0@test.test
TestingV3AuthInitialVotingInterval 300
TestingV3AuthInitialVoteDelay 20
TestingV3AuthInitialDistDelay 20
EOL"

sudo bash -c "cat >/var/www/html/fingerprint <<EOL
DirAuthority $HOSTNAME orport=5000 no-v2 hs v3ident=$finger1 $ADDRESS:7000 $finger2
EOL"


sleep 90

DIRS=$(cat /etc/hosts | grep dir | cut -d ' ' -f 3)
for d in $DIRS
do
   wget -qO- http://"$d"/fingerprint  | sudo tee -a /etc/tor/torrc
done


sudo service tor restart

sleep 30

sudo cat /var/log/tor/debug.log | grep "Trusted"
