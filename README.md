Migration
=========
Nova-Neutron migration

Guide
==============
Create an environment on nova-net using the following steps:
1. First make following changes to the local.conf file
[[local|localrc]]
enable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service q-neutron
enable_service tempest

2. Run stack.sh

3. When the stack has been successfully created - make the following changes in the nova.conf file:
Replace following lines:
-------------------------
vif_plugging_timeout = 300
vif_plugging_is_fatal = True
linuxnet_interface_driver =
security_group_api = neutron
network_api_class = nova.network.neutronv2.api.API
firewall_driver = nova.virt.firewall.NoopFirewallDriver
--------------------------
by:
--------------------------
flat_interface = eth0
flat_network_bridge = br100
vlan_interface = eth0
public_interface = br100
network_manager = nova.network.manager.FlatDHCPManager
network_api_class = nova.network.api.API
firewall_driver = nova.virt.libvirt.firewall.IptablesFirewallDriver
--------------------------

4. Restart n-api, n-cpu, n-net services
5. Create some networks using nova-net:
nova net-create <name> <cidr>
6. Boot several VMs on the networks you just created
nova boot --flavor <flavor id> --image <image-id> --nic net-id=<network id> <vm name>
7. Once the VMs are up and running, run the automate.py script using: python automate.py
