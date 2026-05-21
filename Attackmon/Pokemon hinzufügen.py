import sqlite3

conn = sqlite3.connect('Attackmon.db')
cur = conn.cursor()
cur.execute('''
    Insert into Pokemon (P_NR, Name, Evolutionsstufe, Gewicht, Primärer_Typ, Sekundärer_Typ)
    VALUES (
    '9', 
    'Turtok', 
    '3', 
    '85,5',
    'Wasser', 
    '-')''')

conn.commit()
conn.close()