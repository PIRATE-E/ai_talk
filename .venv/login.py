import base64
import hashlib
import secrets
import sqlite3


class LoginAI():
    _current_user = None
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.userpresent = False  # this flag for check that user is already exist or not
        self.current_user = LoginAI._current_user
        pass

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                username TEXT PRIMARY KEY,
                hashed_password TEXT,
                salt TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    prompt TEXT,
                    response TEXT,
                    FOREIGN KEY (username) REFERENCES users(username)
                    )
                """
            )
            conn.commit()

    def _generate_salt(self):
        # this method will called when we have to insert user into data base
        return secrets.token_bytes(16)

    def _hash_password(self, password, salt):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

    def create_account(self, username, password):
        self.cursor.execute(
            """
            SELECT 1 FROM users WHERE username = ?
            """, (username,)
        )

        if self.cursor.fetchone():
            self.userpresent = True
            return False  # user is already present

        salt = self._generate_salt()
        hashed_password = self._hash_password(password, salt)

        salt_b64 = base64.b64encode(salt)
        hashed_password_b64 = base64.b64encode(hashed_password)

        self.cursor.execute(
            """
            INSERT INTO users(username, hashed_password, salt) VALUES(?, ?, ?)
            """, (username, hashed_password_b64, salt_b64)
        )

        self.conn.commit()
        LoginAI._current_user = username
        return True  # account has been made

    def login(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            self.cursor.execute(
                """
                SELECT salt, hashed_password FROM users WHERE username = ?
                """, (username,)
            )
            row = self.cursor.fetchone()
            if row:  # user is present in the db
                salt, hashed_password = row
                salt = base64.b64decode(salt)
                hashed_password = base64.b64decode(hashed_password)
                if self._hash_password(password, salt) == hashed_password:
                    self.current_user = username
                    LoginAI._current_user = username
                    return True
                else:
                    return False

            else:
                return False

    @classmethod
    def get_username(cls):
        return cls._current_user