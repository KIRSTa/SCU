from client import Client 

c1 = Client()
c1.server_connect('localhost',3010)
print(c1.send_to('2',0))
