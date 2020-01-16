import subprocess
import re
from pathlib import Path
import os


# virtualbox basic commands
list_vms_cmd = 'vboxmanage list vms --sorted'
list_running_cmd = 'vboxmanage list runningvms --sorted'
list_vmdetails_cmd = 'vboxmanage guestproperty enumerate '
list_natnets_cmd = 'vboxmanage list natnets'
natnet_rule_cmd = 'vboxmanage natnetwork modify --netname '
start_vm_cmd = 'vboxmanage startvm '
headless = ' --type headless'
control_vm_cmd = 'vboxmanage controlvm '
stop_vm_nicely_cmd = ' acpipowerbutton'
stop_vm_hard_cmd = ' poweroff'
showvminfo_cmd = 'vboxmanage showvminfo '
grep_NIC_1_cmd = ' |grep "NIC 1"'
grep_OS_type_cmd = ' |grep "Guest OS"'


# variables initialization
output_lines = []
vm_list = []
power_off_list = []
running_vm_list = []
nat_forwarding_rules_all = []
nat_networks = []



# list all running VMs configured in Virtualbox
def vmlist():
    # using global variable and clearing the list
    global vm_list
    vm_list = []
    # loading list_vms_cmd output to the list
    vmlist_output = output_to_lines(list_vms_cmd)
    # extracting hostnames and adding them to the vm_list list
    for line_number in range(len(vmlist_output)):
        line_content = vmlist_output[line_number]
        capture_name = re.findall(r'"(.*?)"', line_content)
        vm_list.append(capture_name[0])
    return vm_list


# list all VMs configured in Virtualbox
def runningvmlist():
    # using global variable and clearing the list
    global running_vm_list
    running_vm_list = []
    # loading list_vms_cmd output to the list
    running_vm_list_output = output_to_lines(list_running_cmd)
    # extracting hostnames and adding them to the vm_list list
    for line_number in range(len(running_vm_list_output)):
        line_content = running_vm_list_output[line_number]
        capture_name = re.findall(r'"(.*?)"', line_content)
        running_vm_list.append(capture_name[0])
    return running_vm_list


def offvmlist():
    global power_off_list
    global running_vm_list
    global vm_list
    power_off_list = []
    vmlist()
    runningvmlist()
    for vm in vm_list:
        if vm not in running_vm_list:
            power_off_list.append(vm)

    return power_off_list


def get_ip(vm_name):
    command = list_vmdetails_cmd + vm_name
    details_list = output_to_lines(command)
    for lnnr in range(len(details_list)):
        line_content = details_list[lnnr]
        if line_content.__contains__("V4/IP"):
            ip_addr = line_content.split()[3][:-1]
            return ip_addr
        else:
            ip_addr = "Check g additions"
    return ip_addr


# function that can run any command and put output in to list one line per list item

def output_to_lines(command):
    global output_lines
    output_lines = []
    result = subprocess.getoutput(command)
    length = len(result)
    possition = 0
    output_lines = []
    line_content = ''
    for char in result:
        possition = possition + 1
        if char != '\n' and possition != length:
            line_content = line_content + str(char)
        else:
            if possition != length:
                output_lines.append(line_content)
                line_content = ''
            else:
                line_content = line_content + str(result[-1])
                output_lines.append(line_content)
    return output_lines


def list_all_vms():
    vmlist()
    for vmnumber in range(len(vm_list)):
        name = vm_list[vmnumber]
        runningvmlist()
        if name in running_vm_list:
            ip_addr = get_ip(name)
        else:
            ip_addr = "Powered Down"
        if len(name) < 5:
            tab = "\t\t\t"
        elif 5 < len(name) < 10:
            tab = "\t\t"
        elif len(name) >= 10:
            tab = "\t"
        print(vmnumber, "\t", name, tab, ip_addr)


def list_running_vms():
    runningvmlist()
    for vmnumber in range(len(running_vm_list)):
        name = running_vm_list[vmnumber]
        ip_addr = get_ip(name)
        if len(name) < 5:
            tab = "\t\t\t"
        elif 5 < len(name) < 10:
            tab = "\t\t"
        elif len(name) >= 10:
            tab = "\t"
        print(vmnumber, "\t", name, tab, ip_addr)


