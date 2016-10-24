import sqlite3

conn = sqlite3.connect('squaker.db')
print "Opened database successfully"

cur = conn.cursor()
conn.execute('CREATE TABLE IF NOT EXISTS tweets2 (tweet TEXT)')
print "Table created successfully"


cur.execute("INSERT INTO tweets2 (tweet) VALUES (?)", ("Hello Squaker!",))


conn.commit()
msg = "Record successfully added"


cur.execute("select * from tweets2")

print cur.fetchall()
conn.close()
