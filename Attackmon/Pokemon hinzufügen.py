import sqlite3

conn = sqlite3.connect('Attackmon.db')
cur = conn.cursor()
cur.execute('''
    Insert into Pokemon (P_NR, Name, Evolutionsstufe, Gewicht, Primärer_Typ, Sekundärer_Typ)
    VALUES (
    '21', 
    'Habitak', 
    '1', 
    '2',
    'Normal', 
    'Flug')''')

conn.commit()
conn.close()