def list_offline_vms():
    offvmlist()
    for vmnumber in range(len(power_off_list)):
        print(vmnumber, "\t", power_off_list[vmnumber])


def start_vm():
    list_offline_vms()
    vmnumber = input("\nPick VM to Start(q to cancel and go to Main Menu): ")
    if vmnumber == 'q':
        main_menu()
    else:
        vmnumber = int(vmnumber)
        vmtostart = power_off_list[vmnumber]
        command = start_vm_cmd + vmtostart
        output_to_lines(command)
        for line in output_lines:
            print(line)


def start_vm_headless():
    list_offline_vms()
    vmnumber = input("\nPick VM to Start(q to cancel and go to Main Menu): ")
    if vmnumber == 'q':
        main_menu()
    else:
        vmnumber = int(vmnumber)
        vmtostart = power_off_list[vmnumber]
        command = start_vm_cmd + vmtostart + headless
        output_to_lines(command)
        for line in output_lines:
            print(line)


def stop_vm_nicely():
    list_running_vms()
    vmnumber = input("\nPick VM to Stop(q to cancel and go to Main Menu): ")
    if vmnumber == 'q':
        main_menu()
    else:
        vmnumber = int(vmnumber)
        vmtostop = running_vm_list[vmnumber]
        command = control_vm_cmd + vmtostop + stop_vm_nicely_cmd
        output_to_lines(command)
        for line in output_lines:
            print(line)


def stop_vm_hard():
    list_running_vms()
    vmnumber = input("\nPick VM to Stop(q to cancel and go to Main Menu): ")
    if vmnumber == 'q':
        main_menu()
    else:
        vmnumber = int(vmnumber)
        vmtostop = running_vm_list[vmnumber]
        command = control_vm_cmd + vmtostop + stop_vm_hard_cmd
        output_to_lines(command)
        for line in output_lines:
            print(line)


def get_port_fwd_info():
    lines = output_to_lines(list_natnets_cmd)
    global nat_networks
    global nat_forwarding_rules_all
    nat_networks.clear()
    nat_forwarding_rules_all.clear()
    rules_in_nat_network = []
    for line in range(len(lines)):
        content = lines[line]
        if content.startswith('NetworkName'):
            nat_networks.append(content[16:])
        elif content.startswith('Port-forwarding'):
            line = line + 1
            for line in range(line, len(lines)):
                content = lines[line]
                if content.startswith('loopback'):
                    nat_forwarding_rules_all.append(rules_in_nat_network)
                    rules_in_nat_network = []
                    break
                else:
                    rules_in_nat_network.append(content[8:])
    return nat_networks, nat_forwarding_rules_all


def list_port_fwd():
    get_port_fwd_info()
    for net in range(len(nat_networks)):
        net_name = nat_networks[net]
        print("\nNetwork: ", net_name)
        print('Rules:')
        rules = nat_forwarding_rules_all[net]
        for rule in rules:
            print(rule)


def get_vm_nat_network(vmname):
    command = showvminfo_cmd + vmname + grep_NIC_1_cmd
    line = output_to_lines(command)
    content = line[0]
    if content.__contains__("NAT Network"):
        words = content.split('\'')
        vm_nat_network = words[1]
        return vm_nat_network
    else:
        vm_nat_network = "Check guest network settings"
        return vm_nat_network


def check_if_windows(vmname):
    command = showvminfo_cmd + vmname + grep_OS_type_cmd
    line = output_to_lines(command)
    content = line[0]
    if content.__contains__("Windows"):
        return True
    else:
        return False


