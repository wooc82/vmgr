import subprocess

#result = subprocess.run(['ls', '-l', '/home/wooc'], stdout=subprocess.PIPE).stdout.decode('utf-8')

#result = subprocess.getoutput('ls -l /home/wooc')

#virtualbox basic commands
list_vms = 'vboxmanage list vms --sorted'
list_running = 'vboxmanage list runningvms'
list_vmdetails = 'vboxmanage guestproperty enumerate '

vm = 'Ubuntu_3'
parameter = '-l'
vmname = '/home/wooc'
lsl = list_vmdetails + vm


def get_ip(vm_name):
    command = list_vmdetails + vm_name
    details_list = output_to_lines(command)
    print(details_list)
    #return ip




def output_to_lines(command):
#result = subprocess.run([vm, parameter, vmname], stdout=subprocess.PIPE).stdout.decode('utf-8')
    result = subprocess.getoutput(command)


    output_lines = []
    line_content = ''
    for char in result:
        if char != '\n':
            line_content = line_content + str(char)
        else:
            output_lines.append(line_content)
            line_content = ''
    return output_lines

    #for line_nr in range (0,len(output_lines)):
        #print(output_lines[line_nr])





print(output_to_lines(lsl))
print('\ttest\t')




#print(result)
#lista = subprocess.run(['ls', '/home/wooc'],)
