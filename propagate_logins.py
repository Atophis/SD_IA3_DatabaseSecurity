import sqlite3
import hashlib

conn = sqlite3.connect("login_information.db")
cursor = conn.cursor()

# creates a table called login_information
# stores integer ID, 255 byte non-unicode username, and 255 byte non-unicode password
cursor.execute("""CREATE TABLE IF NOT EXISTS login_information (id INTEGER PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)""")
# cursor.execute("""DROP TABLE IF EXISTS login_information""")

# manual input of username and password 1
username1, password1 = "admin", "358921_nouser"
password1 = hashlib.sha256(password1.encode()).hexdigest()

# manual input of username and password 2
username2, password2 = "admin2", "n1o3u5s2er90!"
password2 = hashlib.sha256(password2.encode()).hexdigest()

cursor.execute("INSERT INTO login_information (username, password) VALUES (?, ?)", (username1, password1))
cursor.execute("INSERT INTO login_information (username, password) VALUES (?, ?)", (username2, password2))

conn.commit()