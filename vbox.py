import subprocess
import re

# virtualbox basic commands
list_vms_cmd = 'vboxmanage list vms --sorted'
list_running_cmd = 'vboxmanage list runningvms --sorted'
list_vmdetails_cmd = 'vboxmanage guestproperty enumerate '
list_natnets_cmd = 'vboxmanage list natnets'
natnet_rule_cmd = 'vboxmanage natnetwork modify --netname NatNetwork'
start_vm_cmd = 'vboxmanage startvm '
headless = ' --type headless'
control_vm_cmd = 'vboxmanage controlvm '
stop_vm_nicely_cmd = ' acpipowerbutton'
stop_vm_hard_cmd = ' poweroff'


# variables initialization
output_lines = []
vm_list = []
power_off_list = []
running_vm_list = []
#ip_addr = ""
#onoff = ""


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
    output_to_lines(list_natnets_cmd)



    return nat_networks, nat_rules_all

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


def main_menu():
    print("\nPick and action:")
    print("1.) List all VMs, their status and IPs")
    print("2.) List Running VMs")
    print("3.) Start specific VMs")
    print("4.) Start specific VMs - headless")
    print("5.) Stop specific VMs - nicely")
    print("6.) Stop specific VMs - hard")
    print("7.) Show port forwarding config")
    print("8.) Generate / update port forwarding config")
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


    if option == "q":
        quit()
    else:
        quit()


main_menu()
