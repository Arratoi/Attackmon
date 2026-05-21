import sqlite3

conn = sqlite3.connect('Attackmon.db')
c = conn.cursor()

c.execute('''
INSERT INTO ZT_LVL (Level, ATT_NR, P_NR)
VALUES
(
'1',   
'33',
'2'
)
''')

conn.commit()
conn.close()
#1. --> Level mit den das Pokemon die Attacke erlernt
#2. --> Nummer der TM / Attacke
#3. --> Pokemon seine Pokedex Nummer