def create_nat_rule(vmname):
    ip = get_ip(vmname)
    if ip == "Check g additions":
        print("Skipping ", vmname, " - Don't see IP - check guest additions")
    else:
        ip_last = ip.split(".")[3]
        nat_name = get_vm_nat_network(vmname)
        if nat_name == "Check guest network settings":
            print("Skipping ", vmname, nat_name)
        else:
            if check_if_windows(vmname):
                dest_port = '3389'
                if int(ip_last) < 11:
                    port_nr = int(ip_last) + 400
                    rem_port = str(port_nr) + '89'
                else:
                    rem_port = ip_last + '89'
            else:
                dest_port = '22'
                if int(ip_last) < 11:
                    port_nr = int(ip_last) + 400
                    rem_port = str(port_nr) + '22'
                else:
                    rem_port = ip_last + '22'
            name = vmname + '_vmgr'
            command = natnet_rule_cmd + nat_name + ' --port-forward-4 "' + name + ':tcp:[]:' + rem_port + ':[' + ip + ']:' + dest_port + '"'
            output_to_lines(command)
            print('Created a rule for ', vmname)


def generate_nat_rules():
    runningvmlist()
    for vmname in runningvmlist():
        create_nat_rule(vmname)


def nat_network_rule_cleanup():
    get_port_fwd_info()
    for net in nat_networks:
        rules = nat_forwarding_rules_all[nat_networks.index(net)]
        for rule in rules:
            words = rule.split(':')
            rule_name = str(words[0])
            if rule_name.__contains__('_vmgr'):
                command = natnet_rule_cmd + net + ' --port-forward-4 delete ' + rule_name
                output_to_lines(command)


def ask_for_username(vmname):
    message = 'Enter Username for ' + vmname + ': '
    username = input(message)
    return username


def ask_for_ssh_key(vmname):
    message = 'Enter cert for ' + vmname + '(hit enter to skip cert for this host): '
    cert = input(message)
    return cert


def add_ssh_config_entry(vmname, port, username, cert):
    global vmgr_config_file
    vmgr_config_file.write('\nHost ' + vmname + '\n')
    vmgr_config_file.write('  Hostname 127.0.0.1\n')
    vmgr_config_file.write('  Port ' + port + '\n')
    if username == 'ask':
        username = ask_for_username(vmname)
        vmgr_config_file.write('  User ' + username + '\n')
    else:
        vmgr_config_file.write('  User ' + username + '\n')
    if cert != 'no':
        if cert == 'ask':
            cert = ask_for_ssh_key(vmname)
            if cert:
                vmgr_config_file.write('  IdentityFile ' + cert + '\n')
        else:
            vmgr_config_file.write('  IdentityFile ' + cert + '\n')


def generate_vmgr_config_file():
    global vmgr_config_file
    home = str(Path.home())
    path = home + '/.ssh/vmgr_config'
    vmgr_config_file = (open(path, "w"))
    get_port_fwd_info()
    same_user = input('Use same username for all hosts?  y/n:  ')
    if same_user == 'y':
        username = input('Enter username for all hosts: ')
    use_cert = input('Use certificates to connect to hosts?  y/n:  ')
    if use_cert == 'y':
        same_cert = input('Use same certificate for all hosts?  y/n:  ')
        if same_cert == 'y':
            cert = input('Enter cert for all hosts: ')

    for net in range(len(nat_networks)):
        rules = nat_forwarding_rules_all[net]
        for rule in rules:
            rule_content = rule.split(':')
            dest_port = rule_content[-1]
            rule_name = rule_content[0]
            in_port = rule_content[3]
            vmname = rule_name[:-5]
            if rule_name[-5:] == '_vmgr' and dest_port == '22':

                if same_user == 'n':
                    username = 'ask'

                if use_cert == 'n':
                    cert = 'no'

                if use_cert == 'y' and same_cert == 'n':
                    cert = 'ask'

                add_ssh_config_entry(vmname, in_port, username, cert)

    vmgr_config_file.close()


