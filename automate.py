import logging
from neutronclient.neutron import client
from novaclient.client import Client

USERNAME='admin'
PASSWORD='nomoresecrete'
TENANT='admin'
VERSION='2.0'
AUTH_URL='http://172.19.20.42:5000/v2.0'

logging.basicConfig(level=logging.DEBUG)
nova = Client('2', USERNAME, PASSWORD, TENANT, AUTH_URL)
neutron = client.Client(VERSION, username=USERNAME, password=PASSWORD, tenant_name=TENANT, auth_url=AUTH_URL)
neutron.format = 'json'

servers=nova.servers.list()
netlist=nova.networks.list()

#Making changes in nova.conf for compute to use neutron for networking
x1 = open('novaconf.txt').read().splitlines()
x2 = open('/etc/nova/nova.conf').read().splitlines()
del x2[0:10]
x = x1+x2
f=open('/etc/nova/nova.conf','w')
for ele in x:
    f.write(ele+'\n')

f.close()
print "nova.conf file modded"
true=0
while true != 1:
    Prompt=raw_input("Please restart n-api,n-cpu, q-api and enter 'y': ")
    if Prompt == "y":
	true=1
    else:
        true=0
print "Services restarted successfully, beginning migration"

#cloning networks in neutron and then creating valid subnet
for net in reversed(netlist):
    temp_ip = str(net.cidr)
    temp_ip = temp_ip.split("/")
    netw=neutron.create_network( { 'network' : { 'name' : net.label, 'admin_state_up': True } } )
    net_dict = netw['network']
    network_id = net_dict['id']
    print net.cidr
    print('Network %s created' % network_id)
    body_create_subnet = {'subnets': [{'ip_version': 4, 'network_id': network_id,'cidr': net.cidr}]}
    subnet = neutron.create_subnet(body=body_create_subnet)
    print('Created subnet %s' % subnet)
    for serv in reversed(servers):
	print('In block')
	print net.label	
	try:	
	    q =str(serv.networks[net.label])
	    found=True
	    print('found')
	except:
	    found=False
	print found
	if found==True:
	    print('In subnet loop')
    	    q = q.split("'")
            snet = q[1]
	    checkval.append(snet.split("."))
	    print checkval
	    body_value = {"port":{"admin_state_up":True,"network_id":network_id}}
	    response = neutron.create_port(body=body_value)
	    serv.interface_attach(response["port"]["id"],None,None)	        
	    print('FOUND AND SUBNET CREATED\n')
