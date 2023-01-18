import socket

servers = []

# sock_user = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# sock_user.connect(('localhost',3000))

while True:
    msg=input(">>>")
    if msg == "conn":
        host=input("Enter host: ")
        port=input("Enter port: ")
        sock_user = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock_user.connect((host,int(port)))
        servers.append(sock_user)
    elif msg == "send":
        servers_index = input(f"Enter index(0-{len(servers)-1}): ")
        client_msg = input(">>>")
        servers[int(servers_index)].send(client_msg.encode())
        output=servers[int(servers_index)].recv(1024)
        print(output.decode('UTF-8'))



