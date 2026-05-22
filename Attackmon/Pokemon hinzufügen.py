import sqlite3

conn = sqlite3.connect('Attackmon.db')
cur = conn.cursor()
cur.execute('''
    Insert into Pokemon (P_NR, Name, Evolutionsstufe, Gewicht, Primärer_Typ, Sekundärer_Typ)
    VALUES (
    '50', 
    'Digda', 
    '1', 
    '0,8',
    'Boden', 
    '-')''')

conn.commit()
conn.close()