import sqlite3

conn = sqlite3.connect('Attackmon.db')
c = conn.cursor()

c.execute('''
INSERT INTO Rettung (Level, ATT_NR, P_NR)
   SELECT Level, ATT_NR, P_NR FROM ZT_LVL;''')
c.execute('''
DROP TABLE ZT_LVL;''')
c.execute('''
ALTER TABLE Rettung RENAME TO ZT_LVL;''')


conn.commit()
conn.close()