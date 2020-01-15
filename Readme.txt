Manage VMs on the server

Assumptions for ssh and rdp configs:
* Network is NAT Network

Main MENU

1.) List all VMs, their status and IPs
2.) List Running VMs and their IP
3.) Start specific VMs
4.) Start specific VMs headless
5.) Stop specific VMs - nicely
6.) Stop specific VMs - hard
7.) Show port forwarding config - reads the list of NAT Networks configure and rules in each network
8.) Generate / update port forwarding config - removes all rules previously created by the application and creates rules for running VMs that are in the NAT Networks and have guest additions installed (can see IP).
9.) Update ssh config file on the server for accessing VMs from outside the NAT network
10.) Generate / update configs for RDP sessions to access Windows servers from outside NAT network