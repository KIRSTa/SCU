from PyQt5.QtWidgets import (QWidget,QApplication,QLabel,QGridLayout,QPushButton,QLineEdit,QComboBox,QMessageBox)
from client import Client
import sys
from dataclasses import dataclass
from typing import List

@dataclass
class UsbDevice:
    Connected: str
    Host: str
    VID: str
    PID: str
    Product: str
    Manufacturer: str
    Serial_Number: str
    Bus_Port: str
    Disconnected: str

def parse_usb_history(usb_devices_text)->List[UsbDevice]:
    data = usb_devices_text.split("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−")[1:]
    devices = []
    for device in data[1:-1]:
        devices.append(
            UsbDevice(
                *[d.split(": ")[-1].replace(" ", "") for d in device[1:-1].split("\n")]
            )
        )

    return devices


class MyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client = Client()
    def conn(self):
        host = self.host_line_edit.text()
        port = self.port_line_edit.text()
        try:
            self.client.server_connect(host,int(port))
            self.combo_box.addItem(f"{host} : {port}")            
        except:
            QMessageBox.about(self,"allert",f"{host} : {port} crashed")
    def get_hash(self):
        server_index = self.combo_box.currentIndex()
        hash_file = self.client.send_to("1",server_index) 
        self.hash_label.setText(hash_file)
    
    def get_usb_devices(self):
        server_index = self.combo_box.currentIndex()
        usb_devices = self.client.send_to("4",server_index) 
        devices = parse_usb_history(usb_devices)
        for device in devices:
            print("=========================")
            print(f'Connected:{device.Connected}\nProduct:{device.Product}\nSerial_Number:{device.Serial_Number}\nBus_Port:{device.Bus_Port}')


    def get_bash(self):
        server_index = self.combo_box.currentIndex()
        bash_file = self.client.send_to("2",server_index)
        self.bash_label.setText(bash_file)
        bash_file = self.client.send_to("3",server_index)
        self.history_label.setText(bash_file)
    def connect_list(self):
        msg = ''
        with open("host_port.txt",'r') as f:
            hostes_portes = f.readlines()
        for host_port in hostes_portes:
            msg += host_port[:-1]
            [host,port] = host_port.split(":")
            try:
                self.client.server_connect(host,int(port))
                self.combo_box.addItem(f"{host}:{port}")
                msg += " connected \n"
            except:
                msg += " no connect... \n"
        QMessageBox.about(self,"allert",msg)
        

        
    def initUI(self):
        grid = QGridLayout()
        
        self.host_line_edit = QLineEdit() 
        self.port_line_edit = QLineEdit() 

        self.hash_label = QLabel("HASH")
        self.bash_label = QLabel("BASH")
        self.history_label = QLabel("Allarm")
        self.host_label = QLabel("Enter host")
        self.port_label = QLabel("Enter port")

        self.button_connect = QPushButton("Connect")
        self.button_connect.clicked.connect(self.conn)

        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(150)

        self.button_hash = QPushButton("Get Hash")
        self.button_hash.clicked.connect(self.get_hash)

        self.button_bash = QPushButton("Get Bash")
        self.button_bash.clicked.connect(self.get_bash)

        self.button_connect_list = QPushButton("Connect list")
        self.button_connect_list.clicked.connect(self.connect_list)
        
        self.button_get_usb = QPushButton("Get USB devices")
        self.button_get_usb.clicked.connect(self.get_usb_devices)


        grid.addWidget(self.host_line_edit,0,1)
        grid.addWidget(self.port_line_edit,1,1)
        grid.addWidget(self.button_connect,2,0)
        grid.addWidget(self.combo_box,0,2)
        grid.addWidget(self.button_hash,2,2)
        grid.addWidget(self.button_bash,3,2)
        grid.addWidget(self.button_connect_list,1,2)
        grid.addWidget(self.host_label,0,0)
        grid.addWidget(self.port_label,1,0)
        grid.addWidget(self.hash_label,3,1)
        grid.addWidget(self.bash_label,4,1)
        grid.addWidget(self.history_label,5,1)
        grid.addWidget(self.button_get_usb,3,3)


        self.setLayout(grid)

        self.setGeometry(500, 500, 500, 200)
        self.setWindowTitle("SCU")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyGUI()
    sys.exit(app.exec_())