def generate_vmgr_rdp_files():
    get_port_fwd_info()
    home = str(Path.home())
    paths = ['/.local/share/remmina/', '/.ssh/RDP_Mac/', '/.ssh/RDP_Win/']
    for folder in paths:
        path = home + folder
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            file_cleanup(path)

    ip = str(input('\nEnter hypervisor IP: '))
    same_user = input('Use same username for all hosts?  y/n:  ')
    if same_user == 'y':
        username = input('Enter username for all hosts: ')

    for net in range(len(nat_networks)):
        rules = nat_forwarding_rules_all[net]
        for rule in rules:
            rule_content = rule.split(':')
            dest_port = rule_content[-1]
            rule_name = rule_content[0]
            port = rule_content[3]
            vmname = rule_name[:-5]
            if rule_name[-5:] == '_vmgr' and dest_port == '3389':
                if same_user == 'n':
                    username = ask_for_username(vmname)

                generate_remmina_rdp_file(vmname, ip, port, username)
                generate_mac_rdp_file(vmname, ip, port, username)
                generate_win_rdp_file(vmname, ip, port, username)



def file_cleanup(path):
    list_of_files = os.listdir(path)
    for file in list_of_files:
        if file.__contains__("_vmgr"):
            file_to_remove = path + file
            os.remove(file_to_remove)


def generate_remmina_rdp_file(vmname, ip, port, username):
    home = str(Path.home())
    path = home + '/.local/share/remmina/'

    file = path + vmname + '_vmgr.remmina'
    remmina_rdp_config_file = open(file, "w")

    remmina_rdp_config_file.write("[remmina]\n")
    remmina_rdp_config_file.write("relax-order-checks=0\n")

    remmina_rdp_config_file.write("name=" + vmname + "_vmgr\n")

    remmina_rdp_config_file.write("resolution_mode=2\n")
    remmina_rdp_config_file.write("gwtransp=http\n")
    remmina_rdp_config_file.write("serialdriver=\n")
    remmina_rdp_config_file.write("password=.\n")
    remmina_rdp_config_file.write("gateway_domain=\n")
    remmina_rdp_config_file.write("quality=0\n")
    remmina_rdp_config_file.write("shareserial=0\n")
    remmina_rdp_config_file.write("sound=on\n")
    remmina_rdp_config_file.write("enableproxy=0\n")
    remmina_rdp_config_file.write("microphone=0\n")
    remmina_rdp_config_file.write("precommand=\n")
    remmina_rdp_config_file.write("sharefolder=\n")
    remmina_rdp_config_file.write("ssh_privatekey=\n")
    remmina_rdp_config_file.write("cert_ignore=0\n")
    remmina_rdp_config_file.write("ssh_enabled=0\n")
    remmina_rdp_config_file.write("domain=\n")
    remmina_rdp_config_file.write("disable_fastpath=0\n")
    remmina_rdp_config_file.write("sharesmartcard=0\n")
    remmina_rdp_config_file.write("disableautoreconnect=0\n")
    remmina_rdp_config_file.write("ssh_server=\n")
    remmina_rdp_config_file.write("gateway_server=\n")
    remmina_rdp_config_file.write("printername=\n")
    remmina_rdp_config_file.write("ssh_username=\n")
    remmina_rdp_config_file.write("resolution_width=0\n")
    remmina_rdp_config_file.write("ssh_charset=\n")
    remmina_rdp_config_file.write("ssh_auth=0\n")
    remmina_rdp_config_file.write("ssh_password=\n")
    remmina_rdp_config_file.write("shareprinter=0\n")
    remmina_rdp_config_file.write("gateway_username=\n")
    remmina_rdp_config_file.write("postcommand=\n")
    remmina_rdp_config_file.write("security=\n")

    remmina_rdp_config_file.write("server=" + ip + ":" + port + "\n")

    remmina_rdp_config_file.write("gateway_password=\n")
    remmina_rdp_config_file.write("glyph-cache=0\n")
    remmina_rdp_config_file.write("ssh_loopback=0\n")
    remmina_rdp_config_file.write("console=0\n")
    remmina_rdp_config_file.write("parallelname=\n")
    remmina_rdp_config_file.write("smartcardname=ls\n")
    remmina_rdp_config_file.write("disableclipboard=0\n")
    remmina_rdp_config_file.write("resolution_height=0\n")
    remmina_rdp_config_file.write("execpath=\n")
    remmina_rdp_config_file.write("parallelpath=\n")
    remmina_rdp_config_file.write("group=vmgr\n")
    remmina_rdp_config_file.write("shareparallel=0\n")
    remmina_rdp_config_file.write("exec=\n")
    remmina_rdp_config_file.write("disablepasswordstoring=0\n")
    remmina_rdp_config_file.write("colordepth=64\n")
    remmina_rdp_config_file.write("serialname=\n")
    remmina_rdp_config_file.write("loadbalanceinfo=\n")
    remmina_rdp_config_file.write("clientname=\n")
    remmina_rdp_config_file.write("gateway_usage=0\n")
    remmina_rdp_config_file.write("serialpermissive=0\n")
    remmina_rdp_config_file.write("protocol=RDP\n")

    remmina_rdp_config_file.write("username=" + username + "\n")

    remmina_rdp_config_file.write("printerdriver=\n")
    remmina_rdp_config_file.write("serialpath=\n")
    remmina_rdp_config_file.write("window_height=843\n")
    remmina_rdp_config_file.write("viewmode=1\n")
    remmina_rdp_config_file.write("window_maximize=0\n")
    remmina_rdp_config_file.write("window_width=1432\n")
    remmina_rdp_config_file.write("scale=2\n")

    remmina_rdp_config_file.close()


