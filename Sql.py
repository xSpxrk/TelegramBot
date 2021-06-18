import sqlite3


class SQL:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def add_user(self, user_id, username, chat_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `Users` (`UserId`, `Username`, `ChatId`) VALUES (?, ?, ?)",
                                (user_id, username, chat_id))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Users` WHERE `UserId` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def get_chats_id(self):
        with self.connection:
            return self.cursor.execute("SELECT ChatId FROM USERS").fetchall()
