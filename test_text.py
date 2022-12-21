with open("bash.txt",'r') as f:
        text = f.read()
        r = text.splitlines()
        for i in r:
            if i == "sudo su":
                print("alarm")
            elif i == "cd":
                print("nice")
        
        