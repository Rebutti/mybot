import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = (?)", (user_id,)).fetchmany(1)
            return bool(len(result))
    
    def add_user(self, user_id, username):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    def get_all(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM users")
    def get_user_by_username(self, username):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM users WHERE username = (?)", (username,)).fetchmany(1)
            if bool(len(result)):
                return result[0][0]
            else:
                return -1

