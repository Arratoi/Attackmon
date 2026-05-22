import sqlite3

conn = sqlite3.connect('Attackmon.db')
c = conn.cursor()
c.execute('''
Select * FROM Pokemon''')
for row in c.fetchall():
    print(row)
conn.commit()
conn.close()
