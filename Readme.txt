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
7.) Show port forwarding config - reads the list of NAT Networks and configures rules in each network
8.) Generate / update port forwarding ssh config
    a.)removes all rules previously created by the application
    b.)creates rules for running VMs that are in the NAT Networks and have guest additions installed (can see IP).
    c.)generates vmgr_config file in .ssh folder (add "Include ~/.ssh/vmgr_config" as a first line in your ssh config file)
9.) Copy existing vmgr_config file and replaces localhost IP with your server IP so the config can be used on other hosts
10.) Generate / update configs for RDP sessions to access Windows servers