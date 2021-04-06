import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    def add_tank(self, name, ab, rb, sb):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'fr' ('name', 'ab', 'rb', 'sb') VALUES(?,?,?,?)", (name, ab, rb, sb))
    def close(self):
        """Закрываем соединение"""
        self.connection.close()