def generate_mac_rdp_file(vmname, ip, port, username):
    home = str(Path.home())
    path = home + '/.ssh/RDP_Mac/'

    file = path + vmname + '_vmgr.rdp'
    mac_rdp_config_file = open(file, "w")

    mac_rdp_config_file.write("gatewaybrokeringtype:i:0\n")
    mac_rdp_config_file.write("use redirection server name:i:0\n")
    mac_rdp_config_file.write("disable themes:i:0\n")
    mac_rdp_config_file.write("disable cursor setting:i:0\n")
    mac_rdp_config_file.write("disable menu anims:i:1\n")
    mac_rdp_config_file.write("remoteapplicationcmdline:s:\n")
    mac_rdp_config_file.write("redirected video capture encoding quality:i:0\n")
    mac_rdp_config_file.write("audiocapturemode:i:0\n")
    mac_rdp_config_file.write("prompt for credentials on client:i:0\n")
    mac_rdp_config_file.write("remoteapplicationprogram:s:\n")
    mac_rdp_config_file.write("gatewayusagemethod:i:2\n")
    mac_rdp_config_file.write("screen mode id:i:1\n")
    mac_rdp_config_file.write("use multimon:i:0\n")
    mac_rdp_config_file.write("authentication level:i:2\n")
    mac_rdp_config_file.write("desktopwidth:i:0\n")
    mac_rdp_config_file.write("desktopheight:i:0\n")
    mac_rdp_config_file.write("redirectclipboard:i:1\n")
    mac_rdp_config_file.write("loadbalanceinfo:s:\n")
    mac_rdp_config_file.write("enablecredsspsupport:i:1\n")
    mac_rdp_config_file.write("promptcredentialonce:i:0\n")
    mac_rdp_config_file.write("redirectprinters:i:0\n")
    mac_rdp_config_file.write("autoreconnection enabled:i:1\n")
    mac_rdp_config_file.write("administrative session:i:0\n")
    mac_rdp_config_file.write("redirectsmartcards:i:0\n")
    mac_rdp_config_file.write("authoring tool:s:\n")
    mac_rdp_config_file.write("alternate shell:s:\n")
    mac_rdp_config_file.write("remoteapplicationmode:i:0\n")
    mac_rdp_config_file.write("disable full window drag:i:1\n")
    mac_rdp_config_file.write("gatewayusername:s:\n")
    mac_rdp_config_file.write("shell working directory:s:\n")
    mac_rdp_config_file.write("audiomode:i:0\n")
    mac_rdp_config_file.write("remoteapplicationappid:s:\n")

    mac_rdp_config_file.write("username:s:" + username + "\n")

    mac_rdp_config_file.write("allow font smoothing:i:1\n")
    mac_rdp_config_file.write("connect to console:i:0\n")
    mac_rdp_config_file.write("gatewayhostname:s:\n")
    mac_rdp_config_file.write("camerastoredirect:s:\n")
    mac_rdp_config_file.write("drivestoredirect:s:*\n")
    mac_rdp_config_file.write("session bpp:i:32\n")
    mac_rdp_config_file.write("disable wallpaper:i:0\n")

    mac_rdp_config_file.write("full address:s:" + ip + ":" + port + "\n")

    mac_rdp_config_file.write("gatewayaccesstoken:s:\n")

    mac_rdp_config_file.close()


def generate_win_rdp_file(vmname, ip, port, username):
    home = str(Path.home())
    path = home + '/.ssh/RDP_Win/'

    file = path + vmname + '_vmgr.rdp'
    win_rdp_config_file = open(file,"w")

    win_rdp_config_file.write("screen mode id:i:1\n")
    win_rdp_config_file.write("use multimon:i:0\n")
    win_rdp_config_file.write("desktopwidth:i:1280\n")
    win_rdp_config_file.write("desktopheight:i:720\n")
    win_rdp_config_file.write("session bpp:i:24\n")
    win_rdp_config_file.write("winposstr:s:0,3,0,0,800,600\n")
    win_rdp_config_file.write("compression:i:1\n")
    win_rdp_config_file.write("keyboardhook:i:2\n")
    win_rdp_config_file.write("audiocapturemode:i:0\n")
    win_rdp_config_file.write("videoplaybackmode:i:1\n")
    win_rdp_config_file.write("connection type:i:7\n")
    win_rdp_config_file.write("networkautodetect:i:1\n")
    win_rdp_config_file.write("bandwidthautodetect:i:1\n")
    win_rdp_config_file.write("displayconnectionbar:i:1\n")
    win_rdp_config_file.write("enableworkspacereconnect:i:0\n")
    win_rdp_config_file.write("disable wallpaper:i:0\n")
    win_rdp_config_file.write("allow font smoothing:i:0\n")
    win_rdp_config_file.write("allow desktop composition:i:0\n")
    win_rdp_config_file.write("disable full window drag:i:1\n")
    win_rdp_config_file.write("disable menu anims:i:1\n")
    win_rdp_config_file.write("disable themes:i:0\n")
    win_rdp_config_file.write("disable cursor setting:i:0\n")
    win_rdp_config_file.write("bitmapcachepersistenable:i:1\n")

    win_rdp_config_file.write("full address:s:" + ip + ":" + port + "\n")

    win_rdp_config_file.write("audiomode:i:0\n")
    win_rdp_config_file.write("redirectprinters:i:1\n")
    win_rdp_config_file.write("redirectcomports:i:0\n")
    win_rdp_config_file.write("redirectsmartcards:i:1\n")
    win_rdp_config_file.write("redirectclipboard:i:1\n")
    win_rdp_config_file.write("redirectposdevices:i:0\n")
    win_rdp_config_file.write("autoreconnection enabled:i:1\n")
    win_rdp_config_file.write("authentication level:i:2\n")
    win_rdp_config_file.write("prompt for credentials:i:0\n")
    win_rdp_config_file.write("negotiate security layer:i:1\n")
    win_rdp_config_file.write("remoteapplicationmode:i:0\n")
    win_rdp_config_file.write("alternate shell:s:\n")
    win_rdp_config_file.write("shell working directory:s:\n")
    win_rdp_config_file.write("gatewayhostname:s:\n")
    win_rdp_config_file.write("gatewayusagemethod:i:4\n")
    win_rdp_config_file.write("gatewaycredentialssource:i:4\n")
    win_rdp_config_file.write("gatewayprofileusagemethod:i:0\n")
    win_rdp_config_file.write("promptcredentialonce:i:0\n")
    win_rdp_config_file.write("gatewaybrokeringtype:i:0\n")
    win_rdp_config_file.write("use redirection server name:i:0\n")
    win_rdp_config_file.write("rdgiskdcproxy:i:0\n")
    win_rdp_config_file.write("kdcproxyname:s:\n")

    win_rdp_config_file.write("username:s:" + username + "\n")

    win_rdp_config_file.write("drivestoredirect:s:\n")

    win_rdp_config_file.close()


