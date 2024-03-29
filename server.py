import socket
from server_utils import *
import mss


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_stream.bind((self.host, self.port))
        self.sock_stream.listen(1)

    def listen_connection(self):
        self.client_conn, self.client_addr = self.sock_stream.accept()

    def run(self):
        self.listen_connection()
        print(f"Connection access: {self.client_addr}")
        while True:
            data = self.client_conn.recv(1024)
            if not data:
                break
            inp = data.decode('UTF-8')
            if inp == "2":
                inp_file = get_bash_history()
                self.client_conn.send(inp_file.encode())
            elif inp == "3":
                ex = get_bash_history()
                inp_ex = get_check(ex, forbidden_commands)
                self.client_conn.send(inp_ex.encode())
            elif inp == "4":
                inp_ex = get_usb_devices()
                self.client_conn.send(inp_ex)
            elif inp == "5":
                example = get_example_program()
                self.client_conn.send(example.encode())
                print(example)
            elif inp == "ping":
                self.client_conn.send(b'ok')
            elif inp == "screen":
                with mss.mss() as sct:
                    filename = sct.shot(output="screen.png")

                screen_img = open('screen.png', 'rb')
                image_data = screen_img.read(2048)
                while image_data:
                    self.client_conn.send(image_data)
                    image_data = screen_img.read(2048)
                screen_img.close()
                self.client_conn.send(b'screen_done')


server = Server('localhost', 3010)
server.run()
