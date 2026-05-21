import sqlite3

conn = sqlite3.connect('Attackmon.db')
cur = conn.cursor()
cur.execute('''
    Insert into Pokemon (P_NR, Name, Evolutionsstufe, Gewicht, Primärer_Typ, Sekundärer_Typ)
    VALUES (
    '20', 
    'Rattikarl', 
    '2', 
    '18,5',
    'Normal', 
    '-')''')

conn.commit()
conn.close()