import socket

class Client:
    def __init__(self) -> None:
        self.servers = []
        self.sock_user = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def server_connect(self,host,port):
        self.sock_user.connect((host,port))
        self.servers.append(self.sock_user)
    def send_to(self,msg,server_index):
        self.servers[server_index].send(msg.encode())
        output=self.servers[server_index].recv(1024)
        return output.decode("UTF-8")
