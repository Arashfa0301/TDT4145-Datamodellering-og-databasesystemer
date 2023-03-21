import sqlite3

con = sqlite3.connect("database.db")

cursor = con.cursor()
cursor.execute(
    """CREATE TABLE person
                    (id INTEGER PRIMARY KEY, name TEXT, birthday TEXT)"""
)
cursor.execute("""INSERT INTO person VALUES (1, 'Ola Nordmann', '2002-02-02')""")
