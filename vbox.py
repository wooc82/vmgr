import subprocess
import re
from pathlib import Path


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


# class vboxvm:
#    def __init__(self, name):
#       self.name = name
#        self.IP = IP_addr
#        self.status = onoff


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
                if int(ip_last) < 10:
                    port_nr = int(ip_last) + 400
                    rem_port = str(port_nr) + '89'
                else:
                    rem_port = ip_last + '89'
            else:
                dest_port = '22'
                if int(ip_last) < 10:
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


def ask_for_ssh_username(vmname):
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
        username = ask_for_ssh_username(vmname)
        vmgr_config_file.write('  User ' + username +'\n')
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
    if use_cert =='y':
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
    print("9.) Update ssh config file on the server for accessing VMs from outside the NAT network")
    print("10.) Generate / update configs for RDP sessions to access Windows servers from outside NAT network\n")
    print('Press "q" to quit')

    option = input("Pick and option: ")
    if option == "1":
        mm_option_1()
    if option == "2":
        mm_option_2()
    if option == "3":
        mm_option_3()
    if option == "4":
        mm_option_4()
    if option == "5":
        mm_option_5()
    if option == "6":
        mm_option_6()
    if option == "7":
        mm_option_7()
    if option == "8":
        mm_option_8()

    if option == "q":
        quit()
    else:
        quit()


main_menu()
