import socket
import hashlib

def get_hash_from_file(path_file):
    h= hashlib.sha256()
    with open(path_file,'r') as f:
        text = f.read()
    h.update(text.encode())
    return h.hexdigest()

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
        

forbidden_commands = ["sudo","nmap","shutdown"]

    


sock_stream = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_stream.bind(('localhost',3006))
sock_stream.listen(1)
conn, addr = sock_stream.accept()
print(f"Connection access: {addr}" )
while True:
    data = conn.recv(1024)
    inp = data.decode('UTF-8')
    if inp == "1":
        hash_file = get_hash_from_file("test.txt")
        conn.send(hash_file.encode())
    elif inp == "2":
        inp_file = get_bash_history()
        conn.send(inp_file.encode())
    elif inp == "3":
        ex = get_bash_history()
        inp_ex = get_check(ex,forbidden_commands)
        conn.send(inp_ex.encode())
    print(data.decode('UTF-8'))