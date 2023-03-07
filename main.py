from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QLineEdit,
    QLabel,
    QWidget,
    QGridLayout,
    QMessageBox,
)

import sys

from gui_2 import MyGUI
from db_controller import DBController


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.w = None
        self.db_controller = DBController()
        self.is_verify = False

        grid = QGridLayout()

        self.button_login = QPushButton("Вход")
        self.button_reg = QPushButton("Регистрация")

        self.login_line_edit = QLineEdit()
        self.passw_line_edit = QLineEdit()

        self.button_login.clicked.connect(self.show_main_app)
        self.button_reg.clicked.connect(self.registration)

        grid.addWidget(self.login_line_edit, 0, 0)
        grid.addWidget(self.passw_line_edit, 0, 1)
        grid.addWidget(self.button_login, 1, 0)
        grid.addWidget(self.button_reg, 1, 1)
        self.setLayout(grid)
        self.setGeometry(500, 500, 500, 200)

    def check_passw_and_login(self):
        login = self.login_line_edit.text()
        passw = self.passw_line_edit.text()

        if self.db_controller.verification(login, passw):
            return True
        else:
            QMessageBox.about(
                self, "Ошибка!", "Не правельный пароль или логин!")
            return False

    def registration(self):
        if self.is_verify:
            login = self.login_line_edit.text()
            passw = self.passw_line_edit.text()

            if not self.db_controller.is_login_exists(login):
                self.db_controller.add_user(login, passw)
                QMessageBox.about(self, "Ок", f"Пользователь {login} создан.")
            else:
                QMessageBox.about(self, "Ошибка", "Такой логин уже есть.")
        else:
            QMessageBox.about(self, "Ошибка", "Вы не авторизованы!")

    def show_main_app(self):
        if self.check_passw_and_login():
            self.is_verify = True
            if self.w is None:
                self.w = MyGUI()
                self.w.show()
                self.showMinimized()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
