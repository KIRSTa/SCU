import socket

class Client:
    def __init__(self) -> None:
        self.servers = {}
        
    def server_connect(self,host,port):
        self.sock_user = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock_user.connect((host,port))
        self.servers[len(self.servers)] = self.sock_user

    def server_reconnect(self,host,port,index):
        try:
            self.sock_user = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock_user.connect((host,port))
            self.servers[index] = self.sock_user
        except:
            pass

    def send_to(self,msg,server_index,to_text=True):
        self.servers[server_index].send(msg.encode('UTF-8'))
        if to_text:
            output=self.servers[server_index].recv(10024)
        else:
            output=self.servers[server_index].recv(30_0024)
        return output.decode() if to_text else output
