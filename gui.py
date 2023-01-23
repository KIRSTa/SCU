from PyQt5.QtWidgets import (QWidget,QApplication,QLabel,QGridLayout,QPushButton)
import sys


class MyGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        
        label1 = QLabel("Дата и время")

        grid.addWidget(label1,0,2)
        
        
        grid.addWidget(QPushButton("Проверка целостности файлов"),0,1)
        grid.addWidget(QPushButton("История вызова терминала"),1,1)
        grid.addWidget(QPushButton("Контроль процессов"),2,1)
        grid.addWidget(QPushButton("Вывод на печать"),3,1)
        grid.addWidget(QPushButton("Справка"),0,0)

        self.setLayout(grid)

        self.setGeometry(500, 500, 500, 200)
        self.setWindowTitle("SCU")
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyGUI()
    sys.exit(app.exec_())