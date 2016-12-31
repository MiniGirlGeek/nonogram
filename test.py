import sqlite3
conn = sqlite3.connect('nonogram_database.db')

c = conn.cursor()
c.execute('''CREATE TABLE users (
                 ID INTEGER PRIMARY KEY autoincrement,
                 NAME VARCHAR NOT NULL,
                 DOB DATETIME NOT NULL,
                 USERNAME VARCHAR NOT NULL,
                 PASSWORD VARCHAR NOT NULL
             );''')
conn.commit()
conn.close()
