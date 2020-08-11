"""A basic Tor testing network.

Instructions:

This profile creates a Tor testing network.

Wait for the profile instance to start, and wait for all of the startup 
processes to finish running. Then log in to the VM via SSH
as specified below.  

It may take a few minutes to build the Tor circuits.

To see the status of the Tor network, run

```
sudo -u debian-tor arm
```

on any of the Tor hosts (client, relay, or directory server).

To verify that the anonymity is working, on the client, run the 
following to see how you appear to the web server:

```
wget -qO- http://192.168.2.200/
```

Then, run the same command with Tor, and see how you appear to 
the webserver:

```
proxychains wget -qO- http://192.168.2.200/
```

If you need to restart the Tor process on any host:

```
sudo pkill -9 tor
sudo /etc/init.d/tor restart
```
"""

#
# NOTE: This code was machine converted. An actual human would not
#       write code like this!
#

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Node client
node_client = request.XenVM('client')
node_client.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_client.Site('Site 1')
node_client.ram = 4096
node_client.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/client-install.sh"))
iface0 = node_client.addInterface('interface-0', pg.IPv4Address('192.168.3.100','255.255.255.0'))

# Node webserver
node_webserver = request.XenVM('webserver')
node_webserver.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_webserver.Site('Site 1')
node_webserver.ram = 4096
node_webserver.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/webserver-install.sh"))
iface1 = node_webserver.addInterface('interface-14', pg.IPv4Address('192.168.2.200','255.255.255.0'))

# Node directoryserver
node_directoryserver = request.XenVM('directoryserver')
node_directoryserver.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_directoryserver.Site('Site 1')
node_directoryserver.ram = 4096
node_directoryserver.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/dir-install.sh"))
iface2 = node_directoryserver.addInterface('interface-2', pg.IPv4Address('192.168.1.4','255.255.255.0'))

# Node relay1
node_relay1 = request.XenVM('relay1')
node_relay1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_relay1.Site('Site 1')
node_relay1.ram = 4096
node_relay1.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/relay-install.sh"))
iface3 = node_relay1.addInterface('interface-4', pg.IPv4Address('192.168.11.2','255.255.255.0'))

# Node relay2
node_relay2 = request.XenVM('relay2')
node_relay2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_relay2.Site('Site 1')
node_relay2.ram = 4096
node_relay2.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/relay-install.sh"))
iface4 = node_relay2.addInterface('interface-17', pg.IPv4Address('192.168.12.2','255.255.255.0'))

# Node relay3
node_relay3 = request.XenVM('relay3')
node_relay3.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_relay3.Site('Site 1')
node_relay3.ram = 4096
node_relay3.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/relay-install.sh"))
iface5 = node_relay3.addInterface('interface-10', pg.IPv4Address('192.168.13.2','255.255.255.0'))

# Node relay4
node_relay4 = request.XenVM('relay4')
node_relay4.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_relay4.Site('Site 1')
node_relay4.ram = 4096
node_relay4.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/relay-install.sh"))
iface6 = node_relay4.addInterface('interface-6', pg.IPv4Address('192.168.16.2','255.255.255.0'))

# Node relay5
node_relay5 = request.XenVM('relay5')
node_relay5.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_relay5.Site('Site 1')
node_relay5.ram = 4096
node_relay5.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/relay-install.sh"))

iface7 = node_relay5.addInterface('interface-8', pg.IPv4Address('192.168.15.2','255.255.255.0'))

# Node router-1
node_router_1 = request.XenVM('router-1')
node_router_1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_router_1.Site('Site 1')
iface8 = node_router_1.addInterface('interface-1', pg.IPv4Address('192.168.3.1','255.255.255.0'))
iface9 = node_router_1.addInterface('interface-11', pg.IPv4Address('192.168.10.1','255.255.255.0'))

# Node router-3
node_router_3 = request.XenVM('router-3')
node_router_3.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_router_3.Site('Site 1')
iface10 = node_router_3.addInterface('interface-13', pg.IPv4Address('192.168.10.3','255.255.255.0'))
iface11 = node_router_3.addInterface('interface-15', pg.IPv4Address('192.168.2.1','255.255.255.0'))

# Node router-2
node_router_2 = request.XenVM('router-2')
node_router_2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU16-64-STD'
node_router_2.Site('Site 1')
iface12 = node_router_2.addInterface('interface-12', pg.IPv4Address('192.168.10.2','255.255.255.0'))
iface13 = node_router_2.addInterface('interface-3', pg.IPv4Address('192.168.1.1','255.255.255.0'))
iface14 = node_router_2.addInterface('interface-5', pg.IPv4Address('192.168.11.1','255.255.255.0'))
iface15 = node_router_2.addInterface('interface-7', pg.IPv4Address('192.168.16.1','255.255.255.0'))
iface16 = node_router_2.addInterface('interface-9', pg.IPv4Address('192.168.15.1','255.255.255.0'))
iface17 = node_router_2.addInterface('interface-16', pg.IPv4Address('192.168.13.1','255.255.255.0'))
iface18 = node_router_2.addInterface('interface-18', pg.IPv4Address('192.168.12.1','255.255.255.0'))

# Link link-0
link_0 = request.Link('link-0')
link_0.Site('undefined')
iface0.bandwidth = 10000
link_0.addInterface(iface0)
iface8.bandwidth = 10000
link_0.addInterface(iface8)

# Link link-3
link_3 = request.Link('link-3')
link_3.Site('undefined')
iface9.bandwidth = 10000
iface9.bandwidth = 10000
link_3.addInterface(iface9)
iface12.bandwidth = 10000
iface12.bandwidth = 10000
link_3.addInterface(iface12)
iface10.bandwidth = 10000
iface10.bandwidth = 10000
link_3.addInterface(iface10)

# Link link-4
link_4 = request.Link('link-4')
link_4.Site('undefined')
iface1.bandwidth = 10000
link_4.addInterface(iface1)
iface11.bandwidth = 10000
link_4.addInterface(iface11)

# Link link-1
link_1 = request.Link('link-1')
link_1.Site('undefined')
iface2.bandwidth = 10000
link_1.addInterface(iface2)
iface13.bandwidth = 10000
link_1.addInterface(iface13)

# Link link-2
link_2 = request.Link('link-2')
link_2.Site('undefined')
iface3.bandwidth = 10000
link_2.addInterface(iface3)
iface14.bandwidth = 10000
link_2.addInterface(iface14)

# Link link-5
link_5 = request.Link('link-5')
link_5.Site('undefined')
iface6.bandwidth = 10000
link_5.addInterface(iface6)
iface15.bandwidth = 10000
link_5.addInterface(iface15)

# Link link-6
link_6 = request.Link('link-6')
link_6.Site('undefined')
iface7.bandwidth = 10000
link_6.addInterface(iface7)
iface16.bandwidth = 10000
link_6.addInterface(iface16)

# Link link-7
link_7 = request.Link('link-7')
link_7.Site('undefined')
iface5.bandwidth = 10000
link_7.addInterface(iface5)
iface17.bandwidth = 10000
link_7.addInterface(iface17)

# Link link-8
link_8 = request.Link('link-8')
link_8.Site('undefined')
iface4.bandwidth = 10000
link_8.addInterface(iface4)
iface18.bandwidth = 10000
link_8.addInterface(iface18)


# Print the generated rspec
pc.printRequestRSpec(request)
