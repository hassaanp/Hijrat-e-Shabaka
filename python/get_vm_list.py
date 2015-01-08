import sys
import json
#import logging
from neutronclient.neutron import client
from novaclient.client import Client


USERNAME=sys.argv[1]
PASSWORD=sys.argv[2]
TENANT='admin'
VERSION='2.0'
AUTH_URL='http://'+sys.argv[3]+':5000/v2.0'
#logging.basicConfig(level=logging.DEBUG)
nova = Client('2', USERNAME, PASSWORD, TENANT, AUTH_URL)
neutron = client.Client(VERSION, username=USERNAME, password=PASSWORD, tenant_name=TENANT, auth_url=AUTH_URL)
neutron.format = 'json'
#print "RUN DAMMIT!"
servers=nova.servers.list()
#netlist=neutron.networks.list()
array_to_return = []
for serv in reversed(servers):
	name = serv.name
	net = json.dumps(serv.networks)
	net = net.split('"')[3]
	print json.dumps({'title': name, 'ip': net}) 
	
