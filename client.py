import socket


# функция, которая принимает строку из "bash.txt" 
# разбивает строку на команды (List) 
# наличие запрещённых команд (sudo) и при обнаружении уведомить (print)


sock_user= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_user.connect(('localhost',3000))
while True:
    msg=input(">>>")

    sock_user.send(msg.encode())
    output=sock_user.recv(1024)
    print(output.decode('UTF-8'))



