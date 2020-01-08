import subprocess

#result = subprocess.run(['ls', '-l', '/home/wooc'], stdout=subprocess.PIPE).stdout.decode('utf-8')

#result = subprocess.getoutput('ls -l /home/wooc')

vm = 'ls -l '
parameter = '-l'
vmname = '/home/wooc'
lsl = vm + vmname

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


    for line_nr in range (0,len(output_lines)):
        print(output_lines[line_nr])



print(output_to_lines(lsl))
print('\ttest\t')




#print(result)
#lista = subprocess.run(['ls', '/home/wooc'],)
