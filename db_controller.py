import sqlite3
from hashlib import sha256


class DBController:
    def __init__(self, db_name="t.sqlite") -> None:
        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()

        if not self._table_exists():
            self._create_table()
            self.add_user("admin", "admin")
        if not self._table_exists_comps():
            self._create_table_comps()

    def _table_exists(self):
        self.cursor.execute(
            """SELECT name FROM sqlite_master WHERE name='users'""")
        tables = self.cursor.fetchall()
        return len(tables) == 1

    def _table_exists_comps(self):
        self.cursor.execute(
            """SELECT name FROM sqlite_master WHERE name='comps'""")
        tables = self.cursor.fetchall()
        return len(tables) == 1

    def _create_table(self):
        self.cursor.execute(
            """CREATE TABLE users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        login TEXT, 
                        password TEXT)
                    """
        )
        self.con.commit()

    def _create_table_comps(self):
        self.cursor.execute(
            """CREATE TABLE comps
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        hostport TEXT, 
                        hashusb TEXT,
                        hashprog TEXT)
                    """
        )
        self.con.commit()

    def add_comp(self, host_port, usb_data, prog_data):
        hash_usb = sha256(usb_data.encode('UTF-8')).hexdigest()
        # hash_prog = sha256(prog_data.encode('UTF-8')).hexdigest()
        hash_prog = prog_data
        self.cursor.execute(
            "INSERT INTO comps (hostport,hashusb,hashprog) VALUES (?, ?,?)", (
                host_port, hash_usb, hash_prog)
        )
        self.con.commit()

    def get_hash_usb_by_host_port(self, host_port):
        self.cursor.execute(
            f"SELECT hashusb FROM comps WHERE hostport == {host_port}")
        return self.cursor.fetchall()[0]

    def check_usb(self, host_port, usb_data):
        hash_usb = sha256(usb_data.encode('UTF-8')).hexdigest()
        self.cursor.execute(
            f"SELECT id  FROM comps WHERE hostport == '{host_port}' AND hashusb == '{hash_usb}'"
        )
        users = self.cursor.fetchall()
        return len(users) >= 1

    def check_prog(self, host_port, prog_data):
        # hash_prog = sha256(prog_data.encode('UTF-8')).hexdigest()
        hash_prog = prog_data
        self.cursor.execute(
            f"SELECT id  FROM comps WHERE hostport == '{host_port}' AND hashprog == '{hash_prog}'"
        )
        users = self.cursor.fetchall()
        return len(users) >= 1

    def is_comp_exists(self, host_port):
        self.cursor.execute(
            f"SELECT id  FROM comps WHERE hostport == '{host_port}'")
        users = self.cursor.fetchall()
        return len(users) == 1

    def add_user(self, login, password):
        login_hash = sha256(login.encode('UTF-8')).hexdigest()
        passw_hash = sha256(password.encode('UTF-8')).hexdigest()
        self.cursor.execute(
            "INSERT INTO users (login, password) VALUES (?, ?)", (login_hash, passw_hash)
        )
        self.con.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def is_login_exists(self, login):
        login_hash = sha256(login.encode('UTF-8')).hexdigest()
        self.cursor.execute(
            f"SELECT id  FROM users WHERE login == '{login_hash}'")
        users = self.cursor.fetchall()
        return len(users) == 1

    def verification(self, login, password):
        login_hash = sha256(login.encode('UTF-8')).hexdigest()
        passw_hash = sha256(password.encode('UTF-8')).hexdigest()
        self.cursor.execute(
            f"SELECT id  FROM users WHERE login == '{login_hash}' AND password == '{passw_hash}'"
        )
        users = self.cursor.fetchall()
        return len(users) >= 1
