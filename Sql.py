import sqlite3


class SQL:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, username, bot, first_name, last_name):
        with self.connection:
            self.cursor.execute("INSERT INTO `Users` (`UserId`, `Username`, `Bot`, `FirstName`, `LastName`) VALUES ("
                                "?, ?, ?, ?, ?)",
                                (user_id, username, bot, first_name, last_name))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Users` WHERE `UserId` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def get_users_id(self):
        with self.connection:
            return self.cursor.execute("SELECT UserId FROM USERS").fetchall()

    def get_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM USERS WHERE UserId = ?", (user_id,)).fetchall()