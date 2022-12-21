def get_check(f_commands,text):
    all_commands = text.splitlines()
    for user_command in all_commands:
        for search_command in f_commands:
            if search_command in user_command:
                return "False" 
    return "True"            
        

forbidden_commands = ["sudo","nmap","shutdown"]
user_command = """cd
ls
mkdir
chmod
sudo su
nmap"""
print (get_check(forbidden_commands,user_command))