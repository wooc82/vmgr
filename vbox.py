import subprocess
import re

#result = subprocess.run(['ls', '-l', '/home/wooc'], stdout=subprocess.PIPE).stdout.decode('utf-8')

#result = subprocess.getoutput('ls -l /home/wooc')

#virtualbox basic commands
list_vms_cmd = 'vboxmanage list vms --sorted'
list_running_cmd = 'vboxmanage list runningvms --sorted'
list_vmdetails_cmd = 'vboxmanage guestproperty enumerate '
list_natnets_cmd = 'vboxmanage list natnets'
natnet_rule_cmd = 'vboxmanage natnetwork modify --netname NatNetwork'


output_lines = []
vm_list = []
power_off_list = []
running_vm_list = []
vm = 'Ubuntu_3'
lsl = list_vmdetails_cmd + vm
IP_addr = ""
onoff = ""


class vboxvm:
    def __init__(self, name):
        self.name = name
        self.IP = IP_addr
        self.status = onoff


#list all running VMs configured in Virtualbox
def vmlist():
    #using global variable and clearing the list
    global vm_list
    vm_list = []
    #loading list_vms_cmd output to the list
    vmlist_output = output_to_lines(list_vms_cmd)
    #extracting hostnames and adding them to the vm_list list
    for line_number in range(len(vmlist_output)):
        line_content = vmlist_output[line_number]
        capture_name = re.findall(r'"(.*?)"',line_content)
        vm_list.append(capture_name[0])
    return vm_list


#list all VMs configured in Virtualbox
def runningvmlist():
    #using global variable and clearing the list
    global running_vm_list
    running_vm_list = []
    #loading list_vms_cmd output to the list
    running_vm_list_output = output_to_lines(list_running_cmd)
    #extracting hostnames and adding them to the vm_list list
    for line_number in range(len(running_vm_list_output)):
        line_content = running_vm_list_output[line_number]
        capture_name = re.findall(r'"(.*?)"',line_content)
        running_vm_list.append(capture_name[0])
    return running_vm_list

def offvmlist():
    global power_off_list
    global running_vm_list
    global vm_list
    vmlist()
    runningvmlist()
    power_off_list = vm_list
    for vm in power_off_list:
        if vm in running_vm_list:
           power_off_list.remove(vm)
    return power_off_list




def get_ip(vm_name):
    command = list_vmdetails_cmd + vm_name
    details_list = output_to_lines(command)
    for lnnr in range(len(details_list)):
        line_content = details_list[lnnr]
        if line_content.__contains__("V4/IP"):
            IP_addr = line_content.split()[3][:-1]
            return IP_addr
        else:
            IP_addr = "Check g additions"
    return IP_addr



#function that can run any command and put output in to list one line per list item
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
            output_lines.append(line_content)
            line_content = ''
    return output_lines




def list_all_vms():
    vmlist()
    for vmnumber in range(len(vm_list)):
        name = vm_list[vmnumber]
        runningvmlist()
        if name in running_vm_list:
            IP = get_ip(name)
        else:
            IP = "Powered Down"
        if len(name)<5:
            tab = "\t\t\t"
        elif 5<len(name)<10:
            tab = "\t\t"
        elif len(name)>=10:
            tab = "\t"
        print(vmnumber, "\t", name, tab, IP)


def list_running_vms():
    runningvmlist()
    for vmnumber in range(len(running_vm_list)):
        print(vmnumber, "\t", running_vm_list[vmnumber])

def list_offline_vms():
    offvmlist()
    for vmnumber in range(len(power_off_list)):
        print(vmnumber, "\t", power_off_list[vmnumber])

def start_vm():
    list_offline_vms()
    vmnumber = int(input("\nPick VM to Start: "))
    vmtostart = power_off_list[vmnumber]
    command = "vboxmanage startvm " + vmtostart
    output_to_lines(command)
    for line in output_lines:
        print(line)

def option_3():
    start_vm()
    print("\nWhat you want to do next:")
    print("1.) Start another VM")
    print("2.) Go back to main menu")
    option = input("\nPick and option: ")
    if option == "1":
        option_3()
    if option == "2":
        main_menu()




def main_menu():
    print("\nPick and action:")
    print("1.) List all VMs, their status and IPs")
    print("2.) List Running VMs")
    print("3.) Start specific VMs")
    print("4.) Stop specific VMs - nicely")
    print("5.) Stop specific VMs - hard")
    print("6.) Show port forwarding config")
    print("7.) Generate / update port forwarding config")
    print("8.) Update ssh config file on the server for accessing VMs from outside the NAT network")
    print("9.) Generate / update configs for RDP sessions to access Windows servers from outside NAT network\n")
    print('Press "q" to quit')

    option = input("Pick and option: ")
    if option == "1":
        list_all_vms()
        input("\nPress enter to go back to main menu...")
        main_menu()
    if option == "2":
        list_running_vms()
        input("\nPress enter to go back to main menu...")
        main_menu()
    if option == "3":
        option_3()




    if option == "q":
        quit()
    else:
        quit()


main_menu()