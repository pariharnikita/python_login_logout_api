import sqlite3
con = sqlite3.connect("user.db")
#con.execute("drop table USERS")  

con.execute("CREATE TABLE USERS (ID INTEGER PRIMARY KEY AUTOINCREMENT,USERNAME TEXT UNIQUE NOT NULL, PASSWORD TEXT NOT NULL)")
con.close()