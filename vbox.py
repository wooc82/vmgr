import subprocess
import re

#result = subprocess.run(['ls', '-l', '/home/wooc'], stdout=subprocess.PIPE).stdout.decode('utf-8')

#result = subprocess.getoutput('ls -l /home/wooc')

#virtualbox basic commands
list_vms_cmd = 'vboxmanage list vms --sorted'
list_running_cmd = 'vboxmanage list runningvms --sorted'
list_vmdetails_cmd = 'vboxmanage guestproperty enumerate '


vm_list = []
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
    return vm_list


def get_ip(vm_name):
    command = list_vmdetails + vm_name
    details_list = output_to_lines(command)
    for lnnr in range(len(details_list)):
        line_content = details_list[lnnr]
        if line_content.__contains__("V4/IP"):
            IP_addr = line_content.split()[3][:-1]
        else:
            IP_addr = "Check g additions"
    return IP_addr


#function that can run any command and put output in to list one line per list item
def output_to_lines(command):
    result = subprocess.getoutput(command)
    length = len(result)
    possition = 0
    output_lines = []
    line_content = ''
    for char in result:
        possition = possition + 1
        if char != '\n' and possition != length-1:
            line_content = line_content + str(char)
        else:
            output_lines.append(line_content)
            line_content = ''
    return output_lines


def list_all_vms():
    vmlist()
    for vmnumber in range(len(vm_list)):
        print(vmnumber, "\t", vm_list[vmnumber])


def list_running_vms():
    runningvmlist()
    for vmnumber in range(len(running_vm_list)):
        print(vmnumber, "\t", running_vm_list[vmnumber])


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

    if option == "q":
        quit()
    else:
        quit()


main_menu()