def generate_vmgr_config_IP_file():
    ip = str(input('Enter hypervisor IP that can be used by other hosts on your network to connect to VMs: '))
    global vmgr_config_file
    home = str(Path.home())
    source = home + '/.ssh/vmgr_config'
    dest = home + '/.ssh/vmgr_config_IP'
    vmgr_config_IP_file = open(dest,'w')
    with open(source) as f:
        lines = f.readlines()
    for line in lines:
        if line.__contains__("127.0.0.1"):
            new_line = line.replace('127.0.0.1', ip)
            vmgr_config_IP_file.write(new_line)
        else:
            vmgr_config_IP_file.write(line)

    vmgr_config_IP_file.close()




def mm_option_1():
    list_all_vms()
    input("\nPress enter to go back to main menu...")
    main_menu()


def mm_option_2():
    list_running_vms()
    input("\nPress enter to go back to main menu...")
    main_menu()


def mm_option_3():
    start_vm()
    print("\nWhat you want to do next:")
    print("1.) Start another VM")
    print("q.) Go back to main menu")
    option = input("\nPick and option: ")
    if option == "1":
        mm_option_3()
    if option == "q":
        main_menu()


def mm_option_4():
    start_vm_headless()
    print("\nWhat you want to do next:")
    print("1.) Start another VM")
    print("q.) Go back to main menu")
    option = input("\nPick and option: ")
    if option == "1":
        mm_option_4()
    if option == "q":
        main_menu()


def mm_option_5():
    stop_vm_nicely()
    print("\nWhat you want to do next:")
    print("1.) Stop another VM")
    print("q.) Go back to main menu")
    option = input("\nPick and option: ")
    if option == "1":
        mm_option_5()
    if option == "q":
        main_menu()


def mm_option_6():
    stop_vm_hard()
    print("\nWhat you want to do next:")
    print("1.) Stop another VM")
    print("q.) Go back to main menu")
    option = input("\nPick and option: ")
    if option == "1":
        mm_option_6()
    if option == "q":
        main_menu()


def mm_option_7():
    list_port_fwd()
    input("\nPress enter to go back to main menu...")
    main_menu()


def mm_option_8():
    nat_network_rule_cleanup()
    generate_nat_rules()
    generate_vmgr_config_file()
    input("\nPress enter to go back to main menu...")
    main_menu()


def mm_option_9():
    generate_vmgr_config_IP_file()
    input("\nPress enter to go back to main menu...")
    main_menu()


def mm_option_10():
    generate_nat_rules()
    generate_vmgr_rdp_files()
    input("\nPress enter to go back to main menu...")
    main_menu()


def main_menu():
    print("\nPick and action:")
    print("1.) List all VMs, their status and IPs")
    print("2.) List Running VMs")
    print("3.) Start specific VMs")
    print("4.) Start specific VMs - headless")
    print("5.) Stop specific VMs - nicely")
    print("6.) Stop specific VMs - hard")
    print("7.) Show port forwarding config")
    print("8.) Generate / update port forwarding ssh vmgr_config file")
    print("9.) Copy existing vmgr_config and replace localhost with hypervisor IP - use on other hosts on the network")
    print("10.) Generate / update configs for RDP sessions to access Windows servers\n")
    print('Press "q" to quit')

    option = input("Pick and option: ")
    if option == "1":
        mm_option_1()
    elif option == "2":
        mm_option_2()
    elif option == "3":
        mm_option_3()
    elif option == "4":
        mm_option_4()
    elif option == "5":
        mm_option_5()
    elif option == "6":
        mm_option_6()
    elif option == "7":
        mm_option_7()
    elif option == "8":
        mm_option_8()
    elif option == "9":
        mm_option_9()
    elif option == "10":
        mm_option_10()

    elif option == "q":
        quit()
    else:
        print("Invalid option selected - try again")
        main_menu()


main_menu()
