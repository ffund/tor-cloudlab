sudo apt-get update
sudo apt-get -y --force-yes install tor vim curl tor-arm
sudo pkill -9 tor

sleep 240

sudo -u debian-tor tor --list-fingerprint --orport 1 \
    --dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    --datadirectory /var/lib/tor/

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
SocksPort 0
OrPort 5000
ControlPort 9051
# An exit policy that allows exiting to IPv4 LAN
ExitPolicyRejectPrivate 0
ExitPolicy accept 10.10.0.0/16:*
ExitPolicy reject *:*
EOL"

DIRS=$(cat /etc/hosts | grep dir | cut -d ' ' -f 3)
for d in $DIRS
do
   wget -qO- http://"$d"/fingerprint  | sudo tee -a /etc/tor/torrc
done

HOSTNAME=$(hostname -s)
echo "Nickname $HOSTNAME" | sudo tee -a /etc/tor/torrc
ADDRESS=$(hostname -I | tr " " "\n" | grep "10.10")
echo "Address $ADDRESS" | sudo tee -a /etc/tor/torrc

sudo cat /etc/tor/torrc

sudo /etc/init.d/tor restart
