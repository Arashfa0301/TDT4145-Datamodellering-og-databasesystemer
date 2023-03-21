import os
from createDatabase import createDatabase
from fillDatabase import fillDatabase

if os.path.exists("trainstationDB.db"):
    os.remove("trainstationDB.db")

createDatabase()
fillDatabase()
