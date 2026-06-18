import sqlite3

conn = sqlite3.connect('Attackmon.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS Fundorte(
Route TEXT NOT NULL,
P_Nr INTEGER NOT NULL,
Wahrscheinlichkeit TEXT,
LEVEL TEXT,
FOREIGN KEY(P_Nr) REFERENCES Pokemon(P_Nr),
PRIMARY KEY(Route,P_Nr))''')


conn.commit()
conn.close()
