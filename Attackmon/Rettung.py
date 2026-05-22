import sqlite3

conn = sqlite3.connect('Attackmon.db')
c = conn.cursor()

c.execute('''
ALTER TABLE Pokemon Name = Didga Values ('Digda')
''')



conn.commit()
conn.close()