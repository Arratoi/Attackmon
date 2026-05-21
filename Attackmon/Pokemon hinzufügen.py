import sqlite3

conn = sqlite3.connect('Attackmon.db')
cur = conn.cursor()
cur.execute('''
    Insert into Pokemon (P_NR, Name, Evolutionsstufe, Gewicht, Primärer_Typ, Sekundärer_Typ)
    VALUES (
    '8', 
    'Schillok', 
    '2', 
    '22,5',
    'Wasser', 
    '-')''')

conn.commit()
conn.close()