import hashlib
import subprocess

def get_hash_from_file(path_file):
    h= hashlib.sha256()
    with open(path_file,'r') as f:
        text = f.read()
    h.update(text.encode())
    return h.hexdigest()

def get_example_program():
    subprocess.getoutput('zgrep " installed " /var/log/dpkg.log* >> ex_prog.txt')
    with open("ex_prog.txt", 'r') as f:
        data = f.readlines()
        data = ''.join([''.join(s.split(' ')[-2:]) for s in data])
        print (data)
    return data.encode()




def get_bash_history():
    with open("bash.txt",'r') as f:
        text = f.read()
    return text

def get_check(text,f_commands):
    all_commands = text.splitlines()
    for user_command in all_commands:
        for search_command in f_commands:
            if search_command in user_command:
                return "False" 
    return "True"            

def get_usb_devices():
    result = subprocess.getoutput('usbrip events history -q >> uh.txt')
    with open("uh.txt", 'r') as f:
        data = f.read()
    return data.encode()

forbidden_commands = ["sudo","nmap","shutdown"]
