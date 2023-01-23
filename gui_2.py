from PyQt5.QtWidgets import (QWidget,QApplication,QLabel,QGridLayout,QPushButton,QLineEdit,QComboBox)
from client import Client
import sys



class MyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client = Client()
    def conn(self):
        host = self.host_line_edit.text()
        port = self.port_line_edit.text()
        self.combo_box.addItem(f"{host}:{port}")
        self.client.server_connect(host,int(port))
    def get_hash(self):
        server_index = self.combo_box.currentIndex()
        hash_file = self.client.send_to("1",server_index) 
        self.hash_label.setText(hash_file)
    def get_bash(self):
        server_index = self.combo_box.currentIndex()
        bash_file = self.client.send_to("2",server_index)
        self.bash_label.setText(bash_file)
        bash_file = self.client.send_to("3",server_index)
        self.history_label.setText(bash_file)

        
        

    def initUI(self):
        grid = QGridLayout()
        
        self.host_line_edit = QLineEdit() 
        self.port_line_edit = QLineEdit() 

        self.hash_label = QLabel("HASH")
        self.bash_label = QLabel("BASH")
        self.history_label = QLabel("Allarm")

        self.button_connect = QPushButton("Connect")
        self.button_connect.clicked.connect(self.conn)

        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(150)

        self.button_hash = QPushButton("Get Hash")
        self.button_hash.clicked.connect(self.get_hash)
        self.button_bash = QPushButton("Get Bash")
        self.button_bash.clicked.connect(self.get_bash)
        

        grid.addWidget(self.host_line_edit,0,0)
        grid.addWidget(self.port_line_edit,1,0)
        grid.addWidget(self.button_connect,2,0)
        grid.addWidget(self.combo_box,0,2)
        grid.addWidget(self.button_hash,1,2)
        grid.addWidget(self.button_bash,2,2)
        grid.addWidget(self.hash_label,3,1)
        grid.addWidget(self.bash_label,4,1)
        grid.addWidget(self.history_label,5,1)


        

        self.setLayout(grid)

        self.setGeometry(500, 500, 500, 200)
        self.setWindowTitle("SCU")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyGUI()
    sys.exit(app.exec_())