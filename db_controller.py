import sqlite3


class DBController:
    def __init__(self, db_name="t.db") -> None:
        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()

        if not self._table_exists():
            self._create_table()
            self.add_user("admin", "admin")

    def _table_exists(self):
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE name='users'""")
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

    def add_user(self, login, password):
        self.cursor.execute(
            "INSERT INTO users (login, password) VALUES (?, ?)", (login, password)
        )
        self.con.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def is_login_exists(self, login):
        self.cursor.execute(f"SELECT id  FROM users WHERE login == '{login}'")
        users = self.cursor.fetchall()
        return len(users) == 1

    def verification(self, login, password):
        self.cursor.execute(
            f"SELECT id  FROM users WHERE login == '{login}' AND password == '{password}'"
        )
        users = self.cursor.fetchall()
        return len(users) >= 1
