"""A basic Tor testing network.

Instructions:

This profile creates a Tor testing network.

Wait for the profile instance to start, and wait for all of the startup 
processes to finish running. Then log in to the VM via SSH
as specified below.  

It may take a few minutes to build the Tor circuits.

To see the status of the Tor network, run

```
sudo -u debian-tor nyx
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
sudo service tor stop
sudo pkill -9 tor
sudo service tor restart
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

# describe parameters
pc.defineParameter("n_dir", "Number of directory servers", portal.ParameterType.INTEGER, 3)
pc.defineParameter("n_relay", "Number of relays (that are not directory servers)", portal.ParameterType.INTEGER, 5)
pc.defineParameter("n_client", "Number of clients", portal.ParameterType.INTEGER, 1)

# Get values specified by user during instantiation
params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# set up clients!
# link between clients and router 1
link_clients_router = request.Link('link-clients-router')
link_clients_router.Site('Site 1')
for i in range(params.n_client):
	# Node client
	node_client = request.XenVM('client' + str(i+1))
	node_client.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
	node_client.Site('Site 1')
	node_client.ram = 4096
	node_client.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/client-install.sh"))
	iface_client = node_client.addInterface('interface-client-' + str(i+1), pg.IPv4Address('192.168.3.' + str(i+1),'255.255.255.0'))
	iface_client.bandwidth = 10000
	link_clients_router.addInterface(iface_client)


# Link between webserver and router 3
link_web = request.Link('link-web')
link_web.Site('Site 1')
# set up webserver
node_webserver = request.XenVM('webserver')
node_webserver.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
node_webserver.Site('Site 1')
node_webserver.ram = 4096
node_webserver.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/webserver-install.sh"))
iface_webserver = node_webserver.addInterface('interface-webserver', pg.IPv4Address('192.168.2.200','255.255.255.0'))
iface_webserver.bandwidth = 10000
link_web.addInterface(iface_webserver)


link_tor = request.Link('link-tor')
link_tor.Site('Site 1')
# Node directoryserver
for i in range(params.n_dir):
	# set up directory servers
	node_dir = request.XenVM('dir' + str(i+1))
	node_dir.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
	node_dir.Site('Site 1')
	node_dir.ram = 4096
	node_dir.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/dir-install.sh"))
	iface_dir = node_dir.addInterface('interface-dir-'  + str(i+1), pg.IPv4Address('192.168.1.' + str(i+1),'255.255.255.0'))
	iface_dir.bandwidth = 10000
	link_tor.addInterface(iface_dir)

# set up relay nodes
for i in range(params.n_relay):
	node_relay = request.XenVM('relay' + str(i+1))
	node_relay.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
	node_relay.Site('Site 1')
	node_relay.ram = 4096
	node_relay.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/relay-install.sh"))
	iface_relay = node_relay.addInterface('interface-relay-' + str(i+1), pg.IPv4Address('192.168.1.' + str(i+100),'255.255.255.0'))
	iface_relay.bandwidth = 10000
	link_tor.addInterface(iface_relay)

# Link between routers
link_r = request.Link('link-r')
link_r.Site('Site 1')


# Node router-1
node_router_1 = request.XenVM('router-1')
node_router_1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
node_router_1.Site('Site 1')
iface_router1 = node_router_1.addInterface('interface-1', pg.IPv4Address('192.168.3.254','255.255.255.0'))
iface_router1.bandwidth = 10000
link_clients_router.addInterface(iface_router1)
iface_r1 = node_router_1.addInterface('interface-router1', pg.IPv4Address('192.168.10.1','255.255.255.0'))
iface_r1.bandwidth = 10000
link_r.addInterface(iface_r1)

# Node router-2
node_router_2 = request.XenVM('router-2')
node_router_2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
node_router_2.Site('Site 1')
iface_router2 = node_router_2.addInterface('interface-3', pg.IPv4Address('192.168.1.254','255.255.255.0'))
iface_router2.bandwidth = 10000
link_tor.addInterface(iface_router2)
iface_r2 = node_router_2.addInterface('interface-router2', pg.IPv4Address('192.168.10.2','255.255.255.0'))
iface_r2.bandwidth = 10000
link_r.addInterface(iface_r2)

# Node router-3
node_router_3 = request.XenVM('router-3')
node_router_3.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
node_router_3.Site('Site 1')
iface_r3 = node_router_3.addInterface('interface-router3', pg.IPv4Address('192.168.10.3','255.255.255.0'))
iface_r3.bandwidth = 10000
link_r.addInterface(iface_r3)
iface_r3_web  = node_router_3.addInterface('interface-r3-web', pg.IPv4Address('192.168.2.1','255.255.255.0'))
iface_r3_web.bandwidth = 10000
link_web.addInterface(iface_r3_web)



# Print the generated rspec
pc.printRequestRSpec(request)
