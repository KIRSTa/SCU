from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLabel,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QMessageBox,
)
from client import Client
import sys
import mss
from dataclasses import dataclass
from typing import List
from PyQt5.QtCore import QTimer
from datetime import datetime


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


def get_hash_system():
    with open("hash.txt", "r") as f:
        hash_system = f.read()
    return hash_system


def parse_usb_history(usb_devices_text) -> List[UsbDevice]:
    data = usb_devices_text.split("−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−")[
        1:
    ]
    devices = []
    for device in data[1:-1]:
        devices.append(
            UsbDevice(
                *[d.split(": ")[-1].replace(" ", "") for d in device[1:-1].split("\n")]
            )
        )

    return devices


def write_logs(host, port, error_bash, error_hash, error_prog, error_conn):
    with open("logs.txt", "a") as f:
        f.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {host} : {port} | {error_bash} | {error_hash} | {error_prog} | {error_conn}\n"
        )


class MyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client = Client()

    def conn(self):
        host = self.host_line_edit.text()
        port = self.port_line_edit.text()
        try:
            self.client.server_connect(host, int(port))
            self.combo_box.addItem(f"{host} : {port}")
        except:
            QMessageBox.about(self, "allert", f"{host} : {port} crashed")

    def get_hash(self, server_index=None):
        if server_index is None:
            server_index = self.combo_box.currentIndex()
        hash_file = self.client.send_to("1", server_index)
        return hash_file


    def get_usb_devices(self):
        server_index = self.combo_box.currentIndex()
        usb_devices = self.client.send_to("4", server_index)
        devices = parse_usb_history(usb_devices)
        msg = ""
        for device in devices:
            msg += "=========================\n"
            msg += f"Connected:{device.Connected}\nProduct:{device.Product}\nSerial_Number:{device.Serial_Number}\nBus_Port:{device.Bus_Port}\n"
        QMessageBox.about(self, "Devices", msg)

    def get_ex_prog_bool(self, server_index=None):
        if server_index is None:
            server_index = self.combo_box.currentIndex()
        ex_prog = self.client.send_to("5", server_index)

        return ex_prog != get_hash_system()

    def get_ex_prog(self):
        if self.get_ex_prog_bool():
            QMessageBox.about(self, "Programm", "Изменение программ")

    def get_bash(self, server_index=None):
        if server_index is None:
            server_index = self.combo_box.currentIndex()
        bash_file = self.client.send_to("2", server_index)
        return bash_file


    def get_bash_bool(self, server_index=None):
        if server_index is None:
            server_index = self.combo_box.currentIndex()
        bash_file = self.client.send_to("3", server_index)
        return bash_file == "True"


    def ping_all(self):
        for index_server in range(self.combo_box.count()):
            [host, port] = self.combo_box.itemText(index_server).split(":")
            try:
                self.client.send_to("ping", index_server)
                bash_error = self.get_bash_bool(index_server)
                prog_error = self.get_ex_prog_bool(index_server)
                errors = [bash_error, prog_error, False, False]
                if True in errors:
                    write_logs(host, port[:-1], *errors)
            except:
                QMessageBox.about(self, "Warning", f"no connected - {host} : {port}")
                write_logs(host, port[:-1], *["-", "-", "-", True])
                self.client.server_reconnect(host, int(port), index_server)

    def connect_list(self):
        msg = ""
        with open("host_port.txt", "r") as f:
            hostes_portes = f.readlines()
        for host_port in hostes_portes:
            msg += host_port[:-1]
            [host, port] = host_port.split(":")
            try:
                self.client.server_connect(host, int(port))
                self.combo_box.addItem(f"{host}:{port}")
                msg += " connected \n"
            except:
                msg += " no connect... \n"
        QMessageBox.about(self, "allert", msg)
    def screenshot(self,server_index):
        if server_index is None:
            server_index = self.combo_box.currentIndex()
        self.client.get_image_from_server(server_index)

        


    def initUI(self):
        grid = QGridLayout()

        self.host_line_edit = QLineEdit()
        self.port_line_edit = QLineEdit()

        self.host_label = QLabel("Enter host")
        self.port_label = QLabel("Enter port")

        self.button_connect = QPushButton("Connect")
        self.button_connect.clicked.connect(self.conn)

        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(150)

        self.button_hash = QPushButton("Get_screenshot")
        self.button_hash.clicked.connect(self.screenshot)


        self.button_connect_list = QPushButton("Connect list")
        self.button_connect_list.clicked.connect(self.connect_list)



        grid.addWidget(self.host_line_edit, 0, 1)
        grid.addWidget(self.port_line_edit, 1, 1)
        grid.addWidget(self.button_connect, 2, 0)
        grid.addWidget(self.combo_box, 0, 2)
        grid.addWidget(self.button_connect_list, 1, 2)
        grid.addWidget(self.button_hash, 2, 2)
        grid.addWidget(self.host_label, 0, 0)
        grid.addWidget(self.port_label, 1, 0)
 

        self.setLayout(grid)

        self.setGeometry(500, 500, 500, 200)
        self.setWindowTitle("SCU")
        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.ping_all)
        timer.setInterval(20_000)
        timer.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyGUI()
    sys.exit(app.exec_())
