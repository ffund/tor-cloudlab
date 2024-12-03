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
pc.defineParameter("cap", "Capacity of each link (kbps)", portal.ParameterType.INTEGER, 10000)

# Get values specified by user during instantiation
params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Link between routers
link_r = request.Link('link-r')

# Link between webserver and router 3
link_web = request.Link('link-web')

# First, set up routers

# Node router1
node_router_1 = request.XenVM('router1')
node_router_1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
iface_r1 = node_router_1.addInterface('interface-router1', pg.IPv4Address('10.10.254.1','255.255.255.0'))
iface_r1.bandwidth = params.cap
link_r.addInterface(iface_r1)
node_router_1.exclusive = True

# Node router2
node_router_2 = request.XenVM('router2')
node_router_2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
iface_r2 = node_router_2.addInterface('interface-router2', pg.IPv4Address('10.10.254.2','255.255.255.0'))
iface_r2.bandwidth = params.cap
link_r.addInterface(iface_r2)
node_router_2.exclusive = True

# Node router3
node_router_3 = request.XenVM('router3')
node_router_3.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
iface_r3 = node_router_3.addInterface('interface-router3', pg.IPv4Address('10.10.254.3','255.255.255.0'))
iface_r3.bandwidth = params.cap
link_r.addInterface(iface_r3)
iface_r3_web  = node_router_3.addInterface('interface-r3-web', pg.IPv4Address('10.10.253.1','255.255.255.0'))
iface_r3_web.bandwidth = params.cap
link_web.addInterface(iface_r3_web)
node_router_3.exclusive = True


# set up webserver
node_webserver = request.XenVM('webserver')
node_webserver.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
node_webserver.ram = 4096
node_webserver.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/webserver-install.sh"))
iface_webserver = node_webserver.addInterface('interface-webserver', pg.IPv4Address('10.10.253.200','255.255.255.0'))
iface_webserver.bandwidth = params.cap
link_web.addInterface(iface_webserver)
node_webserver.exclusive = True

# set up clients!
for i in range(params.n_client):
	# Node client
	node_client = request.XenVM('client' + str(i+1))
	node_client.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
	node_client.ram = 4096
	node_client.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/client-install.sh"))
	iface_client = node_client.addInterface('interface-client-' + str(i+1), pg.IPv4Address('10.10.' + str(200+1+i) + '.' + str(i+1),'255.255.255.0'))
	iface_client.bandwidth = params.cap
	# link between client and router 1
	link_clients_router = request.Link('link-r1-client' + str(i+1))
	link_clients_router.addInterface(iface_client)
	iface_router1 = node_router_1.addInterface('interface-r1-' + str(i+1), pg.IPv4Address('10.10.' + str(200+1+i) + '.254','255.255.255.0'))
	iface_router1.bandwidth = params.cap
	link_clients_router.addInterface(iface_router1)
	node_client.exclusive = True


# Node directoryserver
for i in range(params.n_dir):
	# set up directory servers
	node_dir = request.XenVM('dir' + str(i+1))
	node_dir.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
	node_dir.ram = 4096
	node_dir.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/dir-install.sh"))
	# Link for tor network
	link_tor = request.Link('link-tor-' + str(i+1))
	iface_dir = node_dir.addInterface('interface-dir' + str(i+1), pg.IPv4Address('10.10.' + str(i+1) + '.' + str(i+1),'255.255.255.0'))
	iface_dir.bandwidth = params.cap
	link_tor.addInterface(iface_dir)
	iface_router2 = node_router_2.addInterface('interface-r2-dir' + str(i+1), pg.IPv4Address('10.10.' + str(i+1) + '.254','255.255.255.0'))
	iface_router2.bandwidth = params.cap
	link_tor.addInterface(iface_router2)
	node_dir.exclusive = True
	
# set up relay nodes
for i in range(params.n_relay):
	node_relay = request.XenVM('relay' + str(i+1))
	node_relay.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
	node_relay.ram = 4096
	node_relay.addService(pg.Execute(shell="sh", command="/usr/bin/sudo /bin/bash /local/repository/relay-install.sh"))
	# Link for tor network
	link_tor = request.Link('link-tor-' + str(i+1+100))
	iface_relay = node_relay.addInterface('interface-relay' + str(i+1), pg.IPv4Address('10.10.' + str(i+1+100) + '.' + str(i+1),'255.255.255.0'))
	iface_relay.bandwidth = params.cap
	link_tor.addInterface(iface_relay)
	iface_router2 = node_router_2.addInterface('interface-r2-relay' + str(i+1), pg.IPv4Address('10.10.' + str(i+1+100) + '.254','255.255.255.0'))
	iface_router2.bandwidth = params.cap
	link_tor.addInterface(iface_router2)
	node_relay.exclusive = True

# Print the generated rspec
pc.printRequestRSpec(request)
