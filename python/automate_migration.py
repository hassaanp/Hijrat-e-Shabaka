import subprocess
import sys
import os
import time
import json
from neutronclient.neutron import client
from novaclient.client import Client

USERNAME=sys.argv[1]
PASSWORD=sys.argv[2]
TENANT=sys.argv[3]
VERSION='2.0'
AUTH_URL='http://'+sys.argv[4]+':5000/v2.0'


nova = Client('2', USERNAME, PASSWORD, TENANT, AUTH_URL)
neutron = client.Client(VERSION, username=USERNAME, password=PASSWORD, tenant_name=TENANT, auth_url=AUTH_URL)
neutron.format = 'json'

servers=nova.servers.list()
netlist=nova.networks.list()


selectedlist=sys.argv[5]
selectedlist=selectedlist.replace('<li name=\"mig1\" id=\"mig1\">','')
selectedlist=selectedlist.replace('</li>',' ')
selectedlist1 = selectedlist.split(' ')
selectedlist1.pop()

svmlist=selectedlist1[::2]
snetlist=selectedlist1[1::2]


f=open('f1.txt','w')
f.write(sys.argv[4])
f.close()

#Making changes in nova.conf for compute to use neutron for networking
x1 = open('/home/hassaan/novaconf.txt').read().splitlines()
x2 = open('/etc/nova/nova.conf').read().splitlines()
del x2[0:9]
x = x1+x2
f=open('/etc/nova/nova.conf','w')
for ele in x:
    f.write(ele+'\n')
 
f.close()
#print "nova.conf file modded"
os.system("kill -9 `ps aux | grep -v grep | grep nova-network | awk '{print $2}'`")
os.system('screen -S stack -p n-net -X stuff "/usr/local/bin/nova-network --config-file /etc/nova/nova.conf\n"')



os.system("kill -9 `ps aux | grep -v grep | grep nova-api | awk '{print $2}'`")
os.system('screen -S stack -p n-api -X stuff "/usr/local/bin/nova-api\n"')

os.system("kill -9 `ps aux | grep -v grep | grep nova-compute | awk '{print $2}'`")
cmd ="screen -S stack -p n-cpu -X stuff "+ '"sg libvirtd '+"'/usr/local/bin/nova-compute --config-file /etc/nova/nova.conf'"+'\n"'
os.system(cmd)
time.sleep(10)

ports = json.loads(json.dumps(neutron.list_ports()))
#cloning networks in neutron and then creating valid subnet
for net in reversed(netlist):
    
    netw=neutron.create_network( { 'network' : { 'name' : net.label, 'admin_state_up': True } } )
    net_dict = netw['network']
    network_id = net_dict['id']
    body_create_subnet = {'subnets': [{'ip_version': 4, 'network_id': network_id,'cidr': net.cidr}]}
    subnet = neutron.create_subnet(body=body_create_subnet)
    for serv in reversed(servers):
	try:	
	    q =str(serv.networks[net.label])
            found=True
            ip = json.dumps(serv.networks)
            ip = ip.split('"')[3]
	    if ip in snetlist:
                found=True
            else:
                found=False
	    
	except:
	    found=False
	if found==True:
            ip = json.dumps(serv.networks)
            ip = ip.split('"')[3]
	    body_value = {"port":{"admin_state_up":True,"network_id":network_id,"fixed_ips": [{"ip_address": ip}]}}
            try:
                response = neutron.create_port(body=body_value)
                serv.interface_detach(net.id)
                serv.interface_attach(response["port"]["id"],None,None)
                serv.reboot(reboot_type='HARD')
            except:
                body_value = {"port":{"admin_state_up":True,"network_id":network_id}}
                response = neutron.create_port(body=body_value)
                serv.interface_detach(net.id)
                serv.interface_attach(response["port"]["id"],None,None)
                serv.reboot(reboot_type='HARD')
