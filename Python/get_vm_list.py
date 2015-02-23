import sys
import simplejson
import json
#import logging
#from neutronclient.neutron import client
from novaclient.client import Client
API_is_correct = True
if 'network_api_class = nova.network.neutronv2.api.API' in open('/etc/nova/nova.conf').read():
	API_is_correct = False
else:
	API_is_correct = True

USERNAME=sys.argv[1]
PASSWORD=sys.argv[2]
TENANT=sys.argv[3]
VERSION='2.0'
AUTH_URL='http://'+sys.argv[4]+':5000/v2.0'
try:
	nova = Client('2', USERNAME, PASSWORD, TENANT, AUTH_URL)
	servers=nova.servers.list()
	found = True
except:
	print json.dumps({'fail': 'failed!'})
	found = False
if found == True and API_is_correct == True:
	array_to_return = []
	f = open('backup_vmlist.txt','w')
	for serv in reversed(servers):
		name = serv.name
		net = json.dumps(serv.networks)
		net = net.split('"')[3]
		simplejson.dump([name,net],f)
		print json.dumps({'title': name, 'ip': net})
	f.close()
else:
	print json.dumps({'fail': 'wrongapi!'})
