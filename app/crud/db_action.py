import sqlite3


class UserDatabase:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def insert_user(self, user_id, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM users WHERE user_id = ?
        ''', (user_id,))

        user = cursor.fetchone()

        if user:
            print(f"Пользователь с ID {user_id} уже существует.")
        else:
            cursor.execute('''
                INSERT INTO users (user_id, username)
                VALUES (?, ?)
            ''', (user_id, username))
            print(f"Пользователь с ID {user_id} был добавлен.")

        conn.commit()
        conn.close()

    def get_user_by_id(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM users WHERE user_id = ?
        ''', (user_id,))

        user = cursor.fetchone()
        conn.close()

        return user

    def get_all_users(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()

        return users


db = UserDatabase()