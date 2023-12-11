import sqlite3 as sq

con = sq.connect("PhoneDirectory_DataBase.db")
cur = con.cursor()
cur.close()
con.close()