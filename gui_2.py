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
from dataclasses import dataclass
from typing import List
from PyQt5.QtCore import QTimer
from db_controller import DBController
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


def write_logs(host, port, error_bash, error_prog, error_usb, error_conn):
    with open("logs.txt", "a") as f:
        f.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {host} : {port} | {str(error_bash):<5} | {str(error_prog):<5} | {str(error_usb):<5} | {str(error_conn):<5}\n"
        )


class MyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client = Client()
        self.db_controller = DBController()

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

    def check_usb_devices(self, server_index=None):
        if server_index is None:
            server_index = self.combo_box.currentIndex()

        usb_devices = self.client.send_to("4", server_index)
        devices = parse_usb_history(usb_devices)
        usb_data = "".join(
            [f"{device.Product}{device.Serial_Number}{device.Bus_Port}" for device in devices])
        host_port = self.combo_box.itemText(server_index)

        if not self.db_controller.is_comp_exists(host_port):
            prog_data = self.client.send_to("5", server_index)
            self.db_controller.add_comp(host_port, usb_data, prog_data)
            return False
        else:
            return self.db_controller.check_usb(host_port, usb_data)

    def check_prog(self, server_index=None):
        if server_index is None:
            server_index = self.combo_box.currentIndex()

        host_port = self.combo_box.itemText(server_index)
        prog_data = self.client.send_to("5", server_index)

        if not self.db_controller.is_comp_exists(host_port):
            usb_devices = self.client.send_to("4", server_index)
            devices = parse_usb_history(usb_devices)
            usb_data = "".join(
                [f"{device.Product}{device.Serial_Number}{device.Bus_Port}" for device in devices])

            self.db_controller.add_comp(host_port, usb_data, prog_data)
            return False
        else:
            return self.db_controller.check_prog(host_port, prog_data)

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
                prog_error = self.check_prog(index_server)
                usb_error = self.check_usb_devices(index_server)

                errors = [bash_error, not prog_error, not usb_error, False]
                if True in errors:
                    write_logs(host, port[:-1], *errors)
                    self.screenshot(index_server)
            except Exception as e:
                print(e)
                QMessageBox.about(
                    self, "Warning", f"no connected - {host} : {port}")
                write_logs(host, port[:-1], *["undf", "undf", "undf", True])
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

    def screenshot(self, server_index):
        if server_index is None:
            server_index = self.combo_box.currentIndex()
        [host, port] = self.combo_box.itemText(server_index).split(":")
        self.client.get_image_from_server(server_index, host, port[:-